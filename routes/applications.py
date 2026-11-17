"""Applications CRUD. Interview fields from the form are stored together as one JSON object."""
from flask import Blueprint, flash, redirect, render_template, request, url_for

from models import Application, Job, STATUSES, db
from routes.helpers import text, to_date, to_int

bp = Blueprint("applications", __name__, url_prefix="/applications")

INTERVIEW_TYPES = ["Phone", "Video", "In-person", "Technical", "Panel"]


def fill_application(application, form):
    job_id = to_int(form, "job_id")
    if not job_id or not db.session.get(Job, job_id):
        raise ValueError("Please choose an existing job.")
    app_date = to_date(form, "application_date")
    if not app_date:
        raise ValueError("Application date is required.")
    status = text(form, "status") or "Applied"
    if status not in STATUSES:
        raise ValueError("Invalid status.")
    interview_date = to_date(form, "interview_date")

    interview = {
        "date": interview_date.isoformat() if interview_date else None,
        "time": text(form, "interview_time", 10),
        "type": text(form, "interview_type", 30),
        "interviewer": text(form, "interviewer", 100),
        "notes": text(form, "interview_notes"),
    }
    interview = {k: v for k, v in interview.items() if v}  # drop empty fields

    application.job_id = job_id
    application.application_date = app_date
    application.status = status
    application.resume_version = text(form, "resume_version", 50)
    application.cover_letter_sent = form.get("cover_letter_sent") == "on"
    application.interview_data = interview or None  # dict -> MySQL JSON (or NULL)


@bp.route("/")
def list_applications():
    status = request.args.get("status", "")
    sort = request.args.get("sort", "desc")
    query = Application.query
    if status in STATUSES:
        query = query.filter(Application.status == status)
    order = Application.application_date.asc() if sort == "asc" else Application.application_date.desc()
    applications = query.order_by(order, Application.application_id.desc()).all()
    return render_template("applications/list.html", applications=applications, statuses=STATUSES,
                           status=status, sort=sort)


def render_form(application):
    jobs = Job.query.order_by(Job.job_title).all()
    return render_template("applications/form.html", application=application, jobs=jobs, statuses=STATUSES,
                           interview_types=INTERVIEW_TYPES, form=request.form)


@bp.route("/new", methods=["GET", "POST"])
def create():
    application = Application(job_id=request.args.get("job_id", type=int), status="Applied")
    if request.method == "POST":
        try:
            fill_application(application, request.form)
            db.session.add(application)
            db.session.commit()
            flash("Application added.", "success")
            return redirect(url_for("applications.detail", application_id=application.application_id))
        except ValueError as e:
            db.session.rollback()
            flash(str(e), "error")
    return render_form(application)


@bp.route("/<int:application_id>")
def detail(application_id):
    application = db.get_or_404(Application, application_id)
    return render_template("applications/detail.html", application=application)


@bp.route("/<int:application_id>/edit", methods=["GET", "POST"])
def edit(application_id):
    application = db.get_or_404(Application, application_id)
    if request.method == "POST":
        try:
            fill_application(application, request.form)
            db.session.commit()
            flash("Application updated.", "success")
            return redirect(url_for("applications.detail", application_id=application_id))
        except ValueError as e:
            db.session.rollback()
            flash(str(e), "error")
    return render_form(application)


@bp.route("/<int:application_id>/delete", methods=["POST"])
def delete(application_id):
    application = db.get_or_404(Application, application_id)
    db.session.delete(application)  # nothing references applications, so this is always safe
    db.session.commit()
    flash("Application deleted.", "success")
    return redirect(url_for("applications.list_applications"))
