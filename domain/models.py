class User:
    def __init__(self, user_id, username, password):
        self.user_id = user_id
        self.username = username
        self.password = password  # En production, utilise bcrypt pour le hachage

    def verify_password(self, password):
        return self.password == password