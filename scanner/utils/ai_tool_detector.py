from PIL import Image
import numpy as np

def load_image(image_path):

    image = Image.open(image_path)

    return image

def image_to_array(image):

    img_array = np.array(image)

    return img_array

def extract_features(img_array):

    mean_pixel = np.mean(img_array)

    std_pixel = np.std(img_array)

    unique_colors = len(np.unique(img_array.reshape(-1,3), axis=0))

    return mean_pixel, std_pixel, unique_colors

def guess_ai_tool(mean_pixel, std_pixel, unique_colors):

    if unique_colors < 50000:
        return "Stable Diffusion"

    elif std_pixel > 70:
        return "Midjourney"

    elif mean_pixel > 150:
        return "DALL-E"

    else:
        return "Unknown AI Tool"


def detect_ai_tool(image_path):

    image = load_image(image_path)

    img_array = image_to_array(image)

    mean_pixel, std_pixel, unique_colors = extract_features(img_array)

    tool = guess_ai_tool(mean_pixel, std_pixel, unique_colors)

    return tool