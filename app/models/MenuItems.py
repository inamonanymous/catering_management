from app.models import db
class MenuItems(db.Model):
    item_id = db.Column(db.Integer, primary_key=True)
    menu_id = db.Column(db.Integer, db.ForeignKey('menu.menu_id'), nullable=False)
    category = db.Column(db.Enum('appetizer', 'main', 'drink', 'dessert', 'custom'))
    item_name = db.Column(db.String(100), nullable=False)