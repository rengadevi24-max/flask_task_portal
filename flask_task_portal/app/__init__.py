from flask import Flask, render_template
from config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    from app.books.routes import books_bp
    from app.members.routes import members_bp
    from app.reservations.routes import reservations_bp

    app.register_blueprint(books_bp, url_prefix="/books")
    app.register_blueprint(members_bp, url_prefix="/members")
    app.register_blueprint(reservations_bp, url_prefix="/reservations")

    @app.get("/")
    def home():
        return render_template("home.html")

    @app.errorhandler(404)
    def not_found(error):
        return render_template("error.html", message="Page not found."), 404

    return app
