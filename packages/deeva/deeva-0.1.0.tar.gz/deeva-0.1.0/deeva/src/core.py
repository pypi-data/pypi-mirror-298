import streamlit as st

import itertools
import random
from functools import partial
from stqdm import stqdm
from collections import Counter
from multiprocessing import Manager, Pool

import cv2
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

from .utils import check_image, get_color_distribution

from loaders.utils import *
from configs import configs
from loaders.converters import voc_to_yolo, yolo_to_voc
from utils import is_image, is_label, has_ext, get_name, complete_with_ext, get_ext


class DataMatch(object):
    """
    Class to manage and analyze data files in a structured directory.

    Parameters
    ----------
    data_path : str
       Path to the root directory containing the data
    """

    class Stats:
        """
        Handles the statistics related to a category ('images' or 'labels')

        Parameters
        ----------
        which : str
           Specifies the type of files being processed ('images' or 'labels').

        filenames : list of str
           List of filenames to be analyzed.
        """

        def __init__(self, which, filenames):
            self.which = which
            self.filenames = sorted(filenames)

            self.no_ext = []
            self.wrong_format = []
            self.duplicates = []
            self.correct = []

            self.stats_ = None

        def _is_correct_format(self):
            if self.which == 'images':
                return is_image
            if self.which == 'labels':
                return is_label

        def _collect_stats(self):
            """
            Collect statistics by categorizing filenames into
                - no extension
                - wrong format
                - duplicates
                - correct.

            Returns
            -------
            dict
               A dictionary containing categorized filenames.
            """

            for filename in self.filenames:
                if not has_ext(filename):
                    self.no_ext.append(filename)
                    continue
                if not self._is_correct_format()(filename):
                    self.wrong_format.append(filename)
                    continue

                self.correct.append(filename)

            # collecting duplicates
            for i in range(1, len(self.filenames)):
                if get_name(self.filenames[i - 1]) == get_name(self.filenames[i]):
                    if all(duplicate not in self.no_ext + self.wrong_format
                           for duplicate in self.filenames[i - 1:i + 1]):
                        self.duplicates.append(self.filenames[i])

            return {'No extension': self.no_ext,  # Change this part, you idiot
                    'Wrong format': self.wrong_format,
                    'Duplicates by filename': self.duplicates,
                    'Correct': self.correct}

        def get_stats(self):
            if not self.stats_:
                stats = self._collect_stats()
                self.stats_ = stats

            return self.stats_

    def __init__(self, data_path):
        self.data_path = data_path
        self.image_filenames, self.label_filenames = self.get_filenames(data_path)
        self.image_stats = self.Stats(which='images', filenames=self.image_filenames)
        self.label_stats = self.Stats(which='labels', filenames=self.label_filenames)

    @st.cache_data(show_spinner=False)
    def get_layout_stats(_self):
        image_stats = _self.image_stats.get_stats()
        label_stats = _self.label_stats.get_stats()

        return {'images': image_stats,
                'labels': label_stats}

    def get_garbage(_self):
        """Return all corrupted categories as a dict of dicts"""
        return {
            'images': dict(no_ext=_self.image_stats.no_ext, not_a_right_format=_self.image_stats.wrong_format,
                           duplicates=_self.image_stats.duplicates),
            'labels': dict(no_ext=_self.label_stats.no_ext, not_a_right_format=_self.label_stats.wrong_format,
                           duplicates=_self.label_stats.duplicates)}

    @staticmethod
    def get_filenames(data_dir):
        """
        Get corresponding filenames at root directory

        Returns
        -------
        tuple
            A tuple of two filename lists ('images' and 'labels')
        """
        images_path = os.path.join(data_dir, 'images')
        labels_path = os.path.join(data_dir, 'labels')

        image_filenames = os.listdir(images_path)
        label_filenames = os.listdir(labels_path)

        return image_filenames, label_filenames

    def get_matching(_self, garbage):
        """
        Match images and labels

        Returns
        -------
        dict
            Matching statistics with matched and unmatched categories
        """

        image_trash, label_trash = garbage['images'], garbage['labels']

        # filenames without extension
        image_names = set([get_name(image) for image in _self.image_filenames if
                           image not in itertools.chain(*image_trash.values())])
        label_names = set([get_name(label) for label in _self.label_filenames if
                           label not in itertools.chain(*label_trash.values())])

        lonely_images = image_names - label_names
        lonely_labels = label_names - image_names

        matched_images = image_names - lonely_images
        matched_labels = label_names - lonely_labels

        matched_images = complete_with_ext(os.path.join(_self.data_path, 'images'),
                                           matched_images)
        matched_labels = complete_with_ext(os.path.join(_self.data_path, 'labels'),
                                           matched_labels)
        lonely_images = complete_with_ext(os.path.join(_self.data_path, 'images'),
                                          lonely_images)
        lonely_labels = complete_with_ext(os.path.join(_self.data_path, 'labels'),
                                          lonely_labels)

        return {'Matched images': sorted(matched_images),
                'Matched labels': sorted(matched_labels),
                'Lonely images': lonely_images,
                'Lonely labels': lonely_labels}

    def clear_cache(self):
        self.get_layout_stats.clear()


