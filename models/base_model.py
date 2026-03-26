import psycopg2
from database.db_connection import get_connection

class BaseModel:
    table_name = None

    @classmethod
    def get_connection(cls):
        return get_connection()

    @classmethod
    def get_all(cls, order_by=None):
        conn = cls.get_connection()
        if not conn:
            return []
        cur = conn.cursor()
        query = f"SELECT * FROM {cls.table_name}"
        if order_by:
            query += f" ORDER BY {order_by}"
        cur.execute(query)
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows

    @classmethod
    def get_by_id(cls, record_id):
        conn = cls.get_connection()
        if not conn:
            return None
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {cls.table_name} WHERE {cls.id_field}=%s", (record_id,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        return row

    @classmethod
    def delete(cls, record_id):
        conn = cls.get_connection()
        if not conn:
            return False
        cur = conn.cursor()
        try:
            cur.execute(f"DELETE FROM {cls.table_name} WHERE {cls.id_field}=%s", (record_id,))
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            print(e)
            return False
        finally:
            cur.close()
            conn.close()