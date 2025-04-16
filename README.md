# 🌌 Dream Description Visualizer

Turn your dreams into **realistic AI-generated images** with a single click!  
This project uses the **Stable Diffusion v1.5** model to transform natural language descriptions of dreams into beautiful, downloadable artwork.


### 🌆 Example Output – "Futuristic City at Sunset"

[Generated Image](output.png))


---

## ✨ Overview

**Dream Description Visualizer** is a deep learning-based web application that allows users to describe their dreams or ideas in natural language and instantly receive visual interpretations powered by **Stable Diffusion**.

Whether you're a storyteller, writer, artist, or someone who wants to visualize their wildest imagination — this tool brings your **textual dreams to life** 🌠

---

## 🧠 How It Works

1. 💬 **User inputs a dream** (e.g., "A glowing castle floating in the sky at night").
2. ⚙️ **Model tokenizes and processes** the prompt.
3. 🧨 **Stable Diffusion v1.5** generates high-quality images.
4. 🖼️ **Images are displayed** with options to download.
5. 🔁 Can generate up to **5 unique images per prompt**.

---

## 🔍 Key Features

- 🧠 **Text-to-Image AI** powered by [Stable Diffusion v1.5](https://huggingface.co/runwayml/stable-diffusion-v1-5)
- 🎨 Generate **multiple variations** (1 to 5) of the image
- 🌐 Fully interactive **Flask web application**
- 📥 **Download** any generated image directly
- 💡 Clean, elegant UI built with **Bootstrap 5**
- 🖼️ Preprocessed dataset using **Conceptual Captions** by Google AI

---

## 🏗️ Tech Stack

| Layer       | Tools Used                                                                 |
|-------------|----------------------------------------------------------------------------|
| Frontend    | HTML5, CSS3, Bootstrap 5, JavaScript                                       |
| Backend     | Python, Flask, PyTorch, HuggingFace Diffusers & Transformers               |
| Model       | `StableDiffusionPipeline` from `diffusers`                                 |
| Deployment  | Localhost / Streamlit-ready                                                |

---

## 🗃️ Dataset

- **Name:** Conceptual Captions  
- **Source:** [Google AI Research](https://ai.google.com/research/ConceptualCaptions)  
- **Type:** Paired image-caption data (~3.3M records)  
- **Purpose:** Pretraining + fine-tuning for text-to-image generation models

---

## ⚙️ Installation

```bash
git clone https://github.com/yourusername/dream-description-visualizer.git
cd dream-description-visualizer
pip install -r requirements.txt
python app.py

Then open your browser at http://127.0.0.1:5000
