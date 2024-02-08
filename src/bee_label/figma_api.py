import requests
from bee_label.enums import JarSize


def get_nodes_ids(figma_token: str)->dict[JarSize,dict[str,str]]:
    URL = 'https://api.figma.com/v1/files/IBkWSq4skreUO6bYFvAIXY/nodes?ids=969-3227,970-4380,970-4038&depth=1'

    response = requests.get(URL, headers={'X-FIGMA-TOKEN': figma_token})
    nodes = response.json()
    nodes_id = {JarSize.SMALL: "970:4380", JarSize.MEDIUM: "969:3227", JarSize.LARGE: "970:4038"}
    children_ids = {}

    for size, node_id in nodes_id.items():
        children_ids[size] = {}
        for children in nodes["nodes"][node_id]["document"]["children"]:
            children_ids[size][children["name"]] = children["id"]

    return children_ids

def get_image(figma_token: str, node_id: str)->bytes:
    URL = f'https://api.figma.com/v1/images/IBkWSq4skreUO6bYFvAIXY?ids={node_id}&format=svg'
    response = requests.get(URL, headers={'X-FIGMA-TOKEN': figma_token})
    image_data = requests.get(response.json()['images'][node_id]).content
    return image_data
