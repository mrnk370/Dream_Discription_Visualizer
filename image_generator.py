import os
import torch
from diffusers import StableDiffusionPipeline

# Select device (prefer GPU if available)
device = "cuda" if torch.cuda.is_available() else "cpu"

# Load Stable Diffusion model
pipeline = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
    use_safetensors=True,
).to(device)

def generate_images(prompt, num_images=3):
    """
    Generate multiple images based on the input prompt.

    Args:
        prompt (str): The text description for image generation.
        num_images (int): Number of images to generate.

    Returns:
        list: Paths of generated images.
    """
    # Replicate the prompt for batch image generation
    prompts = [prompt] * num_images
    images = pipeline(prompts, num_inference_steps=50, guidance_scale=7.5).images

    # Ensure output directory exists
    output_dir = "static/generated"
    os.makedirs(output_dir, exist_ok=True)

    image_paths = []
    for i, img in enumerate(images):
        img_path = f"{output_dir}/image_{i}.png"
        img.save(img_path)
        image_paths.append(img_path)

    return image_paths
