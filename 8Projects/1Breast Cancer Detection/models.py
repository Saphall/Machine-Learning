from db import db


class Img(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    img = db.Column(db.Integer, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)
