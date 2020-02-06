# Endpoint: https://westcentralus.api.cognitive.microsoft.com/face/v1.0
# Key 1: e624d4fc0fb2423c890e37001e6709b7
# Key 2: e65f3e6ee83b46bb8328e4a204fba396

# https://i.ibb.co/tpXQ1tH/Shay-Profile-Pic.jpg

from flask import Flask
import json
import requests

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route("/api", methods=['POST'])
def api():
    # Parse input
    image_list = payload[0]
    enriched_image_list = get_parsed_http_input(payload)

    # Group the face images into groups
    facegroup_list = get_grouped_faces(image_list)

    # Assuming the groups list is sorted according to size
    most_common_facegroup = facegroup_list[0]

    # Find best image in the most common facegroup
    best_image = get_best_image(most_common_facegroup)

    # Get the best image's metadata
    best_image_metadata = get_image_metadata(best_image, enriched_image_list)

    return best_image_metadata




if __name__ == '__main__':
    app.run(debug=True)