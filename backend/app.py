from flask import Flask, jsonify, request
from predict import *

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
def allowed_file(file):
    if file.filename[-4] in ALLOWED_EXTENSIONS: return True
    else: return False

@app.route("/predict", methods=['POST'])
def predict():
    if request.method == 'POST':
        file = request.files.get('file')
        print(file)
        if file is None or file.filename == "":
            return jsonify({'error': 'no file'})
        if allowed_file(file):
            return jsonify({'error': 'format not supported'})

        try:
            img_bytes = file.read()
            prediction_list = get_prediction_imgPATH(img_bytes)
            data = {"url": prediction_list}
            return jsonify(data)
        except:
            return jsonify({'error': 'error during prediction'})

if __name__ == "__main__":
    app.run(debug=True)