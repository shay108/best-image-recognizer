from flask import Flask, request
import requests
app = Flask(__name__)

IMAGES_FOLDER = "./image_files"
AZURE_ENDPOINT = "https://westcentralus.api.cognitive.microsoft.com/face/v1.0"
AZURE_API_KEY = "e624d4fc0fb2423c890e37001e6709b7"
# AZURE_API_KEY2 = "e65f3e6ee83b46bb8328e4a204fba396"

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
        image_metadata["imageName"] = image

        images_dict[new_faceId] = image_metadata

    return images_dict


def get_grouped_faces(images_json: dict) -> dict:
    azure_face_group_api = AZURE_ENDPOINT + "/group"

    headers = {'Ocp-Apim-Subscription-Key': AZURE_API_KEY}
    response = requests.post(url=azure_face_group_api, headers=headers, json=images_json)
    grouped_images = response.json()

    return grouped_images


def get_largest_facegroup(facegroups: list) -> list:
    if len(facegroups["groups"]) > 0:
        return max(facegroups["groups"], key=len)
    else:
        return facegroups["messyGroup"]


def get_best_image(facegroup: list, analyzed_images: list) -> dict:
    from PIL import Image

    best_ratio = 0
    best_image = None
    for faceId in facegroup:
        face_meta = analyzed_images[faceId]
        face_rect = face_meta["faceRectangle"]
        face_area = face_rect["width"] * face_rect["height"]
        image_path = IMAGES_FOLDER + "/" + face_meta["imageName"]

        im = Image.open(image_path)
        tot_width, tot_height = im.size
        tot_area = tot_width * tot_height

        face_ratio = face_area / tot_area
        if face_ratio > best_ratio:
            best_ratio = face_ratio
            best_image = analyzed_images[faceId]

    best_image["faceRatio"] = round(best_ratio, 2)
    return best_image


def main(payload) -> dict:
    # Validate payload structure
    if ("images" not in payload) or (type(payload["images"]) != list):
        return "ERROR: Payload is malformed"

    # Validate payload length
    images_list = payload["images"]
    if len(images_list) < 2:
        return "ERROR: A minimum of 2 images must be provided"

    # Detect faces and get images metadata
    images_metadata = analyze_images(images_list)
    faceIds_json = {"faceIds": list(images_metadata.keys())}  # faceIds are needed for grouping

    # Group the face images
    facegroups = get_grouped_faces(faceIds_json)

    # Find the most common face (i.e. largest facegroup)
    largest_facegroup = get_largest_facegroup(facegroups)

    # Find best image in the most common face
    best_image = get_best_image(largest_facegroup, images_metadata)

    return best_image


@app.route("/api", methods=['POST'])
def api():
    payload = request.get_json()
    return main(payload)


if __name__ == '__main__':
    app.run(debug=True)