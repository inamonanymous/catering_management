from app.models.Payments import Payments
from app.models.Packages import Packages
from app.models.EventDetails import EventDetails
from app.models import db
from flask import session, url_for
def remove_booking_parent_rows(event_id, package_id, payment_id):
    try:
        # Remove associated payment if it exists
        if payment_id:
            payment = Payments.query.get(payment_id)
            if payment:
                db.session.delete(payment)

        # Remove associated package if it exists
        if package_id:
            package = Packages.query.get(package_id)
            if package:
                db.session.delete(package)

        # Remove event details
        if event_id:
            event = EventDetails.query.get(event_id)
            if event:
                db.session.delete(event)

        db.session.commit()
        return True  # Successfully removed parent rows

    except Exception as e:
        db.session.rollback()  # Rollback in case of error
        raise Exception(f"Error removing parent rows: {str(e)}")

