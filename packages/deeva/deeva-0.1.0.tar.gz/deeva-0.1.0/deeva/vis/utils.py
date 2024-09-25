import io
from PIL import Image
import numpy as np
import cv2


def crop_solid_edges(im_arr):
    """
    :param im_arr: Input image array.
    :return: Cropped image array with solid edges removed.
    """
    gray = cv2.cvtColor(im_arr, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)

    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnt = contours[0]
    x, y, w, h = cv2.boundingRect(cnt)

    crop = im_arr[y:y + h, x:x + w]

    return crop

def generate_proportional_centroids(n):
    """
    :param n: Number of centroids to generate.
    :return: A numpy array containing the coordinates of the centroids.
    """
    if n == 1:
        return np.array([[0.5, 0.5]])  # Only one centroid at the center of the range [0, 1]

    # Generate (n-1)-sided polygon vertices with radius 0.5 and center at (0.5, 0.5)
    vertices = []
    angles = np.linspace(0, 2 * np.pi, n - 1, endpoint=False)
    for angle in angles:
        x = 0.5 + 0.5 * np.cos(angle)
        y = 0.5 + 0.5 * np.sin(angle)
        vertices.append((x, y))

    # Add the center
    vertices.append((0.5, 0.5))

    return np.array(vertices)


def make_symmetrical(im_arr):
    """
    :param im_arr: Input numpy array representing an image.
    :return: Symmetrical image as a numpy array, concatenated with its flipped version.
    """
    im_flip = cv2.flip(im_arr, 1)
    return np.concatenate((im_arr, im_flip), axis=1)

def get_planet_texture(im_arr):
    """
    :param im_arr: The input image array representing the planet's surface.
    :return: A square image array with symmetrical texture and cropped solid edges.
    """
    cropped = crop_solid_edges(im_arr)
    symmetrical = make_symmetrical(cropped)

    h, w = im_arr.shape[:2]
    square = cv2.resize(symmetrical, (h, h))

    return square

def overlap_area(d, r1, r2):
    """
    :param d: Distance between the centers of the two circles.
    :param r1: Radius of the first circle.
    :param r2: Radius of the second circle.
    :return: The area of overlap between the two circles.
    """
    if d >= r1 + r2:
        return 0
    elif d <= abs(r1 - r2):
        return np.pi * min(r1, r2)**2
    else:
        part1 = r1**2 * np.arccos((d**2 + r1**2 - r2**2) / (2 * d * r1))
        part2 = r2**2 * np.arccos((d**2 + r2**2 - r1**2) / (2 * d * r2))
        part3 = 0.5 * np.sqrt((-d + r1 + r2) * (d + r1 - r2) * (d - r1 + r2) * (d + r1 + r2))
        return part1 + part2 - part3


def solve_distance(d, r1, r2, overlap):
    """
    :param d: distance between the centers of the two circles
    :param r1: radius of the first circle
    :param r2: radius of the second circle
    :param overlap: known overlap area between the two circles
    :return: the difference between the calculated overlap area and the known overlap area
    """
    return overlap_area(d, r1, r2) - overlap


def plotly_fig2array(fig):
    """
    :param fig: Input Plotly figure to be converted to a NumPy array.
    :type fig: plotly.graph_objs._figure.Figure
    :return: Image represented as a NumPy array.
    :rtype: numpy.ndarray
    """
    fig_bytes = fig.to_image(format="png")
    buf = io.BytesIO(fig_bytes)
    img = Image.open(buf)
    return np.asarray(img)


def adjust_annotations(x, y, w, h, aggregate_x, aggregate_y, aggregate_w, aggregate_h):
    """
    :param x: X-coordinate of the annotation.
    :param y: Y-coordinate of the annotation.
    :param w: Width of the annotation.
    :param h: Height of the annotation.
    :param aggregate_x: X-coordinate of the aggregate area.
    :param aggregate_y: Y-coordinate of the aggregate area.
    :param aggregate_w: Width of the aggregate area.
    :param aggregate_h: Height of the aggregate area.
    :return: Adjusted annotation coordinates and dimensions as a tuple (x_new, y_new, w_new, h_new).
    """
    x_new = 0.5 - (aggregate_x - x) / aggregate_w
    y_new = 0.5 - (aggregate_y - y) / aggregate_h

    w_new = w / aggregate_w
    h_new = h / aggregate_h

    return x_new, y_new, w_new, h_new

def get_rect_vertices(img, x, y, w, h):
    """
    :param img: Input image in the form of a NumPy array.
    :param x: x coordinate of the top-left corner of the bounding box as a relative value (0 to 1).
    :param y: y coordinate of the top-left corner of the bounding box as a relative value (0 to 1).
    :param w: Width of the bounding box as a relative value (0 to 1).
    :param h: Height of the bounding box as a relative value (0 to 1).
    :return: Two lists, x_rect and y_rect, containing the x and y coordinates of the vertices of the rectangle.
    """
    img_h, img_w = img.shape[:2]
    x_min, y_min, x_max, y_max = xywh2xyxy(x, y, w, h)

    x_rect = [x_min, x_max, x_max, x_min, x_min]
    y_rect = [y_max, y_max, y_min, y_min, y_max]

    x_rect = [v * img_w for v in x_rect]
    y_rect = [v * img_h for v in y_rect]

    return x_rect, y_rect


def get_aggregate_box(x1, y1, w1, h1, x2, y2, w2, h2):
    """
    :param x1: x-coordinate of the center of the first box
    :param y1: y-coordinate of the center of the first box
    :param w1: width of the first box
    :param h1: height of the first box
    :param x2: x-coordinate of the center of the second box
    :param y2: y-coordinate of the center of the second box
    :param w2: width of the second box
    :param h2: height of the second box
    :return: Aggregate box as a tuple (aggregate_x, aggregate_y, aggregate_w, aggregate_h)
    """
    left1, bottom1, right1, top1 = xywh2xyxy(x1, y1, w1, h1)
    left2, bottom2, right2, top2 = xywh2xyxy(x2, y2, w2, h2)

    aggregate_left = min(left1, left2)
    aggregate_right = max(right1, right2)
    aggregate_top = max(top1, top2)
    aggregate_bottom = min(bottom1, bottom2)

    aggregate_w = aggregate_right - aggregate_left
    aggregate_h = aggregate_top - aggregate_bottom
    aggregate_x = (aggregate_left + aggregate_right) / 2
    aggregate_y = (aggregate_bottom + aggregate_top) / 2

    return aggregate_x, aggregate_y, aggregate_w, aggregate_h


def xywh2xyxy(x, y, w, h):
    """
    :param x: The x-coordinate of the center of the box
    :param y: The y-coordinate of the center of the box
    :param w: The width of the box
    :param h: The height of the box
    :return: A tuple containing the coordinates of the top-left and bottom-right corners (x_min, y_min, x_max, y_max)
    """
    x_min = x - w / 2
    x_max = x + w / 2
    y_min = y - h / 2
    y_max = y + h / 2
    return x_min, y_min, x_max, y_max


def hex_to_rgba(hex_color, alpha, factor=1):
    """
    :param hex_color: Hexadecimal color string (e.g., "#RRGGBB").
    :param alpha: Alpha value for the RGBA color (0.0 to 1.0).
    :param factor: Multiplication factor for the RGB values (default is 1).
    :return: RGBA color string in the format 'rgba(R, G, B, A)'.
    """
    hex_color = hex_color.lstrip('#')
    rgb = tuple(int(hex_color[i:i+2], 16) * factor for i in (0, 2, 4))
    return f'rgba({rgb[0]}, {rgb[1]}, {rgb[2]}, {alpha})'


def crop_aggregate_box(img, pair, padding=0.1, square=False):
    """
    Crop the aggregate bounding box for a pair of boxes

    :param img: The input image represented as a NumPy array.
    :param pair: An object containing bounding box annotations
    :param padding: A float representing the amount of padding to be added around the aggregate bounding box
    :param square: A boolean indicating whether to force the bounding box to be square. Default is False.
    :return: A tuple containing the cropped image and the updated pair with adjusted bounding box annotations.
    """
    img_height, img_width = img.shape[:2]

    bbox1 = (pair.relate_x, pair.relate_y, pair.relate_w, pair.relate_h)
    bbox2 = (pair.with_x, pair.with_y, pair.with_w, pair.with_h)

    aggregate_x, aggregate_y, aggregate_w, aggregate_h = get_aggregate_box(*bbox1, *bbox2)
    if square:
        aggregate_w = aggregate_h = max(aggregate_w, aggregate_h)

    padding_left = min((aggregate_x - aggregate_w/2), padding/2)
    padding_right = min(1 - (aggregate_x + aggregate_w/2), padding/2)
    padding_bottom = min((aggregate_y - aggregate_h/2), padding/2)
    padding_top = min(1 - (aggregate_y + aggregate_h/2), padding/2)

    padding_w = padding_left + padding_right
    padding_h = padding_bottom + padding_top

    # Convert normalized coordinates to pixel coordinates
    left = int((aggregate_x - aggregate_w/2 - padding_left) * img_width)
    right = int((aggregate_x + aggregate_w/2 + padding_right) * img_width)
    bottom = int((aggregate_y - aggregate_h/2 - padding_bottom) * img_height)
    top = int((aggregate_y + aggregate_h/2 + padding_top) * img_height)

    # Perform the crop
    cropped_img = img[bottom:top, left:right]

    aggregates = (aggregate_x + (padding_right - padding_left)/2, aggregate_y + (padding_top - padding_bottom)/2,
                  aggregate_w + padding_w, aggregate_h + padding_h)

    pair.loc[['relate_x', 'relate_y', 'relate_w', 'relate_h']] = adjust_annotations(*bbox1, *aggregates)
    pair.loc[['with_x', 'with_y', 'with_w', 'with_h']] = adjust_annotations(*bbox2, *aggregates)

    return cropped_img, pair