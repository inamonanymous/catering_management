from app.models import db
class Payments(db.Model):
    payment_id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.booking_id'), nullable=False)
    amount_paid = db.Column(db.Numeric(10, 2), nullable=False)
    payment_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    payment_method = db.Column(db.Enum('gcash', 'maya', 'bank_transfer'), nullable=False)