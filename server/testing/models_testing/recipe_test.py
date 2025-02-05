import pytest
from sqlalchemy.exc import IntegrityError
from models import User, Recipe  # Import the User and Recipe models
from app import app
from models import db, Recipe

class TestRecipe:
    '''Recipe in models.py'''

    def test_has_attributes(self):
        '''has attributes title, instructions, and minutes_to_complete.'''

    with app.app_context():

        # Clear existing data
        Recipe.query.delete()
        User.query.delete()
        db.session.commit()

        # Create a user
        user = User(
            username="testuser",
            _password_hash="hashedpassword",  # Provide a valid password hash
            image_url="http://example.com/image.jpg",
            bio="Test bio"
        )
        db.session.add(user)
        db.session.commit()

        # Create a recipe associated with the user
        recipe = Recipe(
            title="Delicious Shed Ham",
            instructions="""Or kind rest bred with am shed then. In""" + \
                """ raptures building an bringing be. Elderly is detract""" + \
                """ tedious assured private so to visited. Do travelling""" + \
                """ companions contrasted it. Mistress strongly remember""" + \
                """ up to. Ham him compass you proceed calling detract.""" + \
                """ Better of always missed we person mr. September""" + \
                """ smallness northward situation few her certainty""" + \
                """ something.""",
            minutes_to_complete=60,
            user_id=user.id  # Associate the recipe with the user
        )

        db.session.add(recipe)
        db.session.commit()

    def test_requires_title(self):
        '''requires each record to have a title.'''

        with app.app_context():

            Recipe.query.delete()
            db.session.commit()

            recipe = Recipe()
            
            with pytest.raises(IntegrityError):
                db.session.add(recipe)
                db.session.commit()

    def test_requires_50_plus_char_instructions(self):
        '''requires instructions to be at least 50 characters long.'''

        with app.app_context():

            Recipe.query.delete()
            db.session.commit()

            # Must raise either a sqlalchemy.exc.IntegrityError or a custom ValueError
            with pytest.raises((IntegrityError, ValueError)):
                recipe = Recipe(
                    title="Generic Ham",
                    instructions="idk lol")  # Not enough characters
                db.session.add(recipe)
                db.session.commit()
