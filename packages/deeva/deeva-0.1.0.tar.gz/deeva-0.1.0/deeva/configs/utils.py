import streamlit as st
from PIL import Image
import base64
from io import BytesIO

def add_caching_vars(page_name, params):
    """
    :param page_name: The base name of the page for which caching variables need to be generated.
    :param params: A dictionary containing existing parameters that need to be merged with the caching variables.
    :return: A dictionary containing the generated caching variables merged with the provided parameters.
    """
    caching_vars = {
        f'{page_name}_input_page': True,
        f'{page_name}_sample_size': None,
        f'{page_name}_use_cached_backup': False,
        f'{page_name}_cache_backup': False,
        f'{page_name}_forget_cached_backup': False,
    }

    return {**caching_vars, **params}

@st.cache_data(show_spinner=False)
def get_image_uri(image, gray=False):
    """
    Return base64 data URI of an image

    :param image: Input image, either as a file path string or a numpy array
    :param gray: Boolean value to specify whether to convert the image to grayscale
    :return: Base64 encoded data URI of the image
    """
    if isinstance(image, str):
        img = Image.open(image)
    else:
        img = Image.fromarray(image)

    if gray:
        img = img.convert('LA')

    img_bytes = BytesIO()
    img.save(img_bytes, format='PNG')

    data_uri = base64.b64encode(img_bytes.getvalue()).decode()
    return data_uri