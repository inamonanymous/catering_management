from app.models import db
from app.models.EventMenuChoices import EventMenuChoices
from app.models.MenuItems import MenuItems
class Menu(db.Model):
    menu_id = db.Column(db.Integer, primary_key=True)
    menu_name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2), nullable=False)  # Price of the menu
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

    menu_items = db.relationship('MenuItems', backref='menu', lazy=True)

    @classmethod
    def get_available_menus_for_event(cls, event_id):
        # Get the menu_ids that have already been selected for the event
        selected_menu_ids = [choice.menu_id for choice in EventMenuChoices.get_all_choices_by_event_id(event_id)]
        
        # Return the menus that have not been selected
        return cls.query.filter(cls.menu_id.notin_(selected_menu_ids)).all()

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def delete_menu(cls, menu_id):
        try:
            target_menu = cls.query.filter_by(menu_id=menu_id).first()
            if target_menu is None:
                return False
            MenuItems.delete_items_by_menu_id(menu_id)
            db.session.delete(target_menu)
            db.session.commit()
            return True
        except Exception as e:
            print(f"cannot delete menu: {e}")
            return False

    @classmethod
    def insert(cls, menu_name, description=None, price=None):
        try:

            new_menu = cls(
                menu_name=menu_name,
                description=description,
                price=price
            )
            db.session.add(new_menu)
            db.session.commit()
            return new_menu
        except Exception as e:
            print(f"cannot insert menu {e}")
            return None
