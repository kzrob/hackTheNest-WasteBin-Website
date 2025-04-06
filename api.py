from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import torch
import io

from transformers import CLIPProcessor, CLIPModel

# Create FastAPI app
app = FastAPI()

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load CLIP model + processor
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(device)
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

# Labels for bin classification
bin_labels = [
    "Trash",
    "Recycling",
    "Compost",
    "E-Waste disposal",
    "Check local disposal regulations (batteries/glass)"
]

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    # Load image
    image_bytes = await file.read()
    try:
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    except Exception:
        return {"error": "Invalid image file."}

    # Prepare inputs
    inputs = processor(
        text=[f"This is {label}" for label in bin_labels],
        images=image,
        return_tensors="pt",
        padding=True
    ).to(device)

    # Inference
    with torch.no_grad():
        outputs = model(**inputs)
        logits_per_image = outputs.logits_per_image  # shape: [1, num_labels]
        probs = logits_per_image.softmax(dim=1)

    # Get top label
    top_idx = probs.argmax().item()
    top_label = bin_labels[top_idx]

    return {
        "prediction": top_label,
        "confidence": round(probs[0, top_idx].item(), 4)
    }
