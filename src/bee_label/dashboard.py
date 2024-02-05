import os
from io import BytesIO
from pathlib import Path
from typing import Literal

import streamlit
from bee_label.rendering import render_image
from PIL import Image

streamlit.title("Générateur d'images de pots de miel")
streamlit.write("Bienvenue dans le générateur d'images de pots de miel !")
name = None
if uploadedfile := streamlit.file_uploader(
    "Charges une étiquette pour le pot de miel",
    type=["png", "jpg", "jpeg"],
    accept_multiple_files=False,
):

    name = os.path.join("./", uploadedfile.name)

    streamlit.write(uploadedfile.name)

    input_temp_path = Path(name)
    selected_image_name = input_temp_path.stem

    with open(name, "wb") as f:
        f.write(uploadedfile.getbuffer())

if name is None:
    streamlit.stop()

size: Literal["500g", "1kg"] | None = streamlit.radio("Choisis une taille de pot", ["500g", "1kg"])
background_color = streamlit.color_picker("Choisis une couleur de fond")

if streamlit.button("Générer l'image"):
    with streamlit.spinner("Génération de l'image..."):
        if size is None:
            raise ValueError("Aucune taille de pot sélectionnée")

        render_image(
            size,
            background_color.replace("#", ""),
            10,
            name,
        )
try:
    image = Image.open("./result.png")
    streamlit.image(image)
    byte_io = BytesIO()
    data = image.save(byte_io, format="PNG")
    streamlit.download_button(
        "Télécharger l'image",
        data=byte_io,
        file_name=f"{selected_image_name}_{size}.png",
        mime="image/png",
    )


    input_temp_path.unlink()
    Path("./result.png").unlink()

except FileNotFoundError:
    pass
