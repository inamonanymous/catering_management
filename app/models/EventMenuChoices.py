from app.models import db

class EventMenuChoices(db.Model):
    choice_id = db.Column(db.Integer, primary_key=True)
    menu_id = db.Column(db.Integer, db.ForeignKey('menu.menu_id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event_details.event_id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)

    @classmethod
    def delete_choices_by_event_id(cls, event_id):
        try:
            # Delete all menu choices associated with the given event_id
            deleted_count = cls.query.filter_by(event_id=event_id).delete()
            db.session.commit()  # Commit the changes to the database
            return deleted_count  # Return the number of rows deleted
        except Exception as e:
            db.session.rollback()  # Rollback in case of error
            raise Exception(f"Error deleting event menu choices: {str(e)}")

    @classmethod
    def update_booking_total_price(cls, event_id):
        # Query to get all the event menu choices for the given event
        event_menu_choices = db.session.query(EventMenuChoices).filter_by(event_id=event_id).all()

        # Calculate total price
        total_price = 0
        for choice in event_menu_choices:
            # Query the Menu table directly using db.session.query
            menu = db.session.query('menu').filter_by(menu_id=choice.menu_id).first()
            if menu:
                total_price += menu.price * choice.quantity
        
        # Query the Bookings table directly using db.session.query
        booking = db.session.query('bookings').filter_by(event_id=event_id).first()
        if booking:
            booking.total_price = total_price
            db.session.commit()

    @classmethod
    def get_all_choices_by_event_id(cls, event_id):
        return cls.query.filter_by(event_id=event_id).all()

    @classmethod
    def insert(cls, menu_id, event_id, quantity=1):
        new_choice = cls(
            menu_id=menu_id,
            event_id=event_id,
            quantity=quantity
        )
        db.session.add(new_choice)
        db.session.commit()
        return new_choice
    
    @classmethod
    def update_choice_quantity(cls, choice_id, quantity):
        target_choice = cls.query.get(choice_id)
        if target_choice:
            target_choice.quantity = quantity
            db.session.commit()  # Ensure the change is saved
        return target_choice

    
    @classmethod
    def delete_choice(cls, choice_id):
        target_choice = cls.query.filter_by(choice_id=choice_id).first()
        db.session.delete(target_choice)
        db.session.commit()
        return True
