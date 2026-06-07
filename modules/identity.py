import os
import logging
from werkzeug.security import check_password_hash, generate_password_hash
from database import User

logging.basicConfig(level=logging.INFO)
IS_DEBUG = os.getenv("DEBUG", "False") == "True"


class IdentityModule:
    @staticmethod
    def hash_password(password):
        return generate_password_hash(password)

    @staticmethod
    def authenticate(username, password):
        if IS_DEBUG:
            logging.info(f"DEBUG: Попытка входа пользователя: {username}")

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            return user
        return None
