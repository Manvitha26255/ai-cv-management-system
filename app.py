from flask import (
    Flask,
    render_template,
    request,
    redirect,
    session,
    send_file
)

from flask_bcrypt import Bcrypt

from models.candidate import db, Candidate
from models.admin import Admin

from services.parser import extract_text_from_pdf
from services.extractor import extract_candidate_details
from services.matcher import calculate_match
from services.google_service import save_to_google_sheet
from services.summary import generate_summary

from collections import Counter

import os

app = Flask(__name__)

bcrypt = Bcrypt(app)

app.secret_key = "secret123"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["UPLOAD_FOLDER"] = "uploads"

db.init_app(app)

with app.app_context():

    db.create_all()

    if not Admin.query.filter_by(
        email="admin@gmail.com"
    ).first():

        hashed_password = bcrypt.generate_password_hash(
            "admin123"
        ).decode("utf-8")

        admin = Admin(
            email="admin@gmail.com",
            password=hashed_password
        )

        db.session.add(admin)

        db.session.commit()


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]

        password = request.form["password"]

        admin = Admin.query.filter_by(
            email=email
        ).first()

        if admin and bcrypt.check_password_hash(
            admin.password,
            password
        ):

            session["admin"] = admin.email

            return redirect("/")

        else:

            return """
            <h2 style='color:red;text-align:center;margin-top:50px;'>
            Invalid Credentials
            </h2>
            """

    return render_template("login.html")


@app.route("/logout")
def logout():

    session.pop("admin", None)

    return redirect("/login")


@app.route("/")
def dashboard():

    if "admin" not in session:

        return redirect("/login")

    candidates = Candidate.query.order_by(
        Candidate.match_score.desc()
    ).all()

    total_candidates = len(candidates)

    total_skills = 0

    all_skills = []

    for candidate in candidates:

        skills = candidate.skills.split(",")

        total_skills += len(skills)

        for skill in skills:

            skill = skill.strip()

            if skill != "":

                all_skills.append(skill)

    skill_counter = Counter(all_skills)

    top_skills = list(skill_counter.keys())[:5]

    top_skill_counts = list(skill_counter.values())[:5]

    candidate_names = [
        candidate.name
        for candidate in candidates
    ]

    candidate_scores = [
        candidate.match_score
        for candidate in candidates
    ]

    best_candidate = None

    if len(candidates) > 0:

        best_candidate = candidates[0]

    return render_template(
        "dashboard.html",
        candidates=candidates,
        total_candidates=total_candidates,
        total_skills=total_skills,
        top_skills=top_skills,
        top_skill_counts=top_skill_counts,
        candidate_names=candidate_names,
        candidate_scores=candidate_scores,
        best_candidate=best_candidate
    )


@app.route("/upload", methods=["POST"])
def upload_resume():

    if "admin" not in session:

        return redirect("/login")

    file = request.files["resume"]

    if file.filename == "":

        return """
        <h2 style='color:red;text-align:center;margin-top:50px;'>
        No file selected
        </h2>
        """

    if not file.filename.lower().endswith(".pdf"):

        return """
        <h2 style='color:red;text-align:center;margin-top:50px;'>
        Only PDF resumes are allowed
        </h2>
        """

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        file.filename
    )

    file.save(filepath)

    text = extract_text_from_pdf(filepath)

    candidate_data = extract_candidate_details(text)

    candidate = Candidate(
        name=candidate_data["name"],
        email=candidate_data["email"],
        phone=candidate_data["phone"],
        skills=candidate_data["skills"],
        match_score=0,
        missing_skills="",
        summary="",
        resume_path=filepath,
        status="Applied"
    )

    db.session.add(candidate)

    db.session.commit()

    save_to_google_sheet(candidate)

    return redirect("/")


@app.route("/match", methods=["POST"])
def match_candidates():

    if "admin" not in session:

        return redirect("/login")

    job_description = request.form[
        "job_description"
    ]

    candidates = Candidate.query.all()

    for candidate in candidates:

        score, missing_skills = calculate_match(
            candidate.skills,
            job_description
        )

        candidate.match_score = score

        candidate.missing_skills = missing_skills

        candidate.summary = generate_summary(
            candidate.skills,
            score
        )

        save_to_google_sheet(candidate)

    db.session.commit()

    return redirect("/")


@app.route("/update-status/<int:id>", methods=["POST"])
def update_status(id):

    candidate = Candidate.query.get(id)

    new_status = request.form["status"]

    candidate.status = new_status

    db.session.commit()

    return redirect("/")


@app.route("/download/<int:id>")
def download_resume(id):

    candidate = Candidate.query.get(id)

    return send_file(
        candidate.resume_path,
        as_attachment=True
    )


@app.route("/delete/<int:id>")
def delete_candidate(id):

    candidate = Candidate.query.get(id)

    db.session.delete(candidate)

    db.session.commit()

    return redirect("/")


if __name__ == "__main__":

    app.run(debug=True)