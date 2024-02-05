import argparse
import os
import sys
from pathlib import Path

import bpy


class ArgumentParserForBlender(argparse.ArgumentParser):
    def _get_argv_after_doubledash(self):
        try:
            idx = sys.argv.index("--")
            return sys.argv[idx+1:] # the list after '--'
        except ValueError as e: # '--' not in the list:
            return []

    def parse_args(self):
        return super().parse_args(args=self._get_argv_after_doubledash())

parser = ArgumentParserForBlender()

parser.add_argument("--output-folder",
                    help="Results subfolder path.")
parser.add_argument("--samples", type=int, default=50,
                    help="Number of desired quacks")
parser.add_argument("--background-color", type=str, default="D5D4CB", help="Background color in hex format (default: D5D4CB)")
parser.add_argument("--image", type=str, help="Image to apply to the jar")
args = parser.parse_args()

SUBFOLDER = args.output_folder
SAMPLES = args.samples
COLOR = args.background_color
IMAGE = args.image

def hex_to_rgb( hex: str ):
    hex_value = int(hex, 16)
    b = (hex_value & 0xFF) / 255.0
    g = ((hex_value >> 8) & 0xFF) / 255.0
    r = ((hex_value >> 16) & 0xFF) / 255.0
    return r, g, b

def change_background_color(hex_value: str):
    r, g, b = hex_to_rgb(hex_value)
    bpy.data.materials["Background"].node_tree.nodes["Principled BSDF"].inputs[0].default_value = (r,g,b, 1)

change_background_color(COLOR)

output_folder = Path("./images/sortie")/ SUBFOLDER
output_folder.mkdir(parents=True, exist_ok=True)


jar = bpy.context.scene.objects["Pot"]
# Get material

material = bpy.data.materials.get("pot_couvercle_etiquette")

if material is None:
    raise ValueError("Aucun matériau nommé 'pot_couvercle_etiquette' trouvé")

nodes = material.node_tree.nodes
image_node = nodes.get("Texture pot")

image_node.image = bpy.data.images.load(IMAGE)
img_folder, img_file = os.path.split(IMAGE)
img_name, img_ext = os.path.splitext(img_file)
bpy.context.scene.render.filepath = bpy.path.relpath(f"./images/sortie/{SUBFOLDER}/{img_name}.png")
bpy.context.scene.cycles.samples = SAMPLES
bpy.ops.render.render(write_still=True)
