"""Job Match page: compares the user's skills to each job's JSON requirements."""
from flask import Blueprint, flash, render_template, request

from matching import parse_skills, rank_jobs
from models import Job

bp = Blueprint("match", __name__, url_prefix="/match")


@bp.route("/", methods=["GET", "POST"])
def index():
    skills_text = ""
    results = None
    if request.method == "POST":
        skills_text = request.form.get("skills", "")
        skills = parse_skills(skills_text)
        if not skills:
            flash("Please enter at least one skill, separated by commas.", "error")
        else:
            jobs = Job.query.all()  # read jobs + requirements from MySQL
            results = rank_jobs(skills, jobs)
    return render_template("match.html", skills_text=skills_text, results=results)
