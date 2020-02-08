from flask import Flask, request
from main import best_image
app = Flask(__name__)

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


@app.route("/best_image", methods=['POST'])
def api():
    payload = request.get_json()
    return best_image(payload)


if __name__ == '__main__':
    app.run(debug=True)