# THis is a file that contains the code to generate the
# embeddings of the images using the VGG16 model

import torch
import torchvision.models as models
import torchvision.transforms as transforms
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from PIL import Image


model = models.vgg16(weights="VGG16_Weights.IMAGENET1K_V1")

model = torch.nn.Sequential(*(list(model.children())[:-1]))

model.eval()

transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225]),
])


def get_embedding(image):
    image = image.convert("RGB")
    image = transform(image)
    with torch.no_grad():
        embedding = model(image)
    embedding = embedding.numpy()
    return embedding


def compare_embeddings(embedding1, embedding2):
    embedding1 = embedding1.reshape(1, -1)
    embedding2 = embedding2.reshape(1, -1)
    return cosine_similarity(embedding1, embedding2)[0][0]
