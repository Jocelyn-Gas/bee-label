
from pathlib import Path

import bpy
from bee_label.color_manipulation import hex_to_rgb
from bee_label.enums import JarSize


def change_background_color(hex_value: str) -> None:
    r, g, b = hex_to_rgb(hex_value)
    bpy.data.materials["Background"].node_tree.nodes["Principled BSDF"].inputs[0].default_value = (r,g,b, 1)

def change_honey_color(hex_value: str) -> None:
    r, g, b = hex_to_rgb(hex_value)
    bpy.data.materials["Miel"].node_tree.nodes["Principled BSDF"].inputs[0].default_value = (r,g,b, 1)

def change_label_texture(image_path: str, size: JarSize) -> None:
    material = bpy.data.materials.get(f"Etiquette_{size.value}")
    nodes = material.node_tree.nodes
    image_node = nodes.get("Texture pot")

    image_node.image = bpy.data.images.load(image_path)

def frame_jar(size:JarSize):
    match size:
        case JarSize.SMALL:
            bpy.context.scene.frame_current = 1
        case JarSize.MEDIUM:
            bpy.context.scene.frame_current = 2
        case JarSize.LARGE:
            bpy.context.scene.frame_current = 3

def render_image(
        jar_size: JarSize,
        background_color: str,
        honey_color: str,
        label_texture: str = "./label.png",
        samples: int = 10,
        output_path: str | Path = "./result.png",
    ) -> None:

    # Load the .blend file
    bpy.ops.wm.open_mainfile(filepath="./.assets/Generateur.blend")

    frame_jar(jar_size)
    change_background_color(background_color)
    change_honey_color(honey_color)
    change_label_texture(label_texture, jar_size)

    bpy.context.scene.render.filepath = bpy.path.relpath(output_path)
    bpy.context.scene.cycles.samples = samples
    bpy.ops.render.render(write_still=True)
