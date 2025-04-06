import requests

# Define the API endpoint
url = "http://127.0.0.1:8000/predict/"

# Path to the test image
image_path = "unnamed.jpg"  # Replace with the path to your test image

# Open the image file in binary mode and send it to the API
with open(image_path, "rb") as image_file:
    files = {"file": image_file}
    response = requests.post(url, files=files)

# Print the response from the API
print(response.json())
