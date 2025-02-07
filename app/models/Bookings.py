from app.models import db
from app.models.EventMenuChoices import EventMenuChoices
from app.models.Payments import Payments

class Bookings(db.Model):
    booking_id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event_details.event_id'), nullable=True)  # Added event_id
    package_id = db.Column(db.Integer, db.ForeignKey('packages.package_id'), nullable=True)  # Added event_id
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    payment_id = db.Column(db.Integer, db.ForeignKey('payments.payment_id'))
    paid_amount = db.Column(db.Numeric(10, 2), default=0.0)
    total_price = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.Enum('to-pay', 'processing', 'completed'), default='to-pay')
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    
    event_details = db.relationship('EventDetails', backref='booking', uselist=False)  # Linking to EventDetails
    packages = db.relationship('Packages', backref='packages', uselist=False)  # Linking to Packages

    @classmethod
    def add_payment(cls, booking_id, payment_id, amount):
        """Add payment to booking and update paid_amount."""
        booking = cls.query.get(booking_id)
        if booking:
            booking.paid_amount += amount  # Add the paid amount to the total paid so far
            booking.payment_id = payment_id  # Optionally, store the payment ID (if needed)
            db.session.commit()
            return booking
        else:
            raise ValueError("Booking not found.")


    @classmethod
    def delete_booking_with_choices(cls, booking_id):
        try:
            # Get the booking by ID
            booking = cls.query.get_or_404(booking_id)

            # Delete all menu choices related to the event
            EventMenuChoices.delete_choices_by_event_id(booking.event_id)

            # Delete the booking record
            db.session.delete(booking)
            db.session.commit()

            return True  # Booking and choices were deleted successfully
        except Exception as e:
            db.session.rollback()  # Rollback in case of error
            raise Exception(f"Error deleting booking and its event menu choices: {str(e)}")

    @classmethod
    def get_all_bookings_by_booking_id(cls, booking_id):
        return cls.query.filter_by(booking_id=booking_id).all()
    
    @classmethod
    def get_all_bookings_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()

    @classmethod
    def get_booking_by_event_id(cls, event_id):
        return cls.query.filter_by(event_id=event_id).first()

    @classmethod
    def delete_booking(cls, booking_id):
        target_booking = cls.query.filter_by(booking_id=booking_id).first()
        db.session.delete(target_booking)
        db.session.commit()

    @classmethod
    def insert(cls, user_id, total_price, status, event_id=None, package_id=None):
        new_booking = cls(
            user_id=user_id,
            total_price=total_price,
            status=status,
            event_id=event_id
        )
        if package_id is not None:
            new_booking.package_id=package_id

        db.session.add(new_booking)
        db.session.commit()
        return new_booking