class Annotations:
    """
    Class to manage and analyze annotations

    Parameters
    ----------
    data_path : str
       Path to the root directory containing the data

    labels : list of str
       List of annotation filenames to be processed.

    labelmap : dict
       A dictionary mapping class IDs to class names
    """

    def __init__(self, data_path, labels, labelmap):
        self.data_path = data_path
        self.labelmap = labelmap
        self.labels = labels
        self.corrupted = []
        self.yolo = []
        self.voc = []
        self.background = []

    @st.cache_data(show_spinner=False)
    def categorize_by_formats(_self):
        """
        Check annotation files for corruption and categorize them

        Returns
        -------
        dict
           A dictionary with categorized annotations
        """
        for label in _self.labels:
            check_correct = check_yolo if label.endswith('.txt') else check_voc
            bucket = _self.yolo if label.endswith('.txt') else _self.voc
            check_empty = check_yolo_empty if label.endswith('.txt') else check_voc_empty

            okay = check_correct(os.path.join(_self.data_path, 'labels', label))
            empty = check_empty(os.path.join(_self.data_path, 'labels', label))
            if okay:
                if empty:
                    _self.background.append(label)
                bucket.append(label)
            else:
                _self.corrupted.append(label)

        return {'yolo': _self.yolo,
                'voc': _self.voc,
                'corrupted': _self.corrupted,
                'background': _self.background}

    def bring_to(self, annotation_format_stats, destination_format, matching_dict):
        """
        Convert annotations from one format to another (YOLO <-> VOC)

        Parameters
        ----------
        annotation_format_stats : dict
           A dictionary containing lists of filenames categorized by format.

        destination_format : str
           The format to which annotations should be converted ('yolo' or 'voc').

        matching_dict : dict
           A dictionary mapping annotation filenames to corresponding image filenames.

        Returns
        -------
        list of str
           A list of annotation filenames that could not be converted due to missing corresponding images.
        """
        convert = voc_to_yolo if destination_format == 'yolo' else yolo_to_voc
        write = write_yolo if destination_format == 'yolo' else write_voc
        bucket = annotation_format_stats['voc'] if destination_format == 'yolo' else annotation_format_stats['yolo']

        not_converted = []
        for label in stqdm(bucket, desc="Converting...   "):
            if label not in matching_dict.keys():
                not_converted.append(label)  # without corresponding image
                continue
            image_path = os.path.join(self.data_path, 'images', matching_dict[label])
            label_path = os.path.join(self.data_path, 'labels', label)

            converted_annotation, destination = convert(label_path, self.labelmap, image_path)
            write(converted_annotation, destination)
            os.remove(label_path)

        return not_converted

    @st.cache_data(show_spinner=False)
    def get_stats(_self):
        """
        Generate a DataFrame of annotation statistics

        Returns
        -------
        pandas.DataFrame
            A pandas DataFrame of annotation statistics
        """

        yolo_instances = []
        for yolo_annotation in _self.yolo:
            with open(os.path.join(_self.data_path, 'labels', yolo_annotation), 'r') as f:
                lines = f.read().splitlines()
                for line in lines:
                    instance = line.strip().split(' ')
                    instance.insert(0, yolo_annotation)
                    yolo_instances.append(instance)

        instances = yolo_instances
        for voc_annotation in _self.voc:
            voc_instances = voc_to_yolo(os.path.join(_self.data_path, 'labels', voc_annotation),
                                        _self.labelmap)[0]
            for instance in voc_instances:
                instance.insert(0, voc_annotation)
            instances += voc_instances

        stats = pd.DataFrame(instances, columns=configs.ANNOTATION_STATS_COLUMNS)
        stats = stats.astype({'x_center': float, 'y_center': float, 'width': float, 'height': float})
        stats['box_size'] = stats['width'] * stats['height']

        stats['class_name'] = stats['object_class']
        # if labelmap detected replace IDs with corresponding labels
        if _self.labelmap:
            stats['class_name'] = stats['object_class'].apply(lambda x: _self.labelmap[str(x)])

        return stats


