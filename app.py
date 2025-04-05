# Libraries
from flask import Flask, request, render_template
from datetime import datetime
import os
import requests

# App
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static/files"

# Constants
ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg", "heif", "heic", "webp"])
API = "https://api-4j61.onrender.com/predict"

# Functions
def get_file_extension(filename):
	if '.' in filename:
		return filename.rsplit('.', 1)[1].lower()
	return "<h1>File extension error</h1> File " + filename

def requestAPI(file_path):
	with open(file_path, 'rb') as image_file:
		response = requests.post(API, files={'file': image_file})
		print()
		print(response.content)
		print()
		print(response.json)
		print()
		print(response.status_code)
		print()
		if response.status_code == 200:
			return response.json()["prediction"]
		return "<h1>API request error</h1> Status code " + str(response.status_code)

# Routing
@app.route("/", methods=["GET","POST"])
def home():
	if request.method == "POST":
		file = request.files["file"]
		extension = get_file_extension(file.filename)
		if file and extension in ALLOWED_EXTENSIONS:
			filename = str(datetime.now()) + '.' + extension
			save_location = os.path.join(app.config["UPLOAD_FOLDER"], filename)
			file.save(save_location)
			result = requestAPI(save_location)
			return result
			# return render_template("index.html", image=app.config["UPLOAD_FOLDER"] + "/" + filename)

		return "Failed to upload file: (" + file.filename + ")"
	
	return render_template("index.html")

# Run
if __name__ == "__main__":
	app.run(debug=True)