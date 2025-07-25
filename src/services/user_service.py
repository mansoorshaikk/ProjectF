from ..repositories.user_repository import UserRepository

class UserService:
    def __init__(self):
        self.user_repository = UserRepository()

    def signup_user(self,email,password,role):
        user = self.user_repository.signup_user(email, password,role)
        return user

    def login_user(self,email,password):
        user = self.user_repository.login_user(email,password)
        return user

    def current_user(self,session_token):
        user = self.user_repository.current_user(session_token)
        return user

