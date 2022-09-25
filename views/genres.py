from flask import request
from flask_restx import Resource, Namespace

from dao.model.genre import GenreSchema
from implemented import genre_service
from service.decorators import auth_required, role_required

genre_ns = Namespace('genres')


@genre_ns.route('/')
class GenresView(Resource):
    @auth_required
    def get(self):
        rs = genre_service.get_all()
        res = GenreSchema(many=True).dump(rs)
        return res, 200

    @role_required
    def post(self):
        req_json = request.json
        if genre_service.create(req_json):
            return 'create genre', 200
        else:
            return 'invalid', 201

@genre_ns.route('/<int:rid>')
class GenreView(Resource):
    @auth_required
    def get(self, rid):
        r = genre_service.get_one(rid)
        sm_d = GenreSchema().dump(r)
        return sm_d, 200

    @role_required
    def put(self, rid):
        req_json = request.json
        if req_json['id'] == rid:
            genre_service.update(req_json)
            return f'update {req_json["name"]}', 204
        else:
            return 'invalid', 201

    @role_required
    def delete(self, rid):
        genre_service.delete(rid)
        return 'delete', 201
