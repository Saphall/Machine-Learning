from flask import Flask, request, Response, redirect
from werkzeug.utils import secure_filename

import os

from flask import render_template

from db import db_init, db
from models import Img
import models

from tensorflow.keras.models import load_model
import cv2
from matplotlib.image import imread


app = Flask(__name__)
# SQLAlchemy config. Read more: https://flask-sqlalchemy.palletsprojects.com/en/2.x/
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///img.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['UPLOAD_FOLDER'] = "./tmp"
app.config['MAX_CONTENT_PATH'] = 100000 * 1024 * 1024
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024
db_init(app)
result =  None


@app.route('/')
def root():
    return render_template('/homepage.html')

@app.route('/about')
def about():
    return render_template('/about.html')


@app.route('/detect')
def detect():
        # return render_template('/result.html?benign')
    return render_template('index.html')


@app.route('/result')
def result():
    return render_template('result.html')


@app.route('/resultCheck')
def resultCheck():
    loaded_model = load_model('Model')

    unknown_image = imread('./tmp/image.jpg')
    unknown_image.shape   # You will see (1024,1024) image

    img = cv2.resize(unknown_image, (224, 224))
    preds = loaded_model.predict(img.reshape(1, 224, 224, 1))

    result = None

    if preds <= 0.5:
        # print("The cancer is Malignant")
        result = True
    else:
        # print("The cancer is Benign")
        result = False

    if result:
        # return render_template('/result.html', text=request.from.get('malignant', ''))
        return redirect('/result?malignant', code=302)
    elif result == False: 
        # return render_template('/result.html', text=request.from.get('malignant', ''))
        return redirect('/result?benign', code=302)
    else:
        return redirect('/result?invalid', code=302)



@app.route('/upload', methods=['POST'])
def upload():
    models.Img.query.delete()
    pic = request.files['pic']
    if not pic:
        return 'No pic uploaded!', 400

    filename = secure_filename(pic.filename)
    mimetype = pic.mimetype
    if not filename or not mimetype:
        return 'Bad upload!', 400

    img = Img(img=pic.read(), name=filename, mimetype=mimetype)
    pic.seek(0)
    pic.save(os.path.join(
        app.config['UPLOAD_FOLDER'], 'image.jpg'))
    db.session.add(img)
    db.session.commit()

    # return 'Img Uploaded!', 200
    return redirect('/detect?preview', code=302)


@app.route('/<int:id>')
def get_img(id):
    img = Img.query.filter_by(id=id).first()
    if not img:
        return 'Img Not Found!', 404

    return Response(img.img, mimetype=img.mimetype)


if __name__ == "__main__":
    app.run()
