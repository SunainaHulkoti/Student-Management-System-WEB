from werkzeug.security import generate_password_hash
import json

# Load users
with open("users.txt", "r") as f:
    users = json.load(f)

# Convert all passwords
for username in users:
    password = users[username]["password"]

    # Only hash if not already hashed
    if not password.startswith("pbkdf2:"):
        users[username]["password"] = generate_password_hash(password)

# Save back
with open("users.txt", "w") as f:
    json.dump(users, f, indent=4)

print("✅ All passwords converted to hashed format!")