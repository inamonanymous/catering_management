from app.models import db
class MenuItems(db.Model):
    item_id = db.Column(db.Integer, primary_key=True)
    menu_id = db.Column(db.Integer, db.ForeignKey('menu.menu_id'), nullable=False)
    category = db.Column(db.Enum('appetizer', 'main', 'drink', 'dessert', 'custom'))
    item_name = db.Column(db.String(100), nullable=False)
    
    @classmethod
    def delete_item_by_item_id(cls, item_id):
        try:
            # Delete all menu choices associated with the given event_id
            deleted_count = cls.query.filter_by(item_id=item_id).delete()
            db.session.commit()  # Commit the changes to the database
            return deleted_count, 200  # Return the number of rows deleted
        except Exception as e:
            db.session.rollback()  # Rollback in case of error
            raise Exception(f"Error deleting event menu items: {str(e)}")
    
    @classmethod
    def delete_items_by_menu_id(cls, menu_id):
        try:
            # Delete all menu choices associated with the given event_id
            deleted_count = cls.query.filter_by(menu_id=menu_id).delete()
            db.session.commit()  # Commit the changes to the database
            return deleted_count  # Return the number of rows deleted
        except Exception as e:
            db.session.rollback()  # Rollback in case of error
            raise Exception(f"Error deleting event menu items: {str(e)}")

    @classmethod
    def insert(cls, menu_id, category, item_name):
        try:
            new_item = cls(
                menu_id=menu_id,
                category=category,
                item_name=item_name
            )
            db.session.add(new_item)
            db.session.commit()
            return new_item  # Return the created item
        except Exception as e:
            db.session.rollback()
            print(f"Error inserting menu item: {e}")
            return None