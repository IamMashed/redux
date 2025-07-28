import io
from flask import current_app


def gen_static_map_url(pins, width=1123, height=794):
    """
    Generate mapbox static map url

    :param pins: A list of pins to display (subject, comparatives)
    :param width: The map default width
    :param height: The map default height
    """
    base_url = current_app.config.get('MAPBOX_URL')
    token = current_app.config.get('MAPBOX_TOKEN')
    style_id = current_app.config.get('MAPBOX_STYLE_ID')
    username = current_app.config.get('MAPBOX_USERNAME')

    pins_overlay = gen_pins_overlay(pins)
    return f'{base_url}/{username}/{style_id}/static/{pins_overlay}/auto/{width}x{height}?access_token={token}'


def gen_pins_overlay(pins):
    """
    Generate pins overlay
    """
    sbj_overlay = gen_subject_overlay(pins[0]['lon'], pins[0]['lat'])
    comps_overlay = ','.join([gen_comp_overlay(i, pins[i]['lon'], pins[i]['lat']) for i in range(1, len(pins))])

    return f'{sbj_overlay},{comps_overlay}'


def gen_subject_overlay(lon, lat):
    """
    Generate subject overlay
    """
    return f'pin-l-s+ff9900({lon},{lat})'


def gen_comp_overlay(pin_num, lon, lat):
    """
    Generate comparative overlay
    """
    return f'pin-l-{pin_num}+0099cc({lon},{lat})'


def get_mapbox_static_map(url, output_path=None):
    """
    Get mapbox static map

    :param output_path: Optional path where to save map on disk
    """
    from PIL import Image
    import requests
    from io import BytesIO

    response = requests.get(url)
    img = Image.open(BytesIO(response.content))

    if output_path:
        img.save(output_path)

    buffered = io.BytesIO()
    img.save(buffered, 'png')

    return buffered
