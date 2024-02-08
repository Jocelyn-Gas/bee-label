from io import BytesIO
from pathlib import Path

import streamlit
from bee_label.enums import HoneyColor, JarSize
from bee_label.figma_api import get_image, get_nodes_ids
from bee_label.image_manipulation import render_svg_to_png, resize_svg
from bee_label.rendering import render_image
from PIL import Image

streamlit.title("Générateur d'images de pots de miel")
streamlit.write("Bienvenue dans le générateur d'images de pots de miel !")

def retrieve_node_ids():
    with streamlit.spinner("Récupération des identifiants des noeuds..."):
        return get_nodes_ids(streamlit.secrets["FIGMA_TOKEN"])
if "node_ids" not in streamlit.session_state:
    streamlit.session_state.node_ids = retrieve_node_ids()

streamlit.header("Taille de pot")
size: JarSize | None = streamlit.radio("Choisis une taille de pot", JarSize, format_func=lambda x: x.value)

streamlit.header("Couleurs")
honey_picked = streamlit.radio("Choisis une couleur de miel", HoneyColor, format_func=lambda x: x.name.lower().capitalize())
if honey_picked is None:
    raise ValueError("Aucune couleur de miel sélectionnée")

honey_color = streamlit.color_picker("Si besoin tu peux modifier la couleur", honey_picked.value)


background_color = streamlit.color_picker("Choisis une couleur de fond", "#FFFFFF")

streamlit.header("Etiquette")
streamlit.write("Pour la taille choisie, j'ai trouvé les etiquettes suivantes sur Figma")
picked = streamlit.radio("Choisis", list(streamlit.session_state.node_ids[size].keys()))

uploadedfile = streamlit.file_uploader("Sinon, ajoutes ta propre image", type=["svg"], accept_multiple_files=False)


if streamlit.button("Générer l'image"):

    if uploadedfile is None:
        with streamlit.spinner("Recupération de l'étiquette de Figma..."):
            image_bytes = get_image(streamlit.secrets["FIGMA_TOKEN"], streamlit.session_state.node_ids[size][picked])
    else:
        image_bytes= uploadedfile.read()

    with streamlit.spinner("Traitement de l'étiquette..."):
        image_bytes= image_bytes.decode('utf-8')
        image_bytes= resize_svg(image_bytes, 2048)
        render_svg_to_png(image_bytes, "./label.png")

    with streamlit.spinner("Génération de l'image finale..."):
        if size is None:
            raise ValueError("Aucune taille de pot sélectionnée")

        render_image(
            size,
            background_color.replace("#", ""),
            honey_color.replace("#", ""),
        )
try:
    image = Image.open("./result.png")
    streamlit.image(image)
    byte_io = BytesIO()
    data = image.save(byte_io, format="PNG")
    name = streamlit.text_input("Nom du miel pour le nom de l'image", honey_picked.name.lower().capitalize())
    streamlit.download_button(
        "Télécharger l'image",
        data=byte_io,
        file_name=f"{name}_{size.value}.png",
        mime="image/png",
    )


    Path("./label.png").unlink()
    Path("./result.png").unlink()

except FileNotFoundError:
    pass

#https://www.figma.com/file/IBkWSq4skreUO6bYFvAIXY/Le-Berger-Des-Abeilles?type=design&node-id=969-3228&mode=design&t=XSVTg6mFcvj3C7AO-4
#https://www.figma.com/file/IBkWSq4skreUO6bYFvAIXY/Le-Berger-Des-Abeilles?type=design&node-id=969-3260&mode=design&t=XSVTg6mFcvj3C7AO-4
