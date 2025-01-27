from app.models import db
class Menu(db.Model):
    menu_id = db.Column(db.Integer, primary_key=True)
    menu_name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

    menu_items = db.relationship('MenuItems', backref='menu', lazy=True)