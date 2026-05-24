from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Candidate(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(200)
    )

    email = db.Column(
        db.String(200)
    )

    phone = db.Column(
        db.String(50)
    )

    skills = db.Column(
        db.Text
    )

    match_score = db.Column(
        db.Integer,
        default=0
    )

    missing_skills = db.Column(
        db.Text
    )

    summary = db.Column(
        db.Text
    )

    resume_path = db.Column(
        db.String(500)
    )

    status = db.Column(
        db.String(100),
        default="Applied"
    )