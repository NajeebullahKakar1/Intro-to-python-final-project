"""app.py - Entry point for the Library Management Web App."""
from flask import Flask
from config import Config
from database import init_db
import routes.auth_routes as auth_routes
import routes.book_routes as book_routes
import routes.borrow_routes as borrow_routes
import routes.admin_routes as admin_routes
import routes.api_routes as api_routes

def create_app():
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config.from_object(Config)
    init_db(app.config["DATABASE"])
    app.register_blueprint(auth_routes.bp)
    app.register_blueprint(book_routes.bp)
    app.register_blueprint(borrow_routes.bp)
    app.register_blueprint(admin_routes.bp)
    app.register_blueprint(api_routes.bp)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
