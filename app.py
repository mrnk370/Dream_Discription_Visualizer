from flask import Flask, render_template, request
from image_generator import generate_images

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    image_paths = []
    if request.method == "POST":
        prompt = request.form.get("prompt")
        num_images = int(request.form.get("num_images", 3))
        image_paths = generate_images(prompt, num_images)
    return render_template("index.html", image_paths=image_paths)

if __name__ == "__main__":
    app.run(debug=True)


