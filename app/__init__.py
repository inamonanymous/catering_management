from flask import Flask, render_template, session
from app.main import main
from app.config import AppConfig

def create_app():
    app = Flask(__name__)
    app.register_blueprint(main)
    app.config.from_object(AppConfig)
    return app