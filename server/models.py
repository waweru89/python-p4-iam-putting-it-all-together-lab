from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin
from config import db, bcrypt

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    _password_hash = db.Column(db.String(255), nullable=False)
    image_url = db.Column(db.String(255))
    bio = db.Column(db.String(500))

    # One-to-many relationship: User has many recipes
    recipes = db.relationship('Recipe', backref='user', lazy=True)

    # Validates username length
    @validates('username')
    def validate_username(self, key, username):
        if len(username) < 3:
            raise ValueError("Username must be at least 3 characters long.")
        return username

    # Password hashing
    @hybrid_property
    def password(self):
        raise AttributeError("Password is not accessible directly")

    @password.setter
    def password(self, password):
        self._password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    # Password verification
    def check_password(self, password):
        return bcrypt.check_password_hash(self._password_hash, password)

class Recipe(db.Model, SerializerMixin):
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False, unique=True)
    instructions = db.Column(db.String, nullable=False)
    minutes_to_complete = db.Column(db.Integer, nullable=False)

    # Foreign key to link Recipe to User
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Validates instructions length
    @validates('instructions')
    def validate_instructions(self, key, value):
        if len(value) < 50:
            raise ValueError('Instructions must be at least 50 characters long.')
        return value