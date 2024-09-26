import os
import requests
from pathlib import Path
from ultralytics import YOLO

# URL to download the model if not present
MODEL_URL = "https://drive.usercontent.google.com/uc?id=1igv9rp7LKlkLbGPbxvtM4D4DFM7wtQZy&export=download"
MODEL_NAME = "best.pt"

# Get the path to the user's cache directory
CACHE_DIR = Path.home() / ".cache" / "AI_models_Robocon_24"
MODEL_PATH = CACHE_DIR / MODEL_NAME

# Ensure the cache directory exists
CACHE_DIR.mkdir(parents=True, exist_ok=True)

def download_model_if_not_exists():
    """Check if model exists, otherwise download it to cache folder."""
    if not MODEL_PATH.exists():
        print(f"Model not found at {MODEL_PATH}. Downloading...")
        response = requests.get(MODEL_URL, stream=True)
        if response.status_code == 200:
            # Write the model file to the cache directory
            with open(MODEL_PATH, 'wb') as model_file:
                for chunk in response.iter_content(chunk_size=8192):
                    model_file.write(chunk)
            print(f"Model downloaded successfully and saved to {MODEL_PATH}")
        else:
            raise RuntimeError(f"Failed to download the model. Status code: {response.status_code}")
    else:
        print(f"Model found at {MODEL_PATH}")

# Download the model if it doesn't exist
download_model_if_not_exists()

# Load the YOLO model from the cache
model = YOLO(str(MODEL_PATH))

def ball_detection(image):
    global model
    results = model.predict(image,conf = 0.3)
    results_image = results[0].plot()
    return results_image,results


