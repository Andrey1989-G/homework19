import calendar
import datetime

import jwt
from flask import request, abort
from flask_restx import Resource, Namespace

from config import Config
from dao.model.user import UserSchema
from implemented import user_service
from service.decorators import auth_required

auth_ns = Namespace('auth')


@auth_ns.route('/')
class AuthView(Resource):
    def post(self):
        # получает логин и пароль из Body запроса в виде JSON
        req_json = request.json
        # получаем значения логина, пароля
        username = req_json.get('username', None)
        password = req_json.get('password', None)
        # проверка наличия пользователя
        res = UserSchema(many=True).dump(user_service.get_all())
        if username not in res['username']:
            return 'неверный логин', 401

        # проверка пароля
        # сперва получим хэш любезно предоставленной функцией
        password_hash = user_service.get_hash(password)
        if password_hash not in res['password']:
            return 'ошибка ввода пароля', 401

        access_token = jwt.encode(req_json, Config.SECRET_HERE, algorithm=Config.algo)

        refresh_token = jwt.encode(req_json, Config.SECRET_HERE, algorithm=Config.algo)

        return {"access_token": access_token, "refresh_token": refresh_token}

    def put(self):
        # получает refresh_token из Body запроса в виде JSON
        req_json = request.json
        refresh_token = req_json.get('refresh_token')
        # проверка на наличие отсутствия
        if refresh_token is None:
            abort(400)

        # декодируем рефреш токен
        try:
            data = jwt.decode(jwt=refresh_token, key=Config.SECRET_HERE, algorithms=[Config.algo])
        except Exception as e:
            abort(400)
        # получаем пользователя и извлекаем его с бд
        username = data.get('username')
        user = (UserSchema(many=True).dump(user_service.get_all())).filter(UserSchema.username == username).first()
        data = {
            "username": user.username,
            "role": user.role
        }
        # генерируем токены
        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data["exp"] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, Config.SECRET_HERE, algorithm=Config.algo)
        days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
        data["exp"] = calendar.timegm(days130.timetuple())
        refresh_token = jwt.encode(data, Config.SECRET_HERE, algorithm=Config.algo)
        tokens = {"access_token": access_token, "refresh_token": refresh_token}

        return tokens, 201
