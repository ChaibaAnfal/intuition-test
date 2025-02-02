# domain/users.py
from domain.models import User
from adapters.database_adapter import DatabaseAdapter

class UserService:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def sign_up(self, username, password):
        """
        Crée un nouvel utilisateur avec un ID unique.
        """
        if self.user_repository.find_user_by_username(username):
            raise ValueError("Cet utilisateur existe déjà.")
        user = User(user_id=self.user_repository.next_id(), username=username, password=password)
        self.user_repository.save_user(user)  # Utilise save_user au lieu de save
        return user

    def login(self, username, password):
        user = self.user_repository.find_user_by_username(username)
        if user and user.verify_password(password):
            return user
        raise ValueError("Nom d'utilisateur ou mot de passe incorrect.")