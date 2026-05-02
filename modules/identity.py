from database import User

class IdentityModule:
    @staticmethod
    def authenticate(username, password):
        # Жесткая проверка связки логин+пароль
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            return user
        return None