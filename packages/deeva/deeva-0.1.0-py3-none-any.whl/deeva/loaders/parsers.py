import os
import re
from lxml import etree

from configs import configs


def parse_yolo(annotation, labelmap):
    """
    Parse YOLO file

    :param annotation: Path to YOLO file
    :param labelmap: Dictionary to map label indices to label names
    :return: List of parsed YOLO annotations with label mapping applied
    """
    instances = []
    with open(annotation, 'r') as f:
        lines = f.read().splitlines()
        for line in lines:
            instance = line.strip().split(' ')
            instance = list(map(float, instance))
            instance[0] = int(instance[0])

            if labelmap:
                instance[0] = labelmap[str(instance[0])]

            instances.append(instance)
    return instances


def parse_voc(annotation):
    """
    Parse VOC file

    :param annotation: Path to VOC file
    :return: Parsed XML tree from the given VOC file.
    """
    tree = etree.parse(annotation)
    return tree


def get_labelmap(data_path):
    """
    Locate and parse labelmap from dir

    :param data_path: Path to the directory containing labelmap file
    :return: A dictionary representing the labelmap if correctly formatted;
        'Labelmap not found' if no valid labelmap file is found;
        'Incorrect labelmap' if the file content does not match the expected pattern.
    """

    labelmap_file=None
    label_pattern = r'^\S+$'

    root_dir = os.listdir(data_path)
    for alias in configs.LABELMAP_ALIASES:
        if alias in root_dir:
            labelmap_file = alias
            break
        return 'Labelmap not found'

    with open(os.path.join(data_path, labelmap_file), 'r') as f:
        lines = f.read().splitlines()

    if not all(re.match(label_pattern, line.strip()) for line in lines if line):
        return 'Incorrect labelmap'

    labelmap = {str(n): line.strip() for n, line in zip(range(len(lines)), lines)
                if re.match(label_pattern, line)}

    return labelmap