from flask import Flask, jsonify, redirect, request
from predict import *
from werkzeug.utils import secure_filename
import os
os.system('clear')
app = Flask(__name__)
app.config['files'] = os.path.join(__file__[:-len('app.py')], 'test/')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
def allowed_file(file):
    if file.filename[-4] in ALLOWED_EXTENSIONS: return True
    else: return False

@app.route("/image", methods=['GET', 'POST'])
def image():
    if(request.method == "POST"):
        bytesOfImage = request.get_data()
        with open('image.png', 'wb') as out:
            out.write(bytesOfImage)
        try:
            prediction_list = get_prediction(bytesOfImage)
            i=1
            for image_path in prediction_list:
                # print(image_path)
                os.system(f"cp {image_path} /home/twel/CS232/DemoApp/output/{i}.png")
                i+=1
            return {'response predict': prediction_list}
        except:
            return "Error while processing"
        return "Image read"

    

@app.route("/predict", methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        print(f'Request: {request}')
        if 'file' not in request.files:
            print(request.url)
            # return redirect(request.url)
        file = request.files['file']
        file.save(secure_filename(f.filename))
        # print('Re')
        # print(f"POST: get file {file}")
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