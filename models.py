"""SQLAlchemy models. Each class maps to one of the four MySQL tables in schema.sql."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

JOB_TYPES = ["Full-time", "Part-time", "Contract", "Internship"]
STATUSES = ["Applied", "Screening", "Interview", "Offer", "Rejected", "Withdrawn"]


class Company(db.Model):
    __tablename__ = "companies"

    company_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    company_name = db.Column(db.String(100), nullable=False)
    industry = db.Column(db.String(50))
    website = db.Column(db.String(200))
    city = db.Column(db.String(50))
    state = db.Column(db.String(50))
    notes = db.Column(db.Text)

    # One company -> many jobs, one company -> many contacts
    jobs = db.relationship("Job", back_populates="company")
    contacts = db.relationship("Contact", back_populates="company")


class Job(db.Model):
    __tablename__ = "jobs"

    job_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    company_id = db.Column(db.Integer, db.ForeignKey("companies.company_id"))
    job_title = db.Column(db.String(100), nullable=False)
    job_type = db.Column(db.Enum(*JOB_TYPES, name="job_type"))
    salary_min = db.Column(db.Integer)
    salary_max = db.Column(db.Integer)
    job_url = db.Column(db.String(300))
    date_posted = db.Column(db.Date)
    requirements = db.Column(db.JSON)  # e.g. ["Python", "SQL"]

    company = db.relationship("Company", back_populates="jobs")
    # One job -> many applications
    applications = db.relationship("Application", back_populates="job")


class Application(db.Model):
    __tablename__ = "applications"

    application_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    job_id = db.Column(db.Integer, db.ForeignKey("jobs.job_id"))
    application_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.Enum(*STATUSES, name="status"))
    resume_version = db.Column(db.String(50))
    cover_letter_sent = db.Column(db.Boolean)
    interview_data = db.Column(db.JSON)  # e.g. {"date": "...", "time": "...", "type": "...", "notes": "..."}

    job = db.relationship("Job", back_populates="applications")


class Contact(db.Model):
    __tablename__ = "contacts"

    contact_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    company_id = db.Column(db.Integer, db.ForeignKey("companies.company_id"))
    contact_name = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    linkedin_url = db.Column(db.String(200))
    notes = db.Column(db.Text)

    company = db.relationship("Company", back_populates="contacts")
