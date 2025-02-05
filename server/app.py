#!/usr/bin/env python3

from flask import request, session
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from config import app, db, api
from models import User, Recipe

class Signup(Resource):
    def post(self):
        json = request.get_json()
        try:
            new_user = User(username = json.get('username'),
                            image_url = json.get('image_url'),
                            bio = json.get('bio'),
                            )
            new_user.password_hash = json.get('password')
            db.session.add(new_user)
            db.session.commit()
            session['user_id'] = new_user.id
            return new_user.to_dict(rules=('-recipes', '-_password_hash')), 201
        except IntegrityError as e:
            return {'error': str(e)}, 422

class CheckSession(Resource):
    def get(self):
        user_id = session.get('user_id')
        if user_id:
            user = User.query.filter_by(id=user_id).first()
            return user.to_dict(rules=('-recipes', '-_password_hash')), 200
        return {"error": "User not logged in"}, 401
            

class Login(Resource):
    def post(self):
        json = request.get_json()
        user = User.query.filter(User.username == json.get('username')).first()
        if not user or not user.authenticate(json.get('password')):
            return {'error': 'Invalid login'}, 401
        session['user_id'] = user.id
        return user.to_dict(rules=('-recipes', '-_password_hash')), 200

class Logout(Resource):
    def delete(self):
        if session['user_id']:
            session['user_id'] = None
            return {}, 204
        return {"error": "Not logged in"}, 401

class RecipeIndex(Resource):
    def get(self):
        if session.get('user_id'):
            recipes = [recipe.to_dict() for recipe in Recipe.query.all()]
            return recipes, 200
        return {'error': 'Not logged in'}, 401

    def post(self):
        json = request.get_json()
        try:
            new_recipe = Recipe(title = json.get('title'),
                                instructions = json.get('instructions'),
                                minutes_to_complete = json.get('minutes_to_complete'),
                                user_id = session.get('user_id'))
            db.session.add(new_recipe)
            db.session.commit()
            return new_recipe.to_dict(), 201
        except Exception as e:
            return {'error': str(e)}, 422

api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(CheckSession, '/check_session', endpoint='check_session')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')
api.add_resource(RecipeIndex, '/recipes', endpoint='recipes')


if __name__ == '__main__':
    app.run(port=5555, debug=True)