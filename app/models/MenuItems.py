from app.models import db
class MenuItems(db.Model):
    item_id = db.Column(db.Integer, primary_key=True)
    menu_id = db.Column(db.Integer, db.ForeignKey('menu.menu_id'), nullable=False)
    category = db.Column(db.Enum('appetizer', 'main', 'drink', 'dessert', 'custom'))
    item_name = db.Column(db.String(100), nullable=False)
    
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