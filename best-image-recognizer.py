from flask import Flask, request
import requests
app = Flask(__name__)

IMAGES_FOLDER = "./image_files"
AZURE_ENDPOINT = "https://westcentralus.api.cognitive.microsoft.com/face/v1.0"
AZURE_API_KEY = "e624d4fc0fb2423c890e37001e6709b7"
AZURE_API_KEY2 = "e65f3e6ee83b46bb8328e4a204fba396"

MOCK_JSON_INPUT = {
    "images": [
        "barack1.jpg",
        "barack2.jpg",
        "barack3.jpg",
        "donald1.jpg",
        "donald2.jpg",
        "hillary1.jpg"
    ]
}


def get_face_metadata(image_name: str) -> dict:
    azure_face_detect_api = AZURE_ENDPOINT + "/detect"

    # Read the image into a byte array
    image_path = IMAGES_FOLDER + "/" + image_name
    image_data = open(image_path, "rb").read()

    headers = {"Ocp-Apim-Subscription-Key": AZURE_API_KEY, "Content-Type": "application/octet-stream"}
    response = requests.post(azure_face_detect_api, headers=headers, data=image_data)

    return response.json()[0]


def analyze_images(images_list: list) -> dict:
    images_dict = dict()

    for image in images_list:
        image_metadata = get_face_metadata(image)
        new_faceId = image_metadata["faceId"]
        image_metadata["image_name"] = image

        images_dict[new_faceId] = image_metadata

    return images_dict


def get_grouped_faces(images_json: dict) -> dict:
    azure_face_group_api = AZURE_ENDPOINT + "/group"

    headers = {'Ocp-Apim-Subscription-Key': AZURE_API_KEY}
    response = requests.post(url=azure_face_group_api, headers=headers, json=images_json)
    grouped_images = response.json()

    return grouped_images


def get_best_image(facegroup: list, analyzed_images: list) -> dict:
    from PIL import Image

    best_ratio = 0
    best_image = None
    for faceId in facegroup:
        face_meta = analyzed_images[faceId]
        face_rect = face_meta["faceRectangle"]
        face_area = face_rect["width"] * face_rect["height"]
        image_path = IMAGES_FOLDER + "/" + face_meta["image_name"]

        im = Image.open(image_path)
        tot_width, tot_height = im.size
        tot_area = tot_width * tot_height

        face_ratio = face_area / tot_area
        if face_ratio > best_ratio:
            best_ratio = face_ratio
            best_image = analyzed_images[faceId]

    return best_image


def main(payload) -> dict:
    images_list = payload["images"]
    enhanced_images = analyze_images(images_list)
    faceIds_json = {"faceIds": list(enhanced_images.keys())}

    # Group the face images into groups
    facegroups = get_grouped_faces(faceIds_json)

    # Assuming the groups list is sorted according to size
    most_common_facegroup = facegroups["groups"][0]

    # Find best image in the most common facegroup
    best_image = get_best_image(most_common_facegroup, enhanced_images)

    return best_image


@app.route("/api", methods=['POST'])
def api():
    payload = request.get_json()
    return main(payload)


if __name__ == '__main__':
    app.run(debug=True)