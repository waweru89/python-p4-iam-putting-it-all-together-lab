from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from sqlalchemy.exc import IntegrityError

from config import db, bcrypt

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    _password_hash = db.Column(db.String)
    image_url = db.Column(db.String)
    bio = db.Column(db.String)

    recipes = db.relationship('Recipe', back_populates = 'user')
    serialize_rules = ('-recipes.user', '-recipes.user_id')

    @hybrid_property
    def password_hash(self):
        # return self._password_hash
        raise AttributeError('Password_hash should not be accessed')

    @password_hash.setter
    def password_hash(self, new_password):
        hashed = bcrypt.generate_password_hash(new_password.encode('utf-8'))
        self._password_hash = hashed.decode('utf-8')

    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password)


class Recipe(db.Model, SerializerMixin):
    __tablename__ = 'recipes'
    
    id = db.Column(db.Integer, primary_key=True) 
    title = db.Column(db.String, nullable=False)
    instructions = db.Column(db.String)
    # instructions = db.Column(db.String, db.CheckConstraint('LENGTH(instructions) > 50'))
    minutes_to_complete = db.Column(db.Integer) 
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('User', back_populates = 'recipes')
    serialize_rules = ('-user.recipes',)
    __table_args__ = (db.CheckConstraint('LENGTH(instructions) > 50'),)
    # @validates('instructions')
    # def valid_instructions(self, key, value):
    #     if len(value) < 50:
    #         raise ValueError('Instructions must be more than 50 characters.')
    #     return value

    @validates('title')
    def valid_title(self, key, value):
        if not value:
            raise IntegrityError('Title must be present.')
        return value