import hashlib
import psycopg2
from .base_model import BaseModel

class UserModel(BaseModel):
    table_name = "users"
    id_field = "user_id"

    @classmethod
    def authenticate(cls, username, password):
        conn = cls.get_connection()
        if not conn:
            return None
        cur = conn.cursor()
        pwd_hash = hashlib.sha256(password.encode()).hexdigest()
        cur.execute("SELECT user_id, username, role FROM users WHERE username=%s AND password=%s",
                    (username, pwd_hash))
        user = cur.fetchone()
        cur.close()
        conn.close()
        return user

    @classmethod
    def change_password(cls, user_id, old_password, new_password):
        conn = cls.get_connection()
        if not conn:
            return False
        cur = conn.cursor()
        old_hash = hashlib.sha256(old_password.encode()).hexdigest()
        cur.execute("SELECT user_id FROM users WHERE user_id=%s AND password=%s",
                    (user_id, old_hash))
        if not cur.fetchone():
            cur.close()
            conn.close()
            return False
        new_hash = hashlib.sha256(new_password.encode()).hexdigest()
        cur.execute("UPDATE users SET password=%s WHERE user_id=%s", (new_hash, user_id))
        conn.commit()
        cur.close()
        conn.close()
        return True

    @classmethod
    def register(cls, username, password, role='user'):
        conn = cls.get_connection()
        if not conn:
            return False
        cur = conn.cursor()
        pwd_hash = hashlib.sha256(password.encode()).hexdigest()
        try:
            cur.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
                        (username, pwd_hash, role))
            conn.commit()
            return True
        except psycopg2.IntegrityError:
            conn.rollback()
            return False
        finally:
            cur.close()
            conn.close()