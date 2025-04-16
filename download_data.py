import os
import pandas as pd
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

# Define paths
TRAIN_FILE = "Train_GCC-training.tsv"
VAL_FILE = "Validation_GCC-1.1.0-Validation.tsv"

TRAIN_OUTPUT_DIR = "training"
VAL_OUTPUT_DIR = "validation"

# Ensure directories exist
os.makedirs(TRAIN_OUTPUT_DIR, exist_ok=True)
os.makedirs(VAL_OUTPUT_DIR, exist_ok=True)

# Function to download images
def download_image(row, output_dir):
    """Downloads an image from a URL and saves it to the output directory."""
    url, caption = row.url, row.caption  # Extract values using named columns
    img_id = row.Index  # ✅ Corrected: Using row.Index

    try:
        response = requests.get(url, timeout=5, stream=True)
        if response.status_code == 200 and 'image' in response.headers.get("content-type", ""):
            img_path = os.path.join(output_dir, f"{img_id}.jpg")
            with open(img_path, "wb") as img_file:
                for chunk in response.iter_content(1024):
                    img_file.write(chunk)
            return img_id, "Success"
        else:
            return img_id, f"Failed (Status: {response.status_code})"
    except Exception as e:
        return img_id, f"Error: {str(e)}"

# Download images with multithreading and progress bar
def download_dataset(tsv_file, output_dir):
    """Processes a dataset file, downloading images to the output directory."""
    df = pd.read_csv(tsv_file, sep="\t", header=None, names=["url", "caption"])
    
    results = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_img = {executor.submit(download_image, row, output_dir): row.Index for row in df.itertuples(index=True)}
        
        for future in tqdm(as_completed(future_to_img), total=len(future_to_img), desc=f"Downloading {os.path.basename(tsv_file)}"):
            results.append(future.result())

    # Save download report
    failed_df = pd.DataFrame(results, columns=["ID", "Status"])
    failed_df.to_csv(os.path.join(output_dir, "download_report.tsv"), sep="\t", index=False)

# Start downloading
print("🚀 Downloading Training Set...")
download_dataset(TRAIN_FILE, TRAIN_OUTPUT_DIR)

print("🚀 Downloading Validation Set...")
download_dataset(VAL_FILE, VAL_OUTPUT_DIR)

print("✅ Download completed!")
