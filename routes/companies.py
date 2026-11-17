"""Companies CRUD."""
from flask import Blueprint, flash, redirect, render_template, request, url_for

from models import Company, db
from routes.helpers import text

bp = Blueprint("companies", __name__, url_prefix="/companies")


def fill_company(company, form):
    name = text(form, "company_name", 100)
    if not name:
        raise ValueError("Company name is required.")
    company.company_name = name
    company.industry = text(form, "industry", 50)
    company.website = text(form, "website", 200)
    company.city = text(form, "city", 50)
    company.state = text(form, "state", 50)
    company.notes = text(form, "notes")


@bp.route("/")
def list_companies():
    q = request.args.get("q", "").strip()
    query = Company.query
    if q:
        query = query.filter(Company.company_name.ilike(f"%{q}%"))
    companies = query.order_by(Company.company_name).all()
    return render_template("companies/list.html", companies=companies, q=q)


@bp.route("/new", methods=["GET", "POST"])
def create():
    company = Company()
    if request.method == "POST":
        try:
            fill_company(company, request.form)
            db.session.add(company)
            db.session.commit()
            flash(f"Company '{company.company_name}' added.", "success")
            return redirect(url_for("companies.detail", company_id=company.company_id))
        except ValueError as e:
            db.session.rollback()
            flash(str(e), "error")
    return render_template("companies/form.html", company=company, form=request.form)


@bp.route("/<int:company_id>")
def detail(company_id):
    company = db.get_or_404(Company, company_id)
    return render_template("companies/detail.html", company=company)


@bp.route("/<int:company_id>/edit", methods=["GET", "POST"])
def edit(company_id):
    company = db.get_or_404(Company, company_id)
    if request.method == "POST":
        try:
            fill_company(company, request.form)
            db.session.commit()
            flash("Company updated.", "success")
            return redirect(url_for("companies.detail", company_id=company_id))
        except ValueError as e:
            db.session.rollback()
            flash(str(e), "error")
    return render_template("companies/form.html", company=company, form=request.form)


@bp.route("/<int:company_id>/delete", methods=["POST"])
def delete(company_id):
    company = db.get_or_404(Company, company_id)
    # Safe delete: refuse if other records still point at this company.
    if company.jobs or company.contacts:
        flash(f"Cannot delete '{company.company_name}': it still has {len(company.jobs)} job(s) and "
              f"{len(company.contacts)} contact(s). Delete or reassign those first.", "error")
        return redirect(url_for("companies.detail", company_id=company_id))
    db.session.delete(company)
    db.session.commit()
    flash("Company deleted.", "success")
    return redirect(url_for("companies.list_companies"))
