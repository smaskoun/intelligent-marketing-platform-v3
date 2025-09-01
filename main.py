"""
Application entry point.

This module provides a factory function `create_app()` used by Gunicorn
and the Flask CLI to create and configure the Flask application.  It
sets up the database, CORS, registers blueprints and serves static
files from the `static` directory.
"""

import os
from flask import Flask, send_from_directory
from flask_cors import CORS

from models import db
from routes.brand_voice import brand_voice_bp
from routes.learning_algorithm_routes import learning_algorithm_bp
from routes.ab_testing_routes import ab_testing_bp
from routes.market_data_routes import market_data_bp


def create_app() -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), "static"))
    app.config["SECRET_KEY"] = "a_very_secret_key_that_should_be_changed"

    # Configure SQLite database
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "database", "app.db")
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialise database
    db.init_app(app)
    CORS(app, origins="*")

    # Register blueprints
    app.register_blueprint(brand_voice_bp, url_prefix="/api/brand-voice")
    app.register_blueprint(learning_algorithm_bp, url_prefix="/api/learning")
    app.register_blueprint(ab_testing_bp, url_prefix="/api/ab-testing")
    app.register_blueprint(market_data_bp, url_prefix="/api/market-data")

    # Create tables
    with app.app_context():
        db.create_all()

    # Static file serving
    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def serve(path: str):
        """Serve the front‑end application."""
        static_folder = app.static_folder
        if path and os.path.exists(os.path.join(static_folder, path)):
            return send_from_directory(static_folder, path)
        # Fallback to index.html or placeholder if not present
        index_path = os.path.join(static_folder, "index.html")
        if os.path.exists(index_path):
            return send_from_directory(static_folder, "index.html")
        return "Welcome to Intelligent Marketing Platform v2", 200

    return app


if __name__ == "__main__":
    app = create_app()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
