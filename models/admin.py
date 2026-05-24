from models.candidate import db

class Admin(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String(200), unique=True)

    password = db.Column(db.String(200))