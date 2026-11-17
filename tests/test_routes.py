"""Route tests: CRUD for all four tables, relationships, validation and dashboard counts."""
from datetime import date

from models import Application, Company, Contact, Job, db


def make_company(name="TechCorp"):
    c = Company(company_name=name, industry="Software", city="Austin", state="TX")
    db.session.add(c)
    db.session.commit()
    return c


def make_job(company, title="Software Developer", skills=("Python", "SQL", "Flask")):
    j = Job(company_id=company.company_id, job_title=title, job_type="Full-time",
            salary_min=70000, salary_max=90000, requirements=list(skills))
    db.session.add(j)
    db.session.commit()
    return j


# ---------- Pages load ----------
def test_all_six_pages_load(client):
    for url in ["/", "/companies/", "/jobs/", "/applications/", "/contacts/", "/match/"]:
        assert client.get(url).status_code == 200, url


# ---------- Companies ----------
def test_company_crud(client):
    r = client.post("/companies/new", data={"company_name": "DataCo", "city": "Chicago"}, follow_redirects=True)
    assert b"DataCo" in r.data
    c = Company.query.filter_by(company_name="DataCo").one()

    client.post(f"/companies/{c.company_id}/edit", data={"company_name": "DataCo Inc"})
    assert db.session.get(Company, c.company_id).company_name == "DataCo Inc"

    assert b"DataCo Inc" in client.get("/companies/?q=dataco").data
    assert b"DataCo Inc" not in client.get("/companies/?q=zzz").data

    client.post(f"/companies/{c.company_id}/delete")
    assert db.session.get(Company, c.company_id) is None


def test_company_requires_name(client):
    r = client.post("/companies/new", data={"company_name": "  "})
    assert b"Company name is required" in r.data
    assert Company.query.count() == 0


def test_company_with_jobs_is_not_deleted(client):
    c = make_company()
    make_job(c)
    r = client.post(f"/companies/{c.company_id}/delete", follow_redirects=True)
    assert b"Cannot delete" in r.data
    assert db.session.get(Company, c.company_id) is not None


# ---------- Jobs ----------
def test_job_crud_and_skills_saved_as_json_list(client):
    c = make_company()
    client.post("/jobs/new", data={"job_title": "Data Analyst", "company_id": c.company_id, "job_type": "Full-time",
                                   "salary_min": "60000", "salary_max": "75000",
                                   "requirements": "Python, SQL , Tableau, python"})
    j = Job.query.filter_by(job_title="Data Analyst").one()
    assert j.requirements == ["Python", "SQL", "Tableau"]
    assert j.company.company_name == "TechCorp"

    client.post(f"/jobs/{j.job_id}/edit", data={"job_title": "Senior Data Analyst", "company_id": c.company_id,
                                               "job_type": "Contract", "requirements": "SQL"})
    j = db.session.get(Job, j.job_id)
    assert j.job_title == "Senior Data Analyst" and j.job_type == "Contract" and j.requirements == ["SQL"]

    assert b"Senior Data Analyst" in client.get("/jobs/?job_type=Contract").data
    assert b"Senior Data Analyst" not in client.get("/jobs/?job_type=Internship").data

    client.post(f"/jobs/{j.job_id}/delete")
    assert db.session.get(Job, j.job_id) is None


def test_job_salary_min_greater_than_max_is_rejected(client):
    c = make_company()
    r = client.post("/jobs/new", data={"job_title": "X", "company_id": c.company_id,
                                       "salary_min": "90000", "salary_max": "50000"})
    assert b"Minimum salary cannot be greater" in r.data
    assert Job.query.count() == 0


def test_job_requires_existing_company(client):
    r = client.post("/jobs/new", data={"job_title": "X", "company_id": "999"})
    assert b"existing company" in r.data


def test_job_with_applications_is_not_deleted(client):
    j = make_job(make_company())
    db.session.add(Application(job_id=j.job_id, application_date=date(2026, 10, 1), status="Applied"))
    db.session.commit()
    client.post(f"/jobs/{j.job_id}/delete")
    assert db.session.get(Job, j.job_id) is not None


