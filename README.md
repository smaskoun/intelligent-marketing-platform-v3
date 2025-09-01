# Intelligent Marketing Platform v2

This directory contains a cleaned‑up version of the original `intelligent‑marketing‑platform‑v2` repository.  The application is built with Flask and provides endpoints for brand‑voice training/analysis, learning algorithm recommendations, A/B testing, and real‑estate market data.

Major improvements include:

* Added missing `brand_voice` blueprint and simplified service for brand‑voice analysis/training.
* Removed stale `src` imports and normalised package structure with `__init__.py` files.
* Consolidated SQLAlchemy initialisation in `models/__init__.py` to avoid multiple database instances.
* Added `__init__.py` files to `routes` and `services` so relative imports work consistently.
* Updated imports throughout the project to use the unified package structure.

Follow the instructions below to set up and run the application locally or on Render.

## Requirements

Install Python 3.11+ and create a virtual environment.  Install dependencies with:

```bash
pip install -r requirements.txt
```

## Running locally

```bash
export FLASK_APP=main.py
flask run --host=0.0.0.0 --port=5000
```

Alternatively you can use Gunicorn to run the app in production mode:

```bash
gunicorn "main:create_app()"
```

The API will be available at `http://localhost:5000`.
