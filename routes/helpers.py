"""Small helpers shared by the route files for reading form values safely."""
from datetime import date, datetime


def text(form, name, max_len=None):
    value = (form.get(name) or "").strip()
    if max_len:
        value = value[:max_len]
    return value or None


def to_int(form, name):
    value = (form.get(name) or "").strip()
    if not value:
        return None
    try:
        return int(value)
    except ValueError:
        raise ValueError(f"{name.replace('_', ' ').title()} must be a whole number.")


def to_date(form, name):
    value = (form.get(name) or "").strip()
    if not value:
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError(f"{name.replace('_', ' ').title()} must be a valid date.")


def today():
    return date.today()
