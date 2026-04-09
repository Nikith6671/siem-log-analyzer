import psycopg2
import bcrypt
from db import connect_db

# 🔐 Hash password
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

# 🔑 Verify password
def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

# ➕ Create user
def create_user(username, password, role="user"):
    conn = connect_db()
    cur = conn.cursor()

    hashed = hash_password(password)

    cur.execute(
        "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
        (username, hashed, role)
    )

    conn.commit()
    cur.close()
    conn.close()

# 🔍 Authenticate user
def authenticate(username, password):
    conn = connect_db()
    cur = conn.cursor()

    cur.execute(
        "SELECT password, role FROM users WHERE username=%s",
        (username,)
    )

    result = cur.fetchone()

    cur.close()
    conn.close()

    if result:
        stored_password, role = result
        if verify_password(password, stored_password):
            return role

    return None