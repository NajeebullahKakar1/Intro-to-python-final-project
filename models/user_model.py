from database import query
from config import Config
DB = Config.DATABASE

def create_user(username, password, role="user"):
    return query(DB, "INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, password, role))

def get_user_by_username(username):
    return query(DB, "SELECT * FROM users WHERE username=?", (username,), fetchone=True)

def get_all_users():
    return query(DB, "SELECT id, username, role FROM users", fetchall=True)

def update_user(user_id, username, role):
    return query(DB, "UPDATE users SET username=?, role=? WHERE id=?", (username, role, user_id))

def delete_user(user_id):
    return query(DB, "DELETE FROM users WHERE id=?", (user_id,))
