"""Dashboard: every number here is counted from MySQL at request time."""
from flask import Blueprint, render_template
from sqlalchemy import func

from models import Application, Company, Contact, Job, STATUSES, db
from routes.helpers import today

bp = Blueprint("dashboard", __name__)


@bp.route("/")
def index():
    totals = {
        "companies": db.session.query(func.count(Company.company_id)).scalar(),
        "jobs": db.session.query(func.count(Job.job_id)).scalar(),
        "applications": db.session.query(func.count(Application.application_id)).scalar(),
        "contacts": db.session.query(func.count(Contact.contact_id)).scalar(),
    }

    # SELECT status, COUNT(*) FROM applications GROUP BY status
    rows = db.session.query(Application.status, func.count(Application.application_id)).group_by(Application.status).all()
    counts = {status: count for status, count in rows}
    by_status = [{"status": s, "count": counts.get(s, 0)} for s in STATUSES]
    max_count = max([s["count"] for s in by_status] + [1])

    recent = Application.query.order_by(Application.application_date.desc(), Application.application_id.desc()).limit(5).all()

    # Upcoming interviews: interview_data JSON has a "date" on or after today
    upcoming = []
    now = today().isoformat()
    for app_row in Application.query.filter(Application.interview_data.isnot(None)).all():
        data = app_row.interview_data or {}
        if isinstance(data, dict) and data.get("date") and data["date"] >= now:
            upcoming.append(app_row)
    upcoming.sort(key=lambda a: (a.interview_data.get("date"), a.interview_data.get("time") or ""))

    return render_template("dashboard.html", totals=totals, by_status=by_status, max_count=max_count,
                           recent=recent, upcoming=upcoming)
