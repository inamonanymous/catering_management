from flask import Flask, render_template, session
from app.main import main


def create_app():
    app = Flask(__name__)
    app.register_blueprint(main)
    return app