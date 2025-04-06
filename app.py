# Libraries
from flask import Flask, request, render_template
from datetime import datetime
import json
import os
import requests

# App
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static/files"

# Constants
ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg", "heif", "heic", "webp"])
API = "http://127.0.0.1:8000/predict/"

# Functions
def get_file_extension(filename):
	if '.' in filename:
		return filename.rsplit('.', 1)[1].lower()
	return "<h1>File extension error</h1> File " + filename

def requestAPI(file_path):
	with open(file_path, 'rb') as image_file:
		response = requests.post(API, files={'file': image_file})
		if response.status_code == 200:
			return response.json()["prediction"]
		return "<h1>API request error</h1> Status code " + str(response.status_code)

def edit_json_file(file_path, key, value):
	try:
		with open(file_path, 'r') as file:
			data = json.load(file)
	except FileNotFoundError:
		print(f"Error: File not found: {file_path}")
		return
	except json.JSONDecodeError:
		print(f"Error: Invalid JSON format in: {file_path}")
		return
	
	data[key] = value

	with open(file_path, 'w') as file:
		json.dump(data, file, indent=4)

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
			result = "a " + requestAPI(save_location)
			return render_template("index.html", image=app.config["UPLOAD_FOLDER"] + "/" + filename, result=result)
		return "Failed to upload file: (" + file.filename + ")"
	return render_template("index.html")

@app.route("/about")
def about():
	return render_template("about.html")

# Run
if __name__ == "__main__":
	app.run(debug=True)