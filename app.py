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

def get_bin_sorting(prediction):
    if prediction in ["battery", "glass"]:
        return "Check local laws"
    if prediction == "biological":
        return "Compost"
    if prediction in ["clothes", "plastic", "shoes", "trash"]:
        return "Trash"
    if prediction in ["metal", "paper", "cardboard"]:
        return "Recycle"
    return "Unknown"

def get_rank(upload_count):
    if upload_count < 50:
        return "Unranked"
    if upload_count < 200:
        return "Bronze"
    if upload_count < 500:
        return "Silver"
    if upload_count < 1000:
        return "Platinum"
    if upload_count < 2000:
        return "Diamond"
    if upload_count < 3000:
        return "Trash Titan"
    return "Waste Warden"

# Routing
@app.route("/", methods=["GET", "POST"])
def home():
    upload_count = int(request.cookies.get("uploadCount", 0))
    rank = get_rank(upload_count)

    if request.method == "POST":
        file = request.files.get("file")
        if file and file.filename:
            extension = get_file_extension(file.filename)
            if extension in ALLOWED_EXTENSIONS:
                filename = datetime.now().strftime("%Y%m%d%H%M%S") + '.' + extension
                save_location = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                file.save(save_location)
                prediction = requestAPI(save_location)
                bin_sorting = get_bin_sorting(prediction)
                upload_count += 1
                response = render_template(
                    "index.html",
                    image=f"/{app.config['UPLOAD_FOLDER']}/{filename}",
                    result=prediction,
                    bin_sorting=bin_sorting,
                    rank=get_rank(upload_count)
                )
                response = app.make_response(response)
                response.set_cookie("uploadCount", str(upload_count))
                return response
        return "Failed to upload file. Please try again."
    return render_template("index.html", rank=rank)

@app.route("/about")
def about():
	return render_template("about.html")

# Run
if __name__ == "__main__":
	app.run(debug=True)