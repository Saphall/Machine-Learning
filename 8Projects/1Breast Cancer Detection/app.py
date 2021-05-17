from flask import Flask, request, Response, redirect
from werkzeug.utils import secure_filename

import os

from flask import render_template

from db import db_init, db
from models import Img
import models


app = Flask(__name__)
# SQLAlchemy config. Read more: https://flask-sqlalchemy.palletsprojects.com/en/2.x/
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///img.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['UPLOAD_FOLDER'] = "./tmp"
app.config['MAX_CONTENT_PATH'] = 100000 * 1024 * 1024
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024
db_init(app)


@app.route('/')
def root():
    return render_template('/homepage.html')

@app.route('/about')
def about():
    return render_template('/about.html')


@app.route('/detect')
def detect():
    return render_template('/index.html')


@app.route('/result')
def result():
    return render_template('/result.html')


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
