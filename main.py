from helpers import analyze_images, get_grouped_faces, get_largest_facegroup, get_best_image


def welcome() -> dict:
    welcome_message = "<h1>Welcome! <br> Please consult the README.md file</h1>"

    return welcome_message


def best_image(json_payload: dict) -> dict:
    """ Analyzes and finds the best image of the most common face
        from a given list of images
    """

    # Validate payload fields
    if ("images" not in json_payload) or (type(json_payload["images"]) != list):
        return {"ERROR": "Payload is malformed"}

    # Validate payload length
    images_list = json_payload["images"]
    if len(images_list) < 2:
        return {"ERROR": "A minimum of 2 images must be provided"}

    # Detect faces and get images metadata
    images_metadata = analyze_images(images_list)
    faceIds_json = {"faceIds": list(images_metadata.keys())}  # faceIds are needed for grouping

    # Group the face images
    facegroups = get_grouped_faces(faceIds_json)
    if "ERROR" in facegroups:
        return facegroups

    # Find the most common face (i.e. largest facegroup)
    largest_facegroup = get_largest_facegroup(facegroups)

    # Find best image in the most common face
    best_image = get_best_image(largest_facegroup, images_metadata)

    return best_image
