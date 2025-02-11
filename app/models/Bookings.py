from app.models import db
from app.models.EventMenuChoices import EventMenuChoices
from app.models.Payments import Payments
from app.models.Menu import Menu

class Bookings(db.Model):
    booking_id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event_details.event_id'), nullable=True)  # Added event_id
    package_id = db.Column(db.Integer, db.ForeignKey('packages.package_id'), nullable=True)  # Added event_id
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    payment_id = db.Column(db.Integer, db.ForeignKey('payments.payment_id'), unique=True)
    paid_amount = db.Column(db.Numeric(10, 2), default=0.0)
    total_price = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.Enum('to-pay', 'processing', 'completed'), default='to-pay')
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    
    event_details = db.relationship('EventDetails', backref='booking', uselist=False)  # Linking to EventDetails
    packages = db.relationship('Packages', backref='packages', uselist=False)  # Linking to Packages

    @classmethod
    def update_booking_status_based_on_payment(cls, payment_id, new_payment_status, paid_amount):
        try:
            """Update the booking status based on the payment status."""
            booking = cls.query.filter_by(payment_id=payment_id).first()

            if not booking:
                return None
            if new_payment_status == "completed":
                booking.paid_amount = paid_amount
                booking.status = "processing"  # Move to 'processing' when payment is completed
            elif new_payment_status == "pending":
                booking.paid_amount = 0
                booking.status = "to-pay"  # Revert to 'to-pay' when payment goes back to pending
            db.session.commit()
            return booking
        except:
            return None


    @classmethod
    def remove_payment(cls, payment_id):
        try:
            target_booking = cls.query.filter_by(payment_id=payment_id).first()
            target_booking.payment_id = None
            target_booking.status = 'to-pay'
            db.session.commit()
            return target_booking
        except Exception as e:
            print(e)
            return None

    @classmethod
    def update_booking_total_price(cls, event_id):
        # Query to get all the event menu choices for the given event
        event_menu_choices = db.session.query(EventMenuChoices).filter_by(event_id=event_id).all()

        # Calculate total price
        total_price = 0
        for choice in event_menu_choices:
            # Query the Menu table directly using db.session.query
            menu = db.session.query(Menu).filter_by(menu_id=choice.menu_id).first()
            if menu:
                total_price += menu.price * choice.quantity
        
        # Query the Bookings table directly using db.session.query
        booking = cls.query.filter_by(event_id=event_id).first()
        if booking:
            booking.total_price = total_price
            db.session.commit()

    @classmethod
    def get_completed_payments_by_booking_id(cls, booking_id):
        """Retrieve completed payments for a given booking."""
        booking = cls.query.filter_by(booking_id=booking_id).first()
        if not booking:
            return None

        payment = Payments.query.filter_by(payment_id=booking.payment_id, payment_status='completed').first()
        return payment
    
    @classmethod
    def get_pending_payments_by_booking_id(cls, booking_id):
        """Retrieve completed payments for a given booking."""
        booking = cls.query.filter_by(booking_id=booking_id).first()
        if not booking:
            return None

        payment = Payments.query.filter_by(payment_id=booking.payment_id, payment_status='pending').first()
        return payment

    @classmethod
    def add_payment_to_booking(cls, booking_id, payment_id, amount=None):
        """Add payment to booking and update paid_amount."""
        booking = cls.query.get(booking_id)
        if not booking:
            raise ValueError("Booking not found.")
    
        if amount is not None:
            booking.paid_amount += amount  # Add the paid amount to the total paid so far
        
        booking.payment_id = payment_id  # Optionally, store the payment ID (if needed)
        db.session.commit()
        return booking


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