"""Job Match logic. Plain Python so it can be tested without a database."""


def parse_skills(text):
    """Turn 'Python, SQL , python' into ['Python', 'SQL'] (trimmed, no duplicates, case-insensitive)."""
    if not text:
        return []
    if isinstance(text, list):
        items = text
    else:
        items = str(text).split(",")
    result, seen = [], set()
    for item in items:
        skill = str(item).strip()
        if skill and skill.lower() not in seen:
            seen.add(skill.lower())
            result.append(skill)
    return result


def match_skills(user_skills, job_skills):
    """Compare user skills with one job's required skills.

    Returns a dict with matched, missing, total and percent.
    Match % = matched required skills / total required skills * 100.
    A job with no requirements returns 0% (no division by zero).
    """
    user_set = {s.lower() for s in parse_skills(user_skills)}
    required = parse_skills(job_skills)
    matched = [s for s in required if s.lower() in user_set]
    missing = [s for s in required if s.lower() not in user_set]
    total = len(required)
    percent = round(len(matched) / total * 100) if total else 0
    return {"matched": matched, "missing": missing, "total": total, "percent": percent}


def rank_jobs(user_skills, jobs):
    """Score a list of Job objects and sort them from highest to lowest match."""
    results = []
    for job in jobs:
        requirements = job.requirements if isinstance(job.requirements, list) else []
        score = match_skills(user_skills, requirements)
        score["job"] = job
        results.append(score)
    results.sort(key=lambda r: (r["percent"], len(r["matched"])), reverse=True)
    return results
