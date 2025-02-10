from flask import Flask
from flask_migrate import Migrate
from app.main import main
import os
from app.config import AppConfig
from app.models import db
from app.models.Bookings import Bookings
from app.models.EventDetails import EventDetails
from app.models.EventMenuChoices import EventMenuChoices
from app.models.Menu import Menu
from app.models.MenuItems import MenuItems
from app.models.Packages import Packages
from app.models.Payments import Payments
from app.models.Users import Users

def create_app():
    app = Flask(__name__)
    app.register_blueprint(main)
    app.config.from_object(AppConfig)
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'uploads')
    db.init_app(app)
    Migrate(app, db)

    with app.app_context():
        Bookings,
        EventDetails,
        EventMenuChoices,
        Menu,
        MenuItems,
        Packages,
        Payments,
        Users
        db.create_all()

    return app