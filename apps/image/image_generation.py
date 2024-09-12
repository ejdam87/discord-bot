import requests
import io
from PIL import Image


API_URL = "https://api-inference.huggingface.co/models/CompVis/stable-diffusion-v1-4"

HELP_MSG = '!draw "describe what you want to draw"'
EMPTY_ERR = "Empty sequence provided!"


def query(payload, token: str) -> bytes:
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.content

def generate(description: str, token: str) -> io.BytesIO:
    image_bytes = query({"inputs": description}, token)
    image_bytes = io.BytesIO(image_bytes)
    return image_bytes
