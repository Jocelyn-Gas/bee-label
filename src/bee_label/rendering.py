import os
from pathlib import Path
from typing import Literal

import bpy


def hex_to_rgb( hex: str ) -> tuple[float, float, float]:
    hex_value = int(hex, 16)
    b = (hex_value & 0xFF) / 255.0
    g = ((hex_value >> 8) & 0xFF) / 255.0
    r = ((hex_value >> 16) & 0xFF) / 255.0
    return r, g, b

def change_background_color(hex_value: str) -> None:
    r, g, b = hex_to_rgb(hex_value)
    bpy.data.materials["Background"].node_tree.nodes["Principled BSDF"].inputs[0].default_value = (r,g,b, 1)

def render_image(
        jar_size: Literal["500g", "1kg"],
        background_color: str,
        samples: int,
        image: str
    ) -> None:

    # Load the .blend file
    bpy.ops.wm.open_mainfile(filepath=f"./.assets/Generateur_{jar_size}.blend")

    SUBFOLDER = jar_size #args.output_folder
    SAMPLES = samples #args.samples
    COLOR = background_color #args.background_color

    IMAGE = "./result.png" #f"./images/sortie/{SUBFOLDER}/Thym.png"#args.image

    change_background_color(COLOR)

    material = bpy.data.materials.get("pot_couvercle_etiquette")

    if material is None:
        raise ValueError("Aucun matériau nommé 'pot_couvercle_etiquette' trouvé")

    nodes = material.node_tree.nodes
    image_node = nodes.get("Texture pot")

    image_node.image = bpy.data.images.load(image)

    bpy.context.scene.render.filepath = bpy.path.relpath("./result.png")
    bpy.context.scene.cycles.samples = SAMPLES
    bpy.ops.render.render(write_still=True)
