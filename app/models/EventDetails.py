from app.models import db
from app.models.Bookings import Bookings
from app.models.Payments import Payments
class EventDetails(db.Model):
    event_id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(100), nullable=False)
    number_of_guests = db.Column(db.Integer, nullable=False)
    event_date = db.Column(db.DateTime, nullable=False)
    food_time = db.Column(db.Time, nullable=False)
    event_location = db.Column(db.String(255), nullable=False)
    event_theme = db.Column(db.String(40), nullable=False)
    event_color = db.Column(db.String(40), nullable=False)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    @classmethod
    def get_user_bookings_with_events(cls, user_id):
        return (
            db.session.query(
                Bookings.booking_id,
                Bookings.status,
                Bookings.paid_amount,
                Bookings.total_price,
                Bookings.payment_id,
                Payments.payment_status,  # Get the actual payment status
                cls.event_id,
                cls.event_name,
                cls.event_date,
                cls.food_time,
                cls.event_location
            )
            .join(cls, cls.event_id == Bookings.event_id)
            .outerjoin(Payments, Payments.payment_id == Bookings.payment_id)  # Join Payments table
            .filter(Bookings.user_id == user_id)
            .all()
        )

    @classmethod
    def delete_event_details(cls, event_id):
        # Check if there are any bookings left for the event
        bookings = Bookings.query.filter_by(event_id=event_id).all()
        
        if not bookings:  # Only delete the event if no bookings are associated
            event = cls.query.get(event_id)
            if event:
                db.session.delete(event)
                db.session.commit()
                return True
        return False

    # Removed booking_id, now booking_id is stored in the Booking model (through event_id)
    @classmethod
    def insert(cls, event_name, number_of_guests, event_date, food_time, event_location, event_theme, event_color):
        new_event = cls(
            event_name=event_name,
            number_of_guests=number_of_guests,
            event_date=event_date,
            food_time=food_time,
            event_location=event_location,
            event_theme=event_theme,
            event_color=event_color
        )
        db.session.add(new_event)
        db.session.commit()
        return new_event
    