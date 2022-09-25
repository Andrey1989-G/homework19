import jwt
from flask import request, abort

from config import Config
from implemented import user_service


def auth_required(func):
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)
        data = request.headers['Authorization']
        token = data.split("Bearer ")[-1]
        try:
            jwt.decode(token, Config.SECRET_HERE, algorithm=Config.algo)
        except Exception as e:
            print(f"Traceback: {e}")
            abort(401)
        return func(*args, **kwargs)

    return wrapper


def role_required(func):
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)
        data = request.headers['Authorization']
        token = data.split("Bearer ")[-1]
        # проверяем на админа
        try:
            # извлекаем имя пользователя
            data = jwt.decode(token, Config.SECRET_HERE, algorithm=Config.algo)
            user = user_service.get_one(data.get('username'))
            if user != user.role('admin'):
                print('denied')
                abort(401)

        except Exception as e:
            print(f"Traceback: {e}")
            abort(401)

        return func(*args, **kwargs)

    return wrapper
