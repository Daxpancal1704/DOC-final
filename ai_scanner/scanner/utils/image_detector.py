import torch
import torch.nn.functional as F
from torchvision import models

model = models.resnet18(pretrained=True)

model.eval()

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


def detect_ai_image(tensor):

    probabilities = predict_image(tensor)

    result = classify_ai_image(probabilities)

    return result