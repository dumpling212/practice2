from .base_model import BaseModel

class VisitModel(BaseModel):
    table_name = "visits"
    id_field = "visit_id"

    @classmethod
    def add(cls, client_id, subscription_id, employee_id, visit_date):
        conn = cls.get_connection()
        if not conn:
            return False
        cur = conn.cursor()
        try:
            cur.execute("""
                INSERT INTO visits (client_id, subscription_id, employee_id, visit_date)
                VALUES (%s, %s, %s, %s)
            """, (client_id, subscription_id, employee_id, visit_date))
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
    def update(cls, visit_id, client_id, subscription_id, employee_id, visit_date):
        conn = cls.get_connection()
        if not conn:
            return False
        cur = conn.cursor()
        try:
            cur.execute("""
                UPDATE visits
                SET client_id=%s, subscription_id=%s, employee_id=%s, visit_date=%s
                WHERE visit_id=%s
            """, (client_id, subscription_id, employee_id, visit_date, visit_id))
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
    def get_with_names(cls):
        conn = cls.get_connection()
        if not conn:
            return []
        cur = conn.cursor()
        cur.execute("""
            SELECT v.visit_id, c.surname || ' ' || c.name AS client_name,
                   st.title AS subscription_type, e.surname || ' ' || e.name AS employee_name,
                   v.visit_date
            FROM visits v
            JOIN clients c ON v.client_id = c.client_id
            JOIN subscriptions s ON v.subscription_id = s.subscription_id
            JOIN subscription_types st ON s.type_id = st.type_id
            JOIN employees e ON v.employee_id = e.employee_id
            ORDER BY v.visit_date DESC
        """)
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows