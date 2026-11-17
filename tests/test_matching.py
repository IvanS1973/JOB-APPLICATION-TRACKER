"""Unit tests for the Job Match calculation (no database needed)."""
from types import SimpleNamespace

from matching import match_skills, parse_skills, rank_jobs


def test_full_match_is_100_percent():
    r = match_skills("Python, SQL, Flask", ["Python", "SQL", "Flask"])
    assert r["percent"] == 100
    assert r["matched"] == ["Python", "SQL", "Flask"]
    assert r["missing"] == []


def test_two_of_three_is_67_percent_and_reports_missing():
    r = match_skills("Python, SQL, Flask", ["Python", "SQL", "Tableau"])
    assert r["percent"] == 67
    assert r["total"] == 3
    assert r["missing"] == ["Tableau"]


def test_case_and_whitespace_are_ignored():
    r = match_skills("  python ,sql  ", ["Python", "SQL"])
    assert r["percent"] == 100


def test_duplicates_are_counted_once():
    assert parse_skills("Python, python, PYTHON, SQL") == ["Python", "SQL"]
    r = match_skills("Python, Python", ["Python", "python", "SQL"])
    assert r["total"] == 2
    assert r["percent"] == 50


def test_job_without_requirements_does_not_divide_by_zero():
    assert match_skills("Python", [])["percent"] == 0
    assert match_skills("Python", None)["percent"] == 0


def test_empty_user_input_gives_zero():
    assert parse_skills("") == []
    assert parse_skills(" , ,, ") == []
    assert match_skills("", ["Python"])["percent"] == 0


def test_one_of_four_is_25_percent():
    assert match_skills("Linux", ["Linux", "AWS", "Networking", "Python"])["percent"] == 25


def test_rank_jobs_sorts_highest_first():
    jobs = [
        SimpleNamespace(job_title="Low", requirements=["Java", "C#"]),
        SimpleNamespace(job_title="Full", requirements=["Python", "SQL"]),
        SimpleNamespace(job_title="Half", requirements=["Python", "Go"]),
        SimpleNamespace(job_title="Broken", requirements="not a list"),
    ]
    titles = [r["job"].job_title for r in rank_jobs("python, sql", jobs)]
    assert titles[:2] == ["Full", "Half"]