class Images:
    """
    Class to manage and analyze images

    Parameters
    ----------
    data_path : str
       Path to the root directory containing the data

    images : list of str
       List of image filenames to be processed.

    annotation_stats : pandas.DataFrame
       Output of Annotations.get_stats method
    """

    def __init__(self, data_path, images, annotation_stats):
        self.data_path = data_path
        self.image_paths = [os.path.join(data_path, 'images', image) for image in images]
        self.annotation_stats = annotation_stats
        self.verified_paths = list(itertools.compress(self.image_paths, self.verify()))
        self.n_images = len(images)

    @st.cache_data(show_spinner=False)
    def verify(_self):
        verified = [check_image(image_path) for image_path in _self.image_paths]
        return verified

    def get_format_counts(self):
        """
        Check image files for corruption and categorize them

        Returns
        -------
        dict
            A dictionary of image format statistics
        """
        extensions = [get_ext(path.split('/')[-1]) for path in self.verified_paths]
        extensions.extend(['corrupted'] * (self.n_images - len(self.verified_paths)))  # corrupted if not verified
        return dict(Counter(extensions))

    @staticmethod
    def process_image(image_path):
        """
        Process a single image to extract various properties.

        Parameters
        ----------
        image_path : str
            The file path of the image to be processed.

        Returns
        -------
        list
            A list of extracted properties
        """

        image_array = cv2.imread(image_path)
        height, width, channels = image_array.shape

        image_gray = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)

        # extracting contrast
        contrast_rms = image_gray.std()

        # extracting color distribution
        color_distribution = get_color_distribution(image_array)
        # getting rid of color names
        color_distribution = list(itertools.chain(*color_distribution.values()))

        # extracting image brightness
        brightness = np.mean(image_gray) / 255 * 100

        # extracting image sharpness
        gy, gx = np.gradient(image_gray)
        sharpness = np.sqrt(gx ** 2 + gy ** 2).mean() / 255 * 100

        image_props = [image_path, height, width, channels,
                       contrast_rms, brightness, sharpness]

        # color_distribution is a list of size 28 <-> 7(colors)x4(c,h,s,v)
        image_props.extend(color_distribution)

        return image_props

    @st.cache_data(show_spinner=False)
    def get_stats(_self, sample_size):
        """
        Analyze a random sample of images to gather detailed statistics on image properties.

        Parameters
        ----------
        sample_size : int
            The number of images to use

        Returns
        -------
        pandas.DataFrame
            A DataFrame containing the extracted image statistics
        """

        n_colors = 6
        n_overalls, n_stats = len(configs.IMAGE_STATS_OVERALL_COLUMNS), len(configs.IMAGE_STATS_COLOR_COLUMNS)

        index_level_0 = ['overall'] * n_overalls + [color for color in configs.SIX_COLORS for _ in range(n_stats)]
        index_level_1 = configs.IMAGE_STATS_OVERALL_COLUMNS + configs.IMAGE_STATS_COLOR_COLUMNS * n_colors

        # multilevel(2) columns to separate overall properties from color stats
        print(index_level_0, index_level_1)
        print(len(index_level_0), len(index_level_1))
        columns = pd.MultiIndex.from_arrays([index_level_0, index_level_1])

        sampled_paths = random.sample(_self.verified_paths, sample_size)

        with Pool(os.cpu_count()) as p:
            # noinspection PyTypeChecker
            image_stats = list(stqdm(p.imap(_self.process_image, sampled_paths), total=sample_size,
                                     desc="Scanning images...   "))

        image_stats = pd.DataFrame(image_stats, columns=columns)
        image_stats = image_stats.sort_values([('overall', 'filepath')])

        # merging with annotation_stats to connect images to the objects they contain
        annotations_key = _self.annotation_stats['filename'].apply(get_name)
        images_key = image_stats['overall']['filepath'].apply(lambda x: get_name(x.split('/')[-1]))
        combined = pd.merge(image_stats['overall'], _self.annotation_stats, left_on=images_key,
                            right_on=annotations_key, how='left')

        combined['class_name'] = combined['class_name'].fillna('background')

        # adding class-objects column to image-stats using combined DataFrame
        image_stats['overall', 'class_objects'] = combined.groupby('filepath')[
            'class_name'].unique().sort_index().values

        return image_stats

    @staticmethod
    @st.cache_data(show_spinner=False)
    def get_tones(image_stats):
        """
        Extract color tones using hsv

        Parameters
        ----------
        image_stats : pandas.DataFrame
            Output of Images.get_stats method

        Returns
        -------
        pandas.DataFrame
            A DataFrame containing the extracted color tones where each row represents a tone
        """
        color_cols = [c for (c, _, _) in configs.HUE_RANGES[:-1]]
        color_stats = image_stats.loc[:, color_cols].stack(level=0).droplevel(1)

        tones = color_stats.groupby(['hue', 'sat', 'value'])['count'].sum().sort_index()
        tones = tones.reset_index()

        # shrink tone counts into 1-100 range
        scaler = MinMaxScaler((1, 100))
        tones['count'] = scaler.fit_transform(tones['count'].values.reshape(-1, 1)).astype('int32')

        # Expand hue_tones using the counts
        tones = tones.loc[tones.index.repeat(tones['count'])].reset_index(drop=True)

        return tones

    @property
    def n_verified(self):
        return len(self.verified_paths)


