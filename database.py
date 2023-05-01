import json
import hashlib

class User:
    def __init__(self, login, password):
        self.login = login
        self.password_hash = hashlib.sha256(password.encode()).hexdigest()

    def check_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest() == self.password_hash

class Database:
    def __init__(self, filename):
        self.filename = filename
        self.load()

    def load(self):
        try:
            with open(self.filename, "r") as f:
                self.users = [User(**data) for data in json.load(f)]
        except FileNotFoundError:
            self.users = []

    def save(self):
        with open(self.filename, "w") as f:
            data = [vars(user) for user in self.users]
            json.dump(data, f)

    def find_user(self, login):
        for user in self.users:
            if user.login == login:
                return user
        return None

    def add_user(self, login, password):
        user = User(login, password)
        self.users.append(user)
        self.save()
