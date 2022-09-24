import hashlib

from constants import PWD_HASH_ITERATIONS, PWD_HASH_SALT
from dao.user import UserDAO


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_one(self, uid):
        return self.dao.get_one(uid)

    def get_all(self):
        return self.dao.get_all()

    def create(self, data):
        return self.dao.create(data)

    def update(self, data):
        self.dao.update(data)

    def delete(self, uid):
        self.dao.delete(uid)

    def get_hash(password):
        return hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),  # Convert the password to bytes
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        ).decode("utf-8", "ignore")

    # def auth_required(self, func):
    #     def wrapper(*args, **kwargs):
    #         if 'Authorization' not in request.headers:
    #             abort(401)
    #         data = request.headers['Authorization']
    #         token = data.split("Bearer ")[-1]
    #         try:
    #             jwt.decode(token, Config.SECRET_HERE, algorithm=Config.algo)
    #         except Exception as e:
    #             print(f"Traceback: {e}")
    #             abort(401)
    #         return func(*args, **kwargs)
    #
    #     return wrapper
