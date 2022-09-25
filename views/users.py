from flask import request
from flask_restx import Resource, Namespace

from dao.model.user import UserSchema
from implemented import user_service
from service.decorators import auth_required, role_required

users_ns = Namespace('users')

@users_ns.route('/')
class UsersView(Resource):
    @auth_required
    def get(self):
        res = UserSchema(many=True).dump(user_service.get_all())
        return res, 200


    def post(self):
        req_json = request.json
        req_json['password'] = user_service.get_hash(req_json['password'])
        user_service.create(req_json)
        return 'create user', 201


@users_ns.route('/<int:uid>')
class UserView(Resource):
    @auth_required
    def get(self, uid):
        res = UserSchema().dump(user_service.get_one(uid))
        return res, 200

    @role_required
    def put(self, uid):
        req_json = request.json
        if 'id' not in req_json:
            req_json['id'] = uid
        user_service.update(req_json)
        return 'update', 204

    @role_required
    def delete(self, uid):
        user_service.delete(uid)
        return 'delete', 204

