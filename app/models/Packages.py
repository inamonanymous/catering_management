from app.models import db

class Packages(db.Model):
    package_id = db.Column(db.Integer, primary_key=True)
    package_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    image_path = db.Column(db.String(255))
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

    bookings = db.relationship('Bookings', backref='package', lazy=True)

    @classmethod
    def add_package(cls, package_name, description, price, image_path=None):
        try:
            package = cls(package_name=package_name, description=description, price=price, image_path=image_path)
            db.session.add(package)
            db.session.commit()
            return package
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error adding package: {e}")

    @classmethod
    def update_package(cls, package_id, package_name=None, description=None, price=None):
        try:
            package = cls.query.get(package_id)
            if not package:
                raise Exception("Package not found")
            
            if package_name:
                package.package_name = package_name
            if description:
                package.description = description
            if price:
                package.price = price
            
            db.session.commit()
            return package
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error updating package: {e}")

    @classmethod
    def delete_package(cls, package_id):
        try:
            package = cls.query.get(package_id)
            if not package:
                return {'error': 'Package not found'}, 404
            
            db.session.delete(package)
            db.session.commit()
            return {'success': True, 'message': 'Package deleted successfully.'}, 200
        except Exception as e:
            db.session.rollback()
            return {'error': f'Error deleting package: {e}'}, 500

    @classmethod
    def get_all_packages(cls):
        try:
            return cls.query.all()
        except Exception as e:
            raise Exception(f"Error fetching packages: {e}")