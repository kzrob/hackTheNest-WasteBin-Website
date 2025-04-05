# Libraries
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
from datetime import datetime
import os
ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg", "heif", "heic", "webp"])

def get_file_extension(filename):
    if '.' in filename:
        return filename.rsplit('.', 1)[1].lower()
    return "none"

# App
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static/files"

@app.route("/", methods=["GET","POST"])
def home():
    if request.method == "POST":
        file = request.files["file"]
        extension = get_file_extension(file.filename)
        if file and extension in ALLOWED_EXTENSIONS:
            filename = str(datetime.now()) + '.' + extension
            save_location = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(save_location)
            return render_template("index.html", image=app.config["UPLOAD_FOLDER"] + "/" + filename)

        return "Failed to upload file: (" + file.filename + ")"
    
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)