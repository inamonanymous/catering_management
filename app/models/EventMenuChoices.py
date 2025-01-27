from app.models import db
class EventMenuChoices(db.Model):
    choice_id = db.Column(db.Integer, primary_key=True)
    menu_id = db.Column(db.Integer, db.ForeignKey('menu.menu_id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event_details.event_id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)