class Overlaps:
    """
    Class to manage and analyze overlaps between objects

    Parameters
    ----------
    annotation_stats : pandas.DataFrame
       Output of Annotations.get_stats method
    """

    def __init__(self, annotation_stats):
        self.annotation_stats = annotation_stats.sort_values(['filename', 'class_name'])

    @property
    def n_verified(self):
        return self.annotation_stats['filename'].nunique()

    @staticmethod
    def calculate_overlap(pair_index, data):
        """
        Calculate the overlap area between 2 bounding boxes

        Parameters
        ----------
        pair_index : tuple
            A tuple containing the indices of the two bounding boxes to compare.

        data : pd.DataFrame
            The DataFrame containing the bounding box information for the images.

        Returns
        -------
        list
            A list containing two sublists with detailed information about the overlap between the two bounding boxes
        """
        index1, index2 = pair_index
        bbox1, bbox2 = data.loc[index1], data.loc[index2]

        # Calculate the distance between the centers
        dx = abs(bbox1.x_center - bbox2.x_center)
        dy = abs(bbox1.y_center - bbox2.y_center)

        # Calculate the overlap in each dimension
        overlap_width = max(0, bbox1.width / 2 + bbox2.width / 2 - dx)
        overlap_height = max(0, bbox1.height / 2 + bbox2.height / 2 - dy)

        # Calculate the area of each bounding box and the overlapping area
        overlap_size = min(bbox1.box_size, bbox2.box_size, overlap_width * overlap_height)

        # overlap info from the perspective of the first object
        relation = [bbox1.filename, bbox1.class_name, bbox2.class_name, index1, index2,
                    bbox1.box_size, bbox2.box_size, overlap_size, bbox1.x_center, bbox1.y_center,
                    bbox1.width, bbox1.height, bbox2.x_center, bbox2.y_center, bbox2.width, bbox2.height]

        # overlap info from the perspective of the second object
        reverse_relation = [bbox2.filename, bbox2.class_name, bbox1.class_name, index2, index1,
                            bbox2.box_size, bbox1.box_size, overlap_size, bbox2.x_center, bbox2.y_center,
                            bbox2.width, bbox2.height, bbox1.x_center, bbox1.y_center, bbox1.width, bbox1.height]

        return [relation, reverse_relation]

    @st.cache_data(show_spinner=False)
    def get_stats(_self, sample_size):
        """
        Sample a subset of images and compute the overlap statistics for all pairs of bounding boxes

        Parameters
        ----------
        sample_size : int
            The number of unique image filenames to sample and analyze.

        Returns
        -------
        pd.DataFrame
            A DataFrame containing the overlap statistics for the sampled images
        """

        sampled_filenames = random.sample(_self.annotation_stats['filename'].unique().tolist(), sample_size)
        sampled_annotations = _self.annotation_stats[_self.annotation_stats['filename'].isin(sampled_filenames)]

        calculate_overlap_data = partial(_self.calculate_overlap, data=sampled_annotations)
        grouped = sampled_annotations.groupby('filename')

        # Create pairwise indices
        combinations = [list(itertools.combinations(group.index.values, 2)) for _, group in grouped]
        pairwise_indices = list(itertools.chain.from_iterable(combinations))

        cpu_count = os.cpu_count()
        with Manager():
            pbar = stqdm(total=len(pairwise_indices))
            with Pool(cpu_count) as p:
                overlaps = []
                for result in p.imap_unordered(calculate_overlap_data, pairwise_indices, chunksize=20 * cpu_count):
                    overlaps.extend(result)
                    pbar.update()

            pbar.close()

        overlap_stats = pd.DataFrame(overlaps, columns=configs.OVERLAP_STATS_COLUMNS)
        overlap_stats['size'] = sample_size  # number of images attached to overlap stats

        return overlap_stats


