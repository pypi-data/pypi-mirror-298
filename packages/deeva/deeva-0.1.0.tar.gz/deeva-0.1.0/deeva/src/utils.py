from collections import ChainMap, OrderedDict

import cv2
import numpy as np
import pandas as pd
from PIL import Image

from configs import configs
from utils import closest_odd


def image_resize(image, width=None, height=None, inter=cv2.INTER_AREA):
    """
    :param image: Input image to be resized.
    :param width: The desired width of the resized image
    :param height: The desired height of the resized image
    :param inter: Interpolation method used for resizing. Default is cv2.INTER_AREA.
    :return: Resized image.
    """
    (h, w, dim) = image.shape

    if width is None and height is None:
        return image

    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)

    elif height is None:
        r = width / float(w)
        dim = (width, int(h * r))

    resized = cv2.resize(image, dim, interpolation=inter)

    return resized


def generalize_by_hsv(hsv, sat_ranges, value_ranges):
    """
    Replace hue, saturation and value in the group with mean values

    :param hsv: An array of HSV color values.
    :param sat_ranges: A list of saturation ranges.
    :param value_ranges: A list of value ranges.
    :return: A dictionary with color as the key and a list containing count, hue generalizer,
             saturation generalizer, and value generalizer as the value.
    """
    combinations, combination_counts = np.unique(np.column_stack((hsv[:, 1], hsv[:, 2])),
                                                 return_counts=True, axis=0)
    most_frequent_combination = combinations[np.argmax(combination_counts)]
    most_frequent_sat_range, most_frequent_value_range = most_frequent_combination

    sat_generalizer = sat_ranges[most_frequent_sat_range: most_frequent_sat_range + 2].mean()
    value_generalizer = value_ranges[most_frequent_value_range: most_frequent_value_range + 2].mean()

    count = hsv.shape[0]
    color = configs.SIX_COLORS_REV[hsv[0][0]]
    hue_generalizer = configs.SIX_COLORS_MEAN[color]
    return {color: [count, hue_generalizer, sat_generalizer, value_generalizer]}


def get_color_distribution(im_arr, resize_to=150, blur_kernel_size=20):
    """
    Extract color statistics for a single image

    :param im_arr: Input image array in BGR format
    :type im_arr: numpy.ndarray

    :param resize_to: Target size to resize the image, maintaining the aspect ratio
    :type resize_to: int, optional

    :param blur_kernel_size: Kernel size for median blurring; must be an odd number
    :type blur_kernel_size: int, optional

    :return: Distribution of colors in the image, mapped and generalized into predefined ranges
    :rtype: OrderedDict
    """
    h, w = im_arr.shape[:2]
    if h > w:
        im_arr = cv2.rotate(im_arr, cv2.ROTATE_90_CLOCKWISE)

    target_width = min(resize_to, w)
    im_arr = image_resize(im_arr, width=target_width)

    kernel_size = closest_odd(blur_kernel_size)
    im_arr = cv2.medianBlur(im_arr, kernel_size)

    im_arr_hsv = cv2.cvtColor(im_arr, cv2.COLOR_BGR2HSV)
    im_arr_hsv = im_arr_hsv.reshape(-1, 3).astype('int16')

    generalize_by_hue = np.vectorize(lambda x: configs.HUE_RANGES_LOOKUP[x])

    im_arr_hsv[:, 0] = generalize_by_hue(im_arr_hsv[:, 0])
    im_arr_hsv[:, 1], sat_ranges = pd.cut(im_arr_hsv[:, 1], bins=10,
                                          right=False, labels=False, retbins=True)
    im_arr_hsv[:, 2], value_ranges = pd.cut(im_arr_hsv[:, 2], bins=10,
                                            right=False, labels=False, retbins=True)

    im_arr_hsv = im_arr_hsv[im_arr_hsv[:, 0].argsort()]

    color_groups = np.split(im_arr_hsv, np.unique(im_arr_hsv[:, 0], return_index=True)[1][1:])

    color_groups_generalized = ChainMap(*(generalize_by_hsv(group, sat_ranges, value_ranges)
                                          for group in color_groups))

    missing_colors = set(configs.SIX_COLORS.keys()) - set(color_groups_generalized.keys())
    missing_colors = {k: [np.nan] * 4 for k in missing_colors}

    color_distribution = OrderedDict(sorted({**color_groups_generalized, **missing_colors}.items()))

    return color_distribution


def check_image(img_path):
    """
    :param img_path: The path to the image file to be checked.
    :return: True if the file is a valid image, False otherwise.
    """
    try:
        with Image.open(img_path) as img:
            img.verify()
            return True
    except (IOError, SyntaxError):
        return False



