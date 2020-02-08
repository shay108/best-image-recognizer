import requests

# Some consts have an expiration date.
# To get valid "endpoint" and "key", go to:
# https://azure.microsoft.com/en-in/try/cognitive-services/
IMAGES_FOLDER = "./image_files"
AZURE_ENDPOINT = "https://westcentralus.api.cognitive.microsoft.com/face/v1.0"
AZURE_API_KEY = "e624d4fc0fb2423c890e37001e6709b7"
# AZURE_API_KEY2 = "e65f3e6ee83b46bb8328e4a204fba396"


def get_face_metadata(image_name: str) -> dict:
    """ Detects faces in images using the "Azure Face Detect" API """

    azure_face_detect_api = AZURE_ENDPOINT + "/detect"
    supported_file_extensions = ["jpg", "jpeg", "png", "gif", "bmp"]

    # Read the image into a byte array
    image_path = IMAGES_FOLDER + "/" + image_name
    try:
        image_data = open(image_path, "rb").read()
    except Exception as err:
        print(str(err))
        return {"ERROR": str(err)}

    # Validate file extension
    file_extension = image_name.split(".")[-1]
    if file_extension.lower() not in supported_file_extensions:
        err = f'Extension not supported in file: {image_name}'
        print(err)
        return {"ERROR": err}

    headers = {"Ocp-Apim-Subscription-Key": AZURE_API_KEY, "Content-Type": "application/octet-stream"}
    try:
        response = requests.post(azure_face_detect_api, headers=headers, data=image_data)
    except Exception as err:
        print(str(err))
        return {"ERROR": str(err)}

    return response.json()[0]


def analyze_images(images_list: list) -> dict:
    """ Returns a dictionary of analyzed images and their metadata """

    images_dict = dict()

    for image in images_list:
        image_metadata = get_face_metadata(image)
        if "ERROR" in image_metadata:
            continue
        new_faceId = image_metadata["faceId"]
        image_metadata["imageName"] = image

        images_dict[new_faceId] = image_metadata

    return images_dict


def get_grouped_faces(images_json: dict) -> dict:
    """ Groups similar faces into groups using the "Azure Face Group" API """

    azure_face_group_api = AZURE_ENDPOINT + "/group"

    # Validate json length
    if len(images_json["faceIds"]) < 2:
        return {"ERROR": "A minimum of 2 valid images must be provided"}

    headers = {'Ocp-Apim-Subscription-Key': AZURE_API_KEY}
    try:
        response = requests.post(url=azure_face_group_api, headers=headers, json=images_json)
    except Exception as err:
        print(str(err))
        return {"ERROR": str(err)}

    grouped_images = response.json()

    return grouped_images


def get_largest_facegroup(facegroups: list) -> list:
    """ Returns the largest facegroup from a facegroups list """

    if len(facegroups["groups"]) > 0:
        return max(facegroups["groups"], key=len)
    else:
        return facegroups["messyGroup"]


def get_best_image(facegroup: list, analyzed_images: list) -> dict:
    """ Returns the best image from a given facegroup list """

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
