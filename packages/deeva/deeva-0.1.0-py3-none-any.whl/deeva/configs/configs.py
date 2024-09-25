import mimetypes
import random

import numpy as np
from screeninfo import get_monitors

from .utils import add_caching_vars, get_image_uri

import os
# setting working dir for entire project
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# main st.session_state vars
PARAMS_DEFAULT = dict(
    data_path=None,
    files_pref=None,
    remove_no_ext=False,
    remove_wf=False,
    remove_dp=False,
    remove_lnl=False,
    toggle_no_ext=False,
    toggle_wf=False,
    toggle_dp=False,
    toggle_lnl=False,
    toggle_mbg=False,
    render_final=False,
    choose_fp=None,
    remove_mbg=False,
    pass_forward=None,
    warning=None,
    show_warning=True,
    labelmap=None,
    stats_selectbox_backup=None,
    annotations_class_selectbox_backup=None,
    plot_type_selectbox_backup=None,
    images_class_selectbox_backup=None,
    images_include_selectbox_backup=None,
    medium_low_backup=None,
    medium_high_backup=False,
    box_size_slider_backup=None,
    convert_final=False,
    overlaps_inpute_page=True,
    overlaps_n_cases_backup=3,
    overlaps_n_images_backup=3,
    overlaps_object1_selectbox_backup=None,
    overlaps_object2_selectbox_backup=None,
)

PARAMS_DEFAULT_ANNOTATIONS = dict(
    medium_low=1,
    medium_high=2,
    box_size_slider=(0.0, 100.0)
)

# PARAMS_DEFAULT_OVERLAPS =

CATEGORIES = ['images', 'labels']
DATAMATCH_ATTRIBUTES_SHORT = ['no_ext', 'wrong_format', 'duplicates']
DATAMATCH_ATTRIBUTES_SHORT_REMOVE = ['remove_no_ext', 'remove_wf', 'remove_dp']
DATAMATCH_ATTRIBUTES_SHORT_TOGGLE = ['toggle_no_ext', 'toggle_wf', 'toggle_dp']
DATAMATCH_ATTRIBUTES = ['No extension', 'Wrong format', 'Duplicates by filename']


# set of all common extensions for all types of files
COMMON_EXTENSIONS = set()
for ext, _ in mimetypes.types_map.items():
    COMMON_EXTENSIONS.add(ext.split('.')[-1].lower())

# screen width and height
import os
if not os.getenv("DISPLAY"):  # Check if DISPLAY is set (useful for Linux)
    print("No display detected, running in headless mode.")
    VH, VW = 1080, 1920  # Handle appropriately for headless mode
else:
    monitor = get_monitors()[0]
    VW = monitor.width
    VH = monitor.height

# allowed extensions
IMAGE_EXTENSIONS = ('png', 'jpg', 'jpeg')
LABEL_EXTENSIONS = ('txt', 'xml')

# adding variables to PARAMS_DEFAULT for data caching
PARAMS_DEFAULT = add_caching_vars('images', PARAMS_DEFAULT)
PARAMS_DEFAULT = add_caching_vars('overlaps', PARAMS_DEFAULT)

# all backup vars from PARAMS_DEFAULT
BACKUPS = {k: v for k, v in PARAMS_DEFAULT.items() if k.endswith('_backup')}

# aliases to search for a labelmap more efficiently
LABELMAP_ALIASES = ['labelmap.txt', 'classes.txt', 'mapping.txt', 'label_classes.txt']

# assigned to classes
CLASS_COLORS = [
    "#E53935",  # Red
    "#1E88E5",  # Blue
    "#43A047",  # Green
    "#FDD835",  # Yellow
    "#8E24AA",  # Purple
    "#F57C00",  # Orange
    "#00796B",  # Teal
    "#C2185B",  # Pink
    "#0288D1",  # Light Blue
    "#D32F2F",  # Dark Red
    "#7B1FA2",  # Deep Purple
    "#FBC02D",  # Amber
]
random.shuffle(CLASS_COLORS)

# hue values separated into ranges
HUE_RANGES = [
    ("red", 0, 15),
    ("yellow", 15, 30),
    ("green", 30, 75),
    ("cyan", 75, 95),
    ("blue", 95, 140),
    ("pink", 140, 165),
    ("red", 165, 180),
]


SIX_COLORS = {k: v for k, v in zip(sorted((color for (color, _, _) in HUE_RANGES)), range(7))}
SIX_COLORS_REV = {k: v for v, k in SIX_COLORS.items()}
SIX_COLORS_MEAN = {k: (range_start + range_end) * .5 for (k, range_start, range_end) in HUE_RANGES}
SIX_COLORS_MEAN["red"] = 0

# Create a lookup table
HUE_RANGES_LOOKUP = np.empty(181, dtype=object)
for (color, min_hue, max_hue) in HUE_RANGES:
    HUE_RANGES_LOOKUP[min_hue:max_hue + 1] = SIX_COLORS[color]

# pd.DataFrame column names for different stats
IMAGE_STATS_COLOR_COLUMNS = ['count', 'hue', 'sat', 'value']
IMAGE_STATS_OVERALL_COLUMNS = ['filepath', 'height', 'width', 'n_channels',
                               'RMS_contrast', 'brightness', 'sharpness']
ANNOTATION_STATS_COLUMNS = ['filename', 'object_class', 'x_center',
                            'y_center', 'width', 'height']
OVERLAP_STATS_COLUMNS = ['filename', 'relate', 'relate_with', 'relate_index',
                         'with_index', 'relate_size', 'with_size', 'overlap_size',
                         'relate_x', 'relate_y', 'relate_w', 'relate_h', 'with_x',
                         'with_y', 'with_w', 'with_h']

# base64 Data URIs of corresponding images
URI = {'main_background': get_image_uri('assets/backgrounds/main.png'),
       'black_background': get_image_uri('assets/backgrounds/black.png'),
       'astronaut': get_image_uri('assets/other/astronaut.png'),
       'app': get_image_uri('assets/other/app.png'),
       'disk': get_image_uri('assets/other/disk.png'),
       'bin': get_image_uri('assets/other/hole.png'),
       'blue_planet': get_image_uri('assets/planets/blue.png'),
       'green_planet': get_image_uri('assets/planets/green.jpg'),
       'moon_planet': get_image_uri('assets/planets/moon.jpg'),
       'purple_planet': get_image_uri('assets/planets/purple.png'),
       'red_planet': get_image_uri('assets/planets/red.png'),
       }

HELP_DATA_PATH = (
    "- **Data must be organized into two folders \"images\" and \"labels\"**\n"
    "- **Supports YOLO and PASCAL VOC formats for labels**\n"
    "- **Also provide labelmap for better experience**"
)

HELP_MARK_BACKGROUNDS = '**If rendered will create empty labels for all lonely images**'

HELP_STRATEGY_SELECTBOX = """
                **Image Assigning Strategy**

                - **All**: All images having at least one instance of a specific class will be treated as images of that class.
                - **Most frequent**: If the specific class is the most frequent class in an image, the image is treated as an image of that class.
                """

CAPTIONS_FILES_PREF = ['***Move to distinct folders*** 🗃️',
                       '***Delete from source*** :wastebasket:']

CAPTIONS_CONVERT = ["Convert all annotations to VOC format",
                    "Convert all annotations to YOLO format"]

TOAST_NUMBER_INPUTS = '**Invalid thresholds. low > high**'


ROLL_CONFIGS = dict(x=[29,26,26,26,26],
                     y=[77,73,73,73,73],
                     radius=[-33.5, -45, -55, -65, -75],
                     size=[3.7, 4.7, 5.3, 6.6, 7.4],
                     cruise_time=[30, 60, 90, 120, 180],
                     rotation_time=[3, 5, 7, 10, 15],
                     key=['blue_planet', 'red_planet', 'moon_planet', 'green_planet', 'purple_planet'])

# supply.html path parameters
D1 = ("M 250,0 L 250,90 S 250,190 300.0,190 L 390,190", "M240,0 a-10,10 0 0,0 20,0")
D2 = ("M 160,0 L 160,220 S 160,320 115.0,320 L 10,320", "M150,0 a-10,10 0 0,0 20,0")
