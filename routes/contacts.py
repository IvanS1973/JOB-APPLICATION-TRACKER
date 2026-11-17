"""Contacts CRUD."""
import re

from flask import Blueprint, flash, redirect, render_template, request, url_for

from models import Company, Contact, db
from routes.helpers import text, to_int

bp = Blueprint("contacts", __name__, url_prefix="/contacts")

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def fill_contact(contact, form):
    name = text(form, "contact_name", 100)
    if not name:
        raise ValueError("Contact name is required.")
    company_id = to_int(form, "company_id")
    if not company_id or not db.session.get(Company, company_id):
        raise ValueError("Please choose an existing company.")
    email = text(form, "email", 100)
    if email and not EMAIL_RE.match(email):
        raise ValueError("Please enter a valid email address.")
    contact.contact_name = name
    contact.company_id = company_id
    contact.title = text(form, "title", 100)
    contact.email = email
    contact.phone = text(form, "phone", 20)
    contact.linkedin_url = text(form, "linkedin_url", 200)
    contact.notes = text(form, "notes")


@bp.route("/")
def list_contacts():
    q = request.args.get("q", "").strip()
    query = Contact.query.outerjoin(Company)
    if q:
        like = f"%{q}%"
        query = query.filter(db.or_(Contact.contact_name.ilike(like), Company.company_name.ilike(like)))
    contacts = query.order_by(Contact.contact_name).all()
    return render_template("contacts/list.html", contacts=contacts, q=q)


def render_form(contact):
    companies = Company.query.order_by(Company.company_name).all()
    return render_template("contacts/form.html", contact=contact, companies=companies, form=request.form)


@bp.route("/new", methods=["GET", "POST"])
def create():
    contact = Contact(company_id=request.args.get("company_id", type=int))
    if request.method == "POST":
        try:
            fill_contact(contact, request.form)
            db.session.add(contact)
            db.session.commit()
            flash(f"Contact '{contact.contact_name}' added.", "success")
            return redirect(url_for("contacts.detail", contact_id=contact.contact_id))
        except ValueError as e:
            db.session.rollback()
            flash(str(e), "error")
    return render_form(contact)


@bp.route("/<int:contact_id>")
def detail(contact_id):
    contact = db.get_or_404(Contact, contact_id)
    return render_template("contacts/detail.html", contact=contact)


@bp.route("/<int:contact_id>/edit", methods=["GET", "POST"])
def edit(contact_id):
    contact = db.get_or_404(Contact, contact_id)
    if request.method == "POST":
        try:
            fill_contact(contact, request.form)
            db.session.commit()
            flash("Contact updated.", "success")
            return redirect(url_for("contacts.detail", contact_id=contact_id))
        except ValueError as e:
            db.session.rollback()
            flash(str(e), "error")
    return render_form(contact)


@bp.route("/<int:contact_id>/delete", methods=["POST"])
def delete(contact_id):
    contact = db.get_or_404(Contact, contact_id)
    db.session.delete(contact)
    db.session.commit()
    flash("Contact deleted.", "success")
    return redirect(url_for("contacts.list_contacts"))
