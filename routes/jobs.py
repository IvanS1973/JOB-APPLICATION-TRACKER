"""Jobs CRUD. Skills typed as 'Python, SQL' are stored as the JSON array ["Python", "SQL"]."""
from flask import Blueprint, flash, redirect, render_template, request, url_for

from matching import parse_skills
from models import Company, Job, JOB_TYPES, db
from routes.helpers import text, to_date, to_int

bp = Blueprint("jobs", __name__, url_prefix="/jobs")


def fill_job(job, form):
    title = text(form, "job_title", 100)
    if not title:
        raise ValueError("Job title is required.")
    company_id = to_int(form, "company_id")
    if not company_id or not db.session.get(Company, company_id):
        raise ValueError("Please choose an existing company.")
    job_type = text(form, "job_type")
    if job_type and job_type not in JOB_TYPES:
        raise ValueError("Invalid job type.")
    salary_min = to_int(form, "salary_min")
    salary_max = to_int(form, "salary_max")
    if (salary_min is not None and salary_min < 0) or (salary_max is not None and salary_max < 0):
        raise ValueError("Salaries cannot be negative.")
    if salary_min is not None and salary_max is not None and salary_min > salary_max:
        raise ValueError("Minimum salary cannot be greater than maximum salary.")

    job.job_title = title
    job.company_id = company_id
    job.job_type = job_type
    job.salary_min = salary_min
    job.salary_max = salary_max
    job.job_url = text(form, "job_url", 300)
    job.date_posted = to_date(form, "date_posted")
    job.requirements = parse_skills(form.get("requirements", ""))  # Python list -> MySQL JSON array


@bp.route("/")
def list_jobs():
    company_id = request.args.get("company_id", type=int)
    job_type = request.args.get("job_type", "")
    query = Job.query
    if company_id:
        query = query.filter(Job.company_id == company_id)
    if job_type in JOB_TYPES:
        query = query.filter(Job.job_type == job_type)
    jobs = query.order_by(Job.date_posted.desc(), Job.job_id.desc()).all()
    companies = Company.query.order_by(Company.company_name).all()
    return render_template("jobs/list.html", jobs=jobs, companies=companies, job_types=JOB_TYPES,
                           company_id=company_id, job_type=job_type)


def render_form(job):
    companies = Company.query.order_by(Company.company_name).all()
    return render_template("jobs/form.html", job=job, companies=companies, job_types=JOB_TYPES, form=request.form)


@bp.route("/new", methods=["GET", "POST"])
def create():
    job = Job(company_id=request.args.get("company_id", type=int))
    if request.method == "POST":
        try:
            fill_job(job, request.form)
            db.session.add(job)
            db.session.commit()
            flash(f"Job '{job.job_title}' added.", "success")
            return redirect(url_for("jobs.detail", job_id=job.job_id))
        except ValueError as e:
            db.session.rollback()
            flash(str(e), "error")
    return render_form(job)


@bp.route("/<int:job_id>")
def detail(job_id):
    job = db.get_or_404(Job, job_id)
    return render_template("jobs/detail.html", job=job)


@bp.route("/<int:job_id>/edit", methods=["GET", "POST"])
def edit(job_id):
    job = db.get_or_404(Job, job_id)
    if request.method == "POST":
        try:
            fill_job(job, request.form)
            db.session.commit()
            flash("Job updated.", "success")
            return redirect(url_for("jobs.detail", job_id=job_id))
        except ValueError as e:
            db.session.rollback()
            flash(str(e), "error")
    return render_form(job)


@bp.route("/<int:job_id>/delete", methods=["POST"])
def delete(job_id):
    job = db.get_or_404(Job, job_id)
    if job.applications:
        flash(f"Cannot delete '{job.job_title}': it has {len(job.applications)} application(s). "
              "Delete those applications first.", "error")
        return redirect(url_for("jobs.detail", job_id=job_id))
    db.session.delete(job)
    db.session.commit()
    flash("Job deleted.", "success")
    return redirect(url_for("jobs.list_jobs"))
