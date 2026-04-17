import json
import re
from werkzeug.security import generate_password_hash, check_password_hash

class AuthService:
    def __init__(self, filename="users.txt"):
        self.filename = filename
        self.users = self.load_users()

    def load_users(self):
        try:
            with open(self.filename, "r") as file:
                return json.load(file)
        except:
            return {}

    def save_users(self):
        with open(self.filename, "w") as file:
            json.dump(self.users, file, indent=4)

    # 🔐 PASSWORD VALIDATION
    def validate_password(self, password):
        if len(password) < 6:
            raise ValueError("Password must be at least 6 characters")

        if password.lower() in ["1234", "password", "admin"]:
            raise ValueError("Password too weak")

        if not re.search(r"[A-Z]", password):
            raise ValueError("Must contain uppercase letter")

        if not re.search(r"[a-z]", password):
            raise ValueError("Must contain lowercase letter")

        if not re.search(r"[0-9]", password):
            raise ValueError("Must contain a number")

    # LOGIN
    def login(self, username, password):
        self.users = self.load_users()

        if username not in self.users:
            raise ValueError("User not found")

        user = self.users[username]

        if not check_password_hash(user["password"], password):
            raise ValueError("Incorrect password")

        print("Login Successful!")

        if user.get("first_login"):
            return {"username": username, **user, "force_change": True}

        return {"username": username, **user}

    # CHANGE PASSWORD
    def change_password(self, username, new_password):
        self.validate_password(new_password)

        self.users[username]["password"] = generate_password_hash(new_password)
        self.users[username]["first_login"] = False
        self.save_users()

    # AUTO CREATE USER
    def create_user_for_student(self, student_id, name):
        self.users = self.load_users()

        username = str(student_id)

        if username not in self.users:
            self.users[username] = {
                "password": generate_password_hash("1234"),
                "role": "user",
                "student_id": student_id,
                "first_login": True,
                "name": name
            }

            self.save_users()

    # Reset password to default 
    def reset_password(self, username):
        from werkzeug.security import generate_password_hash

        if username not in self.users:
            raise ValueError("User not found")

        self.users[username]["password"] = generate_password_hash("1234")
        self.users[username]["first_login"] = True

        self.save_users()