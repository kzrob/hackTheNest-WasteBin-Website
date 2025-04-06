from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import torch
import torch.nn as nn
from torchvision import models, transforms
import io

app = FastAPI()

# Allow access from anywhere (adjust for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the device (GPU if available, otherwise CPU)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load the model once during startup
num_classes = 10  # Number of classes in your dataset
model = models.efficientnet_b0(pretrained=False)
model.classifier[1] = nn.Linear(model.classifier[1].in_features, num_classes)
model.load_state_dict(torch.load('fine_tuned_model.pth'))
model = model.to(device)
model.eval()  # Set model to evaluation mode

# Define image transformation (ensure it matches training)
transform = transforms.Compose([
    transforms.Resize((224, 224)),  # Resize image to the required input size
    transforms.ToTensor(),          # Convert image to tensor
    transforms.Normalize(           # Normalize the image using the same mean/std as training
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    ),
])

# Your dataset's class labels (ensure this matches the classes used during training)
dataset_classes = ["battery", "biological", "cardboard", "clothes", "glass", "metal", "paper", "plastic", "shoes", "trash"]
@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    # Read the uploaded image
    image_bytes = await file.read()
    try:
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    except Exception:
        return {"error": "Invalid image file."}

    # Apply transformations and move to device
    input_tensor = transform(image).unsqueeze(0).to(device)

    # Perform inference (no gradient tracking)
    with torch.no_grad():
        output = model(input_tensor)
        _, predicted_class = torch.max(output, 1)

    # Get the predicted class label
    predicted_label = dataset_classes[predicted_class.item()]
    return {"prediction": predicted_label}
