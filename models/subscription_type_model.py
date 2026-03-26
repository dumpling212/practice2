from .base_model import BaseModel

class SubscriptionTypeModel(BaseModel):
    table_name = "subscription_types"
    id_field = "type_id"

    @classmethod
    def add(cls, title, description, price, duration_days, max_visits):
        conn = cls.get_connection()
        if not conn:
            return False
        cur = conn.cursor()
        try:
            cur.execute("""
                INSERT INTO subscription_types (title, description, price, duration_days, max_visits)
                VALUES (%s, %s, %s, %s, %s)
            """, (title, description, price, duration_days, max_visits))
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            print(e)
            return False
        finally:
            cur.close()
            conn.close()

    @classmethod
    def update(cls, type_id, title, description, price, duration_days, max_visits):
        conn = cls.get_connection()
        if not conn:
            return False
        cur = conn.cursor()
        try:
            cur.execute("""
                UPDATE subscription_types
                SET title=%s, description=%s, price=%s, duration_days=%s, max_visits=%s
                WHERE type_id=%s
            """, (title, description, price, duration_days, max_visits, type_id))
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            print(e)
            return False
        finally:
            cur.close()
            conn.close()