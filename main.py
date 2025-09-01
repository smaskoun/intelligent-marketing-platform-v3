# main.py

from flask import Flask, render_template, send_from_directory
from flask_cors import CORS
import os

# Import the single database instance
from models.social_media import db

# Import the corrected blueprints
from routes.brand_voice_routes import brand_voice_bp
from routes.learning_algorithm_routes import learning_algorithm_bp
from routes.ab_testing_routes import ab_testing_bp
from routes.market_data_routes import market_data_bp

def create_app():
    """Create and configure the Flask application."""
    # Correctly set the static folder path
    app = Flask(__name__, static_folder='static')

    # --- Configuration ---
    db_url = os.environ.get('DATABASE_URL', 'sqlite:///local_dev.db')
    if db_url and db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    CORS(app)

    # --- Initialize Database ---
    db.init_app(app)

    # --- Register Blueprints ---
    app.register_blueprint(brand_voice_bp, url_prefix='/api/brand-voice')
    app.register_blueprint(learning_algorithm_bp, url_prefix='/api/learning')
    app.register_blueprint(ab_testing_bp, url_prefix='/api/ab-testing')
    app.register_blueprint(market_data_bp, url_prefix='/api/market-data')

    # --- THIS IS THE FIX ---
    # This route will now serve the main index.html file and handle all sub-paths
    # for a Single Page Application (SPA).
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve(path):
        if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
            return send_from_directory(app.static_folder, path)
        else:
            # Always serve index.html as the fallback for a SPA
            return send_from_directory(app.static_folder, 'index.html')
    # ---------------------

    # --- Create Database Tables ---
    with app.app_context():
        db.create_all()

    return app

# This part is for local development and can be ignored by Gunicorn
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
