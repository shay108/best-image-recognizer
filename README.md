# Best-Image Recognizer Project

## General
This python service exposes an http endpoint which finds the most common face in a list of images, and returns metadata about the "best image" of this common face.
"Best Image" is defined by: the image where the *bounding box* of the face is largest in relation to the *overall size* of the image. 

The service utilizes the **Azure Face API** ([more info here](https://azure.microsoft.com/en-us/services/cognitive-services/face)).

## Input
The service gets a `JSON over http`, containing a *list of images* (*image* means a local filename).
The list of images references filenames located in the "local storage" of the webserver (namely the `image_files` folder).

Example json, below.

## Output
The http request returns a `JSON over http` as well. The JSON contains:
1. Face metadata (from the Azure API) of the "best image"
2. Filename of the "best image"
3. Face ratio of the "best image".

Example json, below.

## Installation
1. Download the files to a folder or clone the repo
2. In the root folder, create a virtualenv: `virtualenv -p python3.7 venv`
3. Activate the virtualenv: `. /venv/bin/activate`
4. Install the requirements: `pip install -r requirements`
5. Set the `FLASK_APP` environment variable: `export FLASK_APP=flask_handler.py`
* For *debug* mode, also set the following variable: `export FLASK_DEBUG=1`  
6. Start the webserver: `python -m flask run`

## Usage
After starting the webserver, use any kind of web client (e.g. *Postman*) to make a post request to the exposed API: `localhost:5000/best_image`

**IMPORTANT:** the application currently uses a free-tier `AZURE_ENDPOINT` and `AZURE_API_KEY` (which are valid until **2020-02-12**). After these dates - new key and endpoint need to be generated from Microsoft ([here](https://azure.microsoft.com/en-in/try/cognitive-services/)).
The new endpoint and key need to be updated in *consts* section at the `helpers.py` file.  
 
### JSON payload example
<pre><code>{
    "images": [
        "john_smith.jpg",
        "barack3.jpg",
        "not_an_image.txt",
        "donald2.jpg",
        "barack2.jpg",
        "donald1.jpg",
        "hillary1.jpg",
        "barack1.jpg"
    ]
}</code></pre>
* Note the above example contains both:
1. Image files which exist in the local storage of the webserver (e.g. `barack3.jpg`)
2. Files which demonstrate the error handling capabilities of the software (e.g. `not_an_image.txt`)

### Response
A valid response for the above input will look like:
<pre><code>{
  "faceId": "ca4dc86e-3722-49a6-b43c-533a669609ed",
  "faceRatio": 0.39,
  "faceRectangle": {
    "height": 253,
    "left": 50,
    "top": 144,
    "width": 253
  },
  "imageName": "barack2.jpg"
}</code></pre>

## Process
The `flask_handler.py` file directs each API endpoint to a specific "main" function (located in the `main.py` file).
Logic is divided into steps including:
1. Input validation
2. Detecting faces in give *image list*
3. Grouping similar faces into *facegroups*
4. Finding the *most common face*
5. Finding the "best image" of the most common face

## Error handling and tests
The software supports handling of the following errors/exceptions:
- An image is not found (handled by error message and skipping)
- Unsupported file format (handled by error message and skipping)
- Not enough valid images (handled by error message and exiting)
- Exceptions in 3rd party APIs (handled by error message and exiting)
- Two "equally-common" faces (handled by choosing one at random)
- No common face found (handled by choosing "best image" from the misc `messyGroup` facegroup)
* As mentioned above, the *example json*  contains some entries which demonstrate handling some of the above errors 

## Potential Improvements
1. Error propagation is done in a very basic way, and can be improved
2. Adding automated tests
3. Adding type checking (e.g. using `mypy`)
