from flask import Flask, session, redirect, request, url_for, render_template
from dotenv import load_dotenv
import os


load_dotenv()
def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=os.getenv("FLASK_SECRET_KEY")
    )
    if not app.secret_key:
        raise ValueError("FLASK_SECRET_KEY environment variable is not set.")       # Ensure the environment variable is set or provide a default value
    return app


