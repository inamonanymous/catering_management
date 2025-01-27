from app.models import db
from werkzeug.security import generate_password_hash, check_password_hash

class Users(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    firstname = db.Column(db.String(255), nullable=False)
    middlename = db.Column(db.String(255), nullable=False)
    lastname = db.Column(db.String(255), nullable=False)
    suffix = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone_number = db.Column(db.String(100), unique=True, nullable=False)
    phone_number2 = db.Column(db.String(100))
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    role = db.Column(db.Enum('admin', 'customer'), nullable=False)

    bookings = db.relationship('Bookings', backref='user', lazy=True)

    @classmethod
    def get_all_users(cls):
        """
        Retrieves all users from the database.

        :return: A list of `Users` objects.
        """
        try:
            return cls.query.all()
        except Exception as e:
            raise Exception(f"An error occurred while fetching users: {e}")

    @classmethod
    def auth_user(cls, username, password):
        """
        Authenticates a user with the provided username and password.

        :param username: The username to authenticate.
        :param password: The plain-text password to verify.
        :return: The authenticated `Users` object if successful, or None if authentication fails.
        """
        try:
            user = cls.query.filter_by(username=username).first()
            if user and check_password_hash(user.password_hash, password):
                return user
            return None
        except Exception as e:
            raise Exception(f"An error occurred during authentication: {e}")

    @classmethod
    def create_user(cls, username, password, firstname, middlename, lastname, suffix, email, phone_number, role, phone_number2=None):
        """
        Creates and inserts a new user into the database.
        
        :param username: User's username (string)
        :param password: Plain text password (string)
        :param firstname: User's first name (string)
        :param middlename: User's middle name (string)
        :param lastname: User's last name (string)
        :param suffix: User's name suffix (string)
        :param email: User's email address (string)
        :param phone_number: User's primary phone number (string)
        :param role: User's role, must be either 'admin' or 'customer' (string)
        :param phone_number2: User's secondary phone number (optional, string)
        :return: The created `Users` object.
        """
        try:
            # Hash the password
            password_hash = generate_password_hash(password)

            # Create user instance
            user = cls(
                username=username,
                password_hash=password_hash,
                firstname=firstname,
                middlename=middlename,
                lastname=lastname,
                suffix=suffix,
                email=email,
                phone_number=phone_number,
                phone_number2=phone_number2,
                role=role
            )

            # Add to database session
            db.session.add(user)
            db.session.commit()

            return user
        except Exception as e:
            db.session.rollback()
            raise Exception(f"An error occurred while creating the user: {e}")