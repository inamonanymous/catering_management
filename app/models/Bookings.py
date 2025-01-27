from app.models import db
class Bookings(db.Model):
    booking_id = db.Column(db.Integer, primary_key=True)
    package_id = db.Column(db.Integer, db.ForeignKey('packages.package_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    event_details = db.Column(db.Text)
    status = db.Column(db.Enum('to-pay', 'processing', 'completed'), default='to-pay')
    price = db.Column(db.Numeric(10, 2), nullable=False)
    is_paid = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    event_details_relationship = db.relationship('EventDetails', backref='booking', lazy=True)
    payments = db.relationship('Payments', backref='booking', lazy=True)