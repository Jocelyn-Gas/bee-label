import re
from functools import partial
from pathlib import Path
from re import Match

import cairosvg


def get_new_height(width:float, height:float, new_width:float) -> float:
    return (new_width * height) / width

def replace_numbers(_: Match, width:float=2048, height:float= 758.26):
    return f'<svg width="{width}" height="{height}"'

def render_svg_to_png(svg_string: str, output_path: str| Path):
    svg_bytes = svg_string.encode('utf-8')
    png_bytes = cairosvg.svg2png(bytestring=svg_bytes)

    if png_bytes is None:
        raise ValueError("Failed to convert SVG to PNG")

    with open(output_path, 'wb') as output_file:
        output_file.write(png_bytes)

def resize_svg(svg_string: str, new_width: float) -> str:
    pattern = r'<svg width="(\d+(\.\d+)?)?" height="(\d+(\.\d+)?)?"'
    if match := re.search(pattern, svg_string):
        width = match.group(1)
        height = match.group(3)

        new_height = get_new_height(float(width), float(height), new_width)
        modified_string = re.sub(pattern, partial(replace_numbers, width=new_width, height=new_height), svg_string)

        return modified_string

    raise ValueError("No width and height found in the SVG file")
