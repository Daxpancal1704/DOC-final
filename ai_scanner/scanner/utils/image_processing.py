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

def preprocess_image(image_path):
    image = Image.open(image_path).convert("RGB")  # 🔥 THIS FIXES IT

    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )
    ])

    tensor = transform(image).unsqueeze(0)
    return tensor