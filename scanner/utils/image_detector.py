import torch
# import torch.nn.functional as F
# from torchvision import models
import cv2
import numpy as np
from transformers import CLIPProcessor, CLIPModel
from PIL import Image
# 🔥 Load pretrained model (real AI detector)
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

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




def detect_ai_image(image_path):

    image = Image.open(image_path).convert("RGB")

    prompts = [
        "a real natural photograph taken with a DSLR camera",
        "a candid real life photo",
        "a professional photography portrait",

        "an AI generated image",
        "digital art created by AI",
        "synthetic unrealistic image"
    ]

    inputs = processor(text=prompts, images=image, return_tensors="pt", padding=True)

    with torch.no_grad():
        outputs = model(**inputs)

    probs = outputs.logits_per_image.softmax(dim=1)[0]

    # Split scores
    human_score = (probs[0] + probs[1] + probs[2]) / 3
    ai_score = (probs[3] + probs[4] + probs[5]) / 3

    human_prob = human_score.item()
    ai_prob = ai_score.item()

    # Normalize
    total = human_prob + ai_prob
    human_prob = (human_prob / total)
    ai_prob = (ai_prob / total)

    # Convert to %
    human_prob = round(human_prob * 100, 2)
    ai_prob = round(ai_prob * 100, 2)

    confidence = round(abs(ai_prob - human_prob), 2)

    # ✅ SAFE document detection
    gray = cv2.imread(image_path, 0)

    if gray is not None:
        edges = cv2.Canny(gray, 100, 200)
        edge_density = np.mean(edges)

        # better heuristic for documents
        if edge_density > 20 and edge_density < 80:
            return {
                "ai_probability": 10,
                "human_probability": 90,
                "confidence": 80,
                "artifacts": ["Document-like structure detected"],
                "type": "Rule-based override"
            }
    artifacts, edge_density, laplacian_var = detect_artifacts(image_path)
    return {
        "ai_probability": ai_prob,
        "human_probability": human_prob,
        "confidence": confidence,
        "artifacts":artifacts,
        "type": "CLIP multi-prompt"
    }