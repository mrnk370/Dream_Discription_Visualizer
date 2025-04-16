import os
import pandas as pd
import requests
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
from tqdm import tqdm

# Define paths
TRAIN_FILE = "Train_GCC-training.tsv"
VALID_FILE = "Validation_GCC-1.1.0-Validation.tsv"

TRAIN_OUTPUT_DIR = "download_report.tsv"
VALID_OUTPUT_DIR = "download_report.tsv"

# Ensure output directories exist
os.makedirs(TRAIN_OUTPUT_DIR, exist_ok=True)
os.makedirs(VALID_OUTPUT_DIR, exist_ok=True)

# Function to download images
def download_image(row, output_dir):
    try:
        url = row.url
        img_id = row.Index  # Using index as image name

        response = requests.get(url, timeout=5, stream=True)
        if response.status_code == 200 and 'image' in response.headers.get("content-type", ""):
            img_path = os.path.join(output_dir, f"{img_id}.jpg")
            with open(img_path, "wb") as img_file:
                for chunk in response.iter_content(1024):
                    img_file.write(chunk)
            return (img_id, "Success")
        else:
            return (img_id, "Failed")
    except Exception as e:
        return (img_id, f"Error: {str(e)}")

# Function to process dataset
def process_dataset(file_path, output_dir):
    # Read dataset, ensuring correct column names
    try:
        df = pd.read_csv(file_path, sep="\t", header=None, names=["url", "caption"])
    except Exception as e:
        print(f"❌ Error reading {file_path}: {e}")
        return

    if "url" not in df.columns:
        print(f"⚠️ Error: No 'url' column found in {file_path}!")
        return

    # Download images with multithreading
    print(f"🚀 Downloading images from {file_path}...")
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(tqdm(executor.map(lambda row: download_image(row, output_dir), df.itertuples(index=True)), total=len(df)))

    # Save download report
    failed_df = pd.DataFrame(results, columns=["ID", "Status"])
    failed_df.to_csv(os.path.join(output_dir, "download_report.tsv"), sep="\t", index=False)

# Function to remove corrupt images
def remove_corrupt_images(folder_path):
    print(f"🔍 Checking images in {folder_path}...")
    for filename in tqdm(os.listdir(folder_path)):
        file_path = os.path.join(folder_path, filename)

            # Skip non-image files
        if not filename.lower().endswith((".jpg", ".jpeg", ".png", ".bmp", ".gif")):
            continue

        try:
            with Image.open(file_path) as img:
                img.verify()
        except (IOError, SyntaxError):
            print(f"❌ Removing corrupt image: {filename}")
            os.remove(file_path)

# Process Training Data
print("📂 Processing Training Data...")
process_dataset(TRAIN_FILE, TRAIN_OUTPUT_DIR)
remove_corrupt_images(TRAIN_OUTPUT_DIR)

# Process Validation Data
if os.path.exists(VALID_FILE):
    print("📂 Processing Validation Data...")
    process_dataset(VALID_FILE, VALID_OUTPUT_DIR)
    remove_corrupt_images(VALID_OUTPUT_DIR)

print("✅ Preprocessing completed successfully!")
