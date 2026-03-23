from PIL import Image
import torch
from torchvision import transforms


def load_image(image_path):

    image = Image.open(image_path)

    return image

def resize_image(image):

    resize = transforms.Resize((224,224))

    image = resize(image)

    return image

def image_to_tensor(image):

    transform = transforms.ToTensor()

    tensor = transform(image)

    return tensor

def normalize_tensor(tensor):

    normalize = transforms.Normalize(
        mean=[0.5,0.5,0.5],
        std=[0.5,0.5,0.5]
    )

    tensor = normalize(tensor)

    return tensor

