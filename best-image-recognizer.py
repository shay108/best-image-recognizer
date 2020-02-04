from flask import Flask
import json

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route("/api", methods=['POST', 'GET'])
def api():
    return {"result": "success"}





if __name__ == '__main__':
    app.run(debug=True)