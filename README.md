# Best-Image Recognizer Project

## General
This python service exposes an http endpoint which finds the most common face in a list of images, and returns metadata about the "best image" of this common face.
"Best Image" is defined by: the image where the *bounding box* of the face is largest in relation to the *overall size* of the image. 

The service utilizes the **Azure Face API** ([link](https://azure.microsoft.com/en-us/services/cognitive-services/face/#detection)).

## Input
The service gets a `JSON over http`, containing a *list of images* (*image* means a local filename).

## Output
The http request returns a `JSON over http` as well. The JSON contains:
1. Face metadata (from the Azure API) of the "best iamge"
2. Filename of the "best image"

## Installation
1. Download the files to a folder or clone the repo
2. In the root folder, create a virtualenv: `virtualenv -p python3.7 venv` (on linux/mac)
3. Activate the virtualenv: `. /venv/bin/activate` (on linux/mac)
4. Install the requirements: `pip install -r requirements`
5. Run the program: `python best-image-recognizer.py`

## Process
TBD

## Architecture
TBD

## Potential Improvements
TBD
