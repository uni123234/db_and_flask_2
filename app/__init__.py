"""
Application factory for creating the Flask app instance.

This module sets up the Flask app and registers blueprints.
"""

from flask import Flask
from app.routes import bp

def create_app():
    """
    Create and configure the Flask app.

    Returns:
        Flask: The Flask application instance.
    """
    app = Flask(__name__)

    app.register_blueprint(bp, url_prefix="/")

    return app
