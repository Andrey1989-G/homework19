from flask import request
from flask_restx import Resource, Namespace

from dao.model.user import UserSchema
from implemented import movie_service

users_ns = Namespace('users')

@users_ns.route('/')
class UsersView(Resource):
    def get(self):
        res = UserSchema(many=True).dump()

