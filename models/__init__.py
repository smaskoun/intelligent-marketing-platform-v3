"""
Model package initialisation.

This module defines a single instance of SQLAlchemy that should be
imported by all other models to avoid creating multiple database
objects.  Import `db` from this package whenever you need the
database object.
"""

from flask_sqlalchemy import SQLAlchemy

# Global SQLAlchemy instance used throughout the application
db = SQLAlchemy()

__all__ = ["db"]