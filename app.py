"""Entry point. Run with:  python app.py"""
from flask import Flask, render_template
from flask_wtf.csrf import CSRFProtect

from config import Config
from models import db

csrf = CSRFProtect()


def create_app(config_object=Config):
    app = Flask(__name__)
    app.config.from_object(config_object)

    db.init_app(app)
    csrf.init_app(app)

    from routes.dashboard import bp as dashboard_bp
    from routes.companies import bp as companies_bp
    from routes.jobs import bp as jobs_bp
    from routes.applications import bp as applications_bp
    from routes.contacts import bp as contacts_bp
    from routes.match import bp as match_bp

    app.register_blueprint(dashboard_bp)
    app.register_blueprint(companies_bp)
    app.register_blueprint(jobs_bp)
    app.register_blueprint(applications_bp)
    app.register_blueprint(contacts_bp)
    app.register_blueprint(match_bp)

    @app.errorhandler(404)
    def not_found(e):
        return render_template("error.html", code=404, message="Page not found."), 404

    @app.errorhandler(500)
    def server_error(e):
        db.session.rollback()
        return render_template("error.html", code=500, message="Something went wrong on the server."), 500

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