def render_layout(session_state, layout_stats, matching, delete=False):
    """
    Render layout configuration

    Parameters
    ----------
    session_state: st.session_state
        Current session_state
    layout_stats: dict
        Output of DataMatch.get_layout_stats method
    matching: dict
        Output of DataMatch.get_matching method
    delete: bool
        Delete if True, separate if false
    """

    for category in configs.CATEGORIES: # labels and images
        for attr, attr_short, attr_short_remove in zip(configs.DATAMATCH_ATTRIBUTES, configs.DATAMATCH_ATTRIBUTES_SHORT,
                                                       configs.DATAMATCH_ATTRIBUTES_SHORT_REMOVE):

            if not layout_stats[category][attr]: # if count for attr is 0
                continue
            if session_state[attr_short_remove]: # if attr is set to be removed
                destination = os.path.join(session_state['data_path'], f'{attr_short}_{category}')
                for filename in layout_stats[category][attr]:
                    if delete:
                        # removing altogether
                        os.remove(os.path.join(session_state['data_path'], category, filename))
                    else:
                        os.mkdir(destination)
                        # moving to destination
                        os.replace(os.path.join(session_state['data_path'], category, filename),
                                   os.path.join(destination, filename))

        if session_state['remove_lnl']: # if lonely files are to be removed
            if not matching[f'Lonely {category}']:
                continue
            destination = os.path.join(session_state['data_path'], f'lonely_{category}')
            condemned = matching[f'Lonely {category}']
            for filename in condemned:
                if delete:
                    os.remove(os.path.join(session_state['data_path'], category, filename))
                else:
                    os.mkdir(destination)
                    # moving to destination
                    os.replace(os.path.join(session_state['data_path'], category, filename),
                               os.path.join(destination, filename))


def add_background_labels(data_path, layout_stats, matching, actual_fill=True):
    """
    Add empty files as background labels

    Parameters
    ----------
    data_path: str
        Path to the root directory containing the data
    layout_stats: dict
        Output of DataMatch.get_layout_stats method
    matching: dict
        Output of DataMatch.get_matching method
    actual_fill: bool
        A boolean flag indicating whether to actually add the background labels or just return file names
    """

    # find most common extension (annotation format)
    extensions = [get_ext(f) for f in layout_stats['labels']['Correct']]
    extension_counts = Counter(extensions)
    most_common_ext = extension_counts.most_common(1)[0][0]

    destinations = []
    if actual_fill:
        get_empty_annotation = empty_yolo if most_common_ext == 'txt' else empty_voc
        write = write_yolo if most_common_ext == 'txt' else write_voc

        for filename in matching['Lonely images']:
            annotation, destination = get_empty_annotation(filename, data_path)
            write(annotation, destination)
            destinations.append(destination)

        return
    return [os.path.basename(destination) for destination in destinations]
