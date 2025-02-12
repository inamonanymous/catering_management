from app.models import db
class Payments(db.Model):
    payment_id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    payment_status = db.Column(db.Enum('pending', 'completed', 'failed'), nullable=False, default='pending')
    payment_method = db.Column(db.Enum('gcash', 'maya'), nullable=False)
    reference_no = db.Column(db.String(20), unique=True, nullable=False)
    payment_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

    bookings = db.relationship('Bookings', backref='payments', lazy=True)

    @classmethod
    def delete_payment(cls, payment_id):
        try:
            target_payment = cls.query.filter_by(payment_id=payment_id).first()
            db.session.delete(target_payment)
            db.session.commit()
            return True
        except Exception as e:
            print(f"error at payments.delete_payment {e}")
            return False

    @classmethod
    def create_payment(cls, amount, payment_method, reference_no, payment_status='pending'):
        """Create a new payment record."""
        # Check if reference number already exists
        if cls.query.filter_by(reference_no=reference_no).first():
            raise ValueError("Reference number already exists.")
        
        # Create and add the payment to the session
        payment = cls(
            amount=amount,
            payment_method=payment_method,
            payment_status=payment_status,
            reference_no=reference_no
        )
        db.session.add(payment)
        db.session.commit()
        return payment

    @classmethod
    def get_payment_by_reference(cls, reference_no):
        """Retrieve a payment record by reference number."""
        return cls.query.filter_by(reference_no=reference_no).first()

    @classmethod
    def update_payment_status(cls, payment_id, new_status):
        """Update the payment status."""
        payment = cls.query.get(payment_id)
        if payment:
            payment.payment_status = new_status
            db.session.commit()
            return payment
        return None