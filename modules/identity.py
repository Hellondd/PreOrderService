from database import User
from werkzeug.security import check_password_hash, generate_password_hash

class IdentityModule:
    @staticmethod
    def hash_password(password):
        return generate_password_hash(password)

    @staticmethod
    def authenticate(username, password):
        user = User.query.filter_by(username=username).first()
        # Проверяем хэш вместо прямого сравнения строк
        if user and check_password_hash(user.password, password):
            return user
        return None