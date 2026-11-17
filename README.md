# Job Application Tracker

A small web app I built to keep my job search organized: the companies I'm interested in, the jobs they've posted,
where I've applied, and the people I've talked to. It also has a **Job Match** page that shows how well my skills
line up with each job.

Built with Python (Flask), MySQL 8, and plain HTML/CSS/JavaScript.

---

## What's inside

```
app.py          starts the app
config.py       reads your database login from .env
models.py       the four tables, written as Python classes
matching.py     the Job Match logic
routes/         one file per page (dashboard, companies, jobs, applications, contacts, match)
templates/      the HTML pages
static/         styles and a little JavaScript
schema.sql      creates the database
seed.sql        adds sample data
tests/          automated tests
```

## How the tables connect

```
companies ──< jobs ──< applications
    │
    └──────< contacts
```

- A **company** can have many **jobs** and many **contacts**.
- A **job** can have many **applications**.
- An application knows its company by following its job.

To protect your data, you can't delete a company that still has jobs or contacts, or a job that still has
applications. The app tells you what to remove first.

Two columns hold JSON:
- `requirements` on jobs, e.g. `["Python", "SQL", "Flask"]`
- `interview_data` on applications, e.g. `{"date": "2026-12-02", "time": "10:00", "type": "Video"}`

## Getting it running (Windows)

**You'll need:** Python 3.10+ (tick "Add to PATH" when installing), MySQL 8 with MySQL Workbench, and VS Code.

1. **Open the folder** in VS Code and open a terminal (*Terminal → New Terminal*).
2. **Set up Python:**
   ```powershell
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. **Create the database:** in MySQL Workbench, open and run `schema.sql`, then `seed.sql`
   (*File → Open SQL Script*, then click the ⚡ button). Running `schema.sql` again resets everything.
4. **Add your password:** copy `.env.example` to `.env` and put your MySQL password in `DB_PASSWORD`.
   This keeps it out of the code, so don't share this file.
5. **Start it:**
   ```powershell
   python app.py
   ```
   Then open **http://127.0.0.1:5000**.
6. **Run the tests:** `pytest`. They use their own temporary database, so your data is safe.

## How it works

- **Flask and MySQL:** `config.py` builds the connection, and SQLAlchemy turns Python code into SQL.
  For example, `Company.query.all()` runs `SELECT * FROM companies`.
- **Forms:** each form sends its fields to Flask. Flask checks them (required fields, valid dates, salary range,
  a real company or job) and then saves and shows a success message. If something's wrong, it explains the problem
  and keeps what you typed. Every form has a security token (CSRF), and the app asks you to confirm before deleting anything.
- **Skills:** type `Python, SQL, Flask`. The app trims the spaces, drops duplicates, and saves it as a JSON list.
- **Job Match:** for each job, *match % = skills you have ÷ skills the job needs × 100*.
  For example, Python, SQL and Flask against a job that needs Python, SQL and Tableau is 2 of 3, which is **67%**,
  with Tableau missing. A job with no listed skills scores 0% instead of crashing. Results are sorted best first.
- **Dashboard:** every number is counted live from MySQL each time you open the page.

## Quick demo

1. Open the Dashboard. You'll see 5 companies, 7 jobs, 6 applications and 5 contacts.
2. Add a company, then a job for it with a few skills.
3. Try a minimum salary above the maximum. It's rejected.
4. Add an application with a future interview date. "Upcoming Interviews" goes up.
5. Try deleting TechCorp. It's blocked because it still has jobs and contacts.
6. On Job Match, enter `Python, SQL, Flask`. Software Developer comes out at 100%, Data Analyst at 67%.
7. Make the window narrow. The layout switches to mobile.

## If something goes wrong

| You see | Try this |
|---|---|
| `python is not recognized` | Reinstall Python with "Add to PATH" ticked, or use `py` |
| `No module named 'flask'` | Activate the venv, then `pip install -r requirements.txt` |
| `Access denied for user 'root'` | Check the password in `.env` |
| `Unknown database 'job_tracker'` | Run `schema.sql` first |
| `Can't connect to MySQL server` | Start the **MySQL80** service in Windows Services |
| PowerShell won't activate the venv | Run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once |
| `CSRF token is missing` | Refresh the page and submit again |