# ---------- Applications ----------
def test_application_crud_with_interview_json(client):
    j = make_job(make_company())
    client.post("/applications/new", data={"job_id": j.job_id, "application_date": "2026-10-03", "status": "Interview",
                                           "resume_version": "v2", "cover_letter_sent": "on",
                                           "interview_date": "2099-01-15", "interview_time": "10:00",
                                           "interview_type": "Video", "interview_notes": "Bring demo"})
    a = Application.query.one()
    assert a.job.company.company_name == "TechCorp"
    assert a.cover_letter_sent is True
    assert a.interview_data == {"date": "2099-01-15", "time": "10:00", "type": "Video", "notes": "Bring demo"}

    r = client.get("/applications/?status=Interview")
    assert b"Software Developer" in r.data and b"TechCorp" in r.data
    assert b"Software Developer" not in client.get("/applications/?status=Offer").data

    client.post(f"/applications/{a.application_id}/edit", data={"job_id": j.job_id, "application_date": "2026-10-03",
                                                                "status": "Offer"})
    a = db.session.get(Application, a.application_id)
    assert a.status == "Offer" and a.interview_data is None and a.cover_letter_sent is False

    client.post(f"/applications/{a.application_id}/delete")
    assert Application.query.count() == 0


def test_application_requires_date_and_valid_status(client):
    j = make_job(make_company())
    assert b"Application date is required" in client.post("/applications/new", data={"job_id": j.job_id}).data
    r = client.post("/applications/new", data={"job_id": j.job_id, "application_date": "2026-10-01", "status": "Hired"})
    assert b"Invalid status" in r.data
    assert Application.query.count() == 0


def test_applications_sort_by_date(client):
    j = make_job(make_company())
    db.session.add_all([
        Application(job_id=j.job_id, application_date=date(2026, 1, 1), status="Applied", resume_version="OLDEST"),
        Application(job_id=j.job_id, application_date=date(2026, 6, 1), status="Applied", resume_version="NEWEST"),
    ])
    db.session.commit()
    desc = client.get("/applications/?sort=desc").data
    asc = client.get("/applications/?sort=asc").data
    assert desc.index(b"NEWEST") < desc.index(b"OLDEST")
    assert asc.index(b"OLDEST") < asc.index(b"NEWEST")


# ---------- Contacts ----------
def test_contact_crud_and_search_by_company(client):
    c = make_company("BrightPath")
    client.post("/contacts/new", data={"contact_name": "Alex Rivera", "company_id": c.company_id,
                                       "email": "alex@brightpath.example"})
    ct = Contact.query.one()
    assert ct.company.company_name == "BrightPath"
    assert b"Alex Rivera" in client.get("/contacts/?q=bright").data
    assert b"Alex Rivera" in client.get("/contacts/?q=alex").data

    client.post(f"/contacts/{ct.contact_id}/edit", data={"contact_name": "Alex R.", "company_id": c.company_id})
    assert db.session.get(Contact, ct.contact_id).contact_name == "Alex R."

    client.post(f"/contacts/{ct.contact_id}/delete")
    assert Contact.query.count() == 0
    assert db.session.get(Company, c.company_id) is not None  # company is untouched


def test_contact_rejects_bad_email(client):
    c = make_company()
    r = client.post("/contacts/new", data={"contact_name": "A", "company_id": c.company_id, "email": "not-an-email"})
    assert b"valid email" in r.data


# ---------- Dashboard ----------
def test_dashboard_counts_update(client):
    import re

    def stat(html, label):
        m = re.search(rf'stat-label">{label}</span><span class="stat-value">(\d+)', html)
        return int(m.group(1))

    html = client.get("/").get_data(as_text=True)
    assert stat(html, "Companies") == 0
    c = make_company()
    j = make_job(c)
    db.session.add(Application(job_id=j.job_id, application_date=date(2026, 10, 1), status="Interview",
                               interview_data={"date": "2099-05-01"}))
    db.session.commit()
    html = client.get("/").get_data(as_text=True)
    assert stat(html, "Companies") == 1
    assert stat(html, "Jobs") == 1
    assert stat(html, "Applications") == 1
    assert stat(html, "Upcoming Interviews") == 1


# ---------- Job Match page ----------
def test_job_match_page_ranks_database_jobs(client):
    tech, data = make_company("TechCorp"), make_company("DataCo")
    make_job(data, "Data Analyst", ["Python", "SQL", "Tableau"])
    make_job(tech, "Software Developer", ["Python", "SQL", "Flask"])
    html = client.post("/match/", data={"skills": "python, SQL, flask"}).get_data(as_text=True)
    assert "100%" in html and "67%" in html
    assert html.index("Software Developer") < html.index("Data Analyst")
    assert "Tableau" in html


def test_job_match_empty_input_shows_error(client):
    assert b"at least one skill" in client.post("/match/", data={"skills": " , "}).data


def test_delete_requires_csrf_token_when_enabled(app):
    app.config["WTF_CSRF_ENABLED"] = True
    c = make_company()
    r = app.test_client().post(f"/companies/{c.company_id}/delete")
    assert r.status_code == 400
    assert db.session.get(Company, c.company_id) is not None
