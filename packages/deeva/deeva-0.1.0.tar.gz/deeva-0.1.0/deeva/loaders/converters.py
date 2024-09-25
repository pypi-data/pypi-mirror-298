from .parsers import parse_voc, parse_yolo

from utils import get_name
from lxml import etree
from PIL import Image
import os


def yolo_to_voc(yolo_annotation, labelmap, image_path):
    """
    Convert YOLO annotation to VOC format

    :param yolo_annotation: path to YOLO annotation file
    :param labelmap: Dictionary mapping class indices to class names
    :param image_path: Path to the image file corresponding to the YOLO annotation
    :return: A tuple containing the parsed annotation tree and the destination filename for the VOC format XML file
    """
    img = Image.open(image_path)
    width, height = img.size
    depth = 3 if img.mode == 'RGB' else 1

    instances = parse_yolo(yolo_annotation, labelmap)

    annotation = etree.Element('annotation')
    etree.SubElement(annotation, 'folder').text = 'images'
    etree.SubElement(annotation, 'filename').text = os.path.basename(image_path)

    size = etree.SubElement(annotation, 'size')
    etree.SubElement(size, 'width').text = str(width)
    etree.SubElement(size, 'height').text = str(height)
    etree.SubElement(size, 'depth').text = str(depth)

    for instance in instances:
        obj_class = instance[0]
        if not labelmap:
            obj_class = int(obj_class)
        x_center, y_center, w, h = list(map(float, instance[1:]))

        xmin = int((x_center - w / 2) * width)
        ymin = int((y_center - h / 2) * height)
        xmax = int((x_center + w / 2) * width)
        ymax = int((y_center + h / 2) * height)

        xmin, xmax = (xmin - 1, xmax + 1) if xmin == xmax else (xmin, xmax)
        ymin, ymax = (ymin - 1, ymax + 1) if ymin == ymax else (ymin, ymax)

        xmin = max(0, xmin)
        xmax = min(xmax, width)
        ymin = max(0, ymin)
        ymax = min(ymax, height)

        obj = etree.SubElement(annotation, 'object')
        etree.SubElement(obj, 'name').text = obj_class
        bbox = etree.SubElement(obj, 'bndbox')
        etree.SubElement(bbox, 'xmin').text = str(xmin)
        etree.SubElement(bbox, 'xmax').text = str(xmax)
        etree.SubElement(bbox, 'ymin').text = str(ymin)
        etree.SubElement(bbox, 'ymax').text = str(ymax)

    tree = etree.ElementTree(annotation)
    destination = get_name(yolo_annotation) + '.xml'
    return tree, destination


def voc_to_yolo(voc_annotation, labelmap, *args):
    """
    Convert VOC annotation to YOLO format

    :param voc_annotation: Path to VOC annotation XML file
    :param labelmap: Dictionary mapping class names to class IDs
    :return: Tuple containing a list of YOLO-formatted annotations and the destination file name
    """
    tree = parse_voc(voc_annotation)
    root = tree.getroot()

    size = root.find('size')
    width = int(size.find('width').text)
    height = int(size.find('height').text)

    instances = []
    labelmap={v: k for k, v in labelmap.items()}
    for obj in root.iter('object'):
        obj_class = int(labelmap[obj.find('name').text])
        bbox = obj.find('bndbox')
        xmin = int(bbox.find('xmin').text)
        ymin = int(bbox.find('ymin').text)
        xmax = int(bbox.find('xmax').text)
        ymax = int(bbox.find('ymax').text)

        x_center = ((xmin + xmax) / 2) / width
        y_center = ((ymin + ymax) / 2) / height
        w = (xmax - xmin) / width
        h = (ymax - ymin) / height

        instance = [obj_class, x_center, y_center, w, h]
        instances.append(instance)

    destination = get_name(voc_annotation) + '.txt'
    return instances, destination




