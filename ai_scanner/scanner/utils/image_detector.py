import torch
import torch.nn.functional as F
from torchvision import models
import cv2
import numpy as np

model = models.resnet18(pretrained=True)

model.eval()


def detect_generation_type(artifacts):
    if any("GAN" in a for a in artifacts):
        return "GAN-generated"
    elif any("Diffusion" in a for a in artifacts):
        return "Diffusion-based"
    else:
        return "Uncertain"

def detect_artifacts(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    edges = cv2.Canny(gray, 100, 200)
    edge_density = np.mean(edges)

    laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()

    artifacts = []

    # Blur detection (diffusion-like)
    if laplacian_var < 50:
        artifacts.append("Blurry / smooth regions (Diffusion-like)")

    # Over-sharp edges (GAN-like)
    if edge_density > 80:
        artifacts.append("Over-sharp edges (GAN-like)")

    # Low texture variation
    if edge_density < 20:
        artifacts.append("Low texture consistency")

    return artifacts, edge_density, laplacian_var

def predict_image(tensor):

    with torch.no_grad():

        outputs = model(tensor)

        probabilities = F.softmax(outputs[0], dim=0)

    return probabilities

def classify_ai_image(probabilities):

    max_prob = torch.max(probabilities).item()

    if max_prob < 0.4:
        ai_prob = 0.75
        human_prob = 0.25

    else:
        ai_prob = 0.25
        human_prob = 0.75

    return {
        "ai_probability": round(ai_prob*100,2),
        "human_probability": round(human_prob*100,2)
    }


def detect_ai_image(tensor, image_path):

    probabilities = predict_image(tensor)

    max_prob = torch.max(probabilities).item()

    # Normalize confidence (not fake anymore)
    confidence = round(max_prob * 100, 2)

    # Artifact detection
    artifacts, edge_density, laplacian_var = detect_artifacts(image_path)

    # Basic AI decision (combined logic)
    if len(artifacts) >= 2:
        result = "AI"
        ai_prob = 70 + min(len(artifacts)*5, 20)
        human_prob = 100 - ai_prob
    else:
        result = "Human"
        human_prob = 70
        ai_prob = 30

    gen_type = detect_generation_type(artifacts)

    return {
        "ai_probability": ai_prob,
        "human_probability": human_prob,
        "confidence": confidence,
        "artifacts": artifacts,
        "type": gen_type
    }