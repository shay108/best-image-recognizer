from flask import Flask, request
from main import welcome, best_image
app = Flask(__name__)

MOCK_JSON_INPUT = {
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
}


@app.route("/", methods=['GET'])
def root_api():
    return welcome()


@app.route("/best_image", methods=['POST'])
def best_image_api():
    payload = request.get_json()
    return best_image(payload)


if __name__ == '__main__':
    app.run(debug=True)