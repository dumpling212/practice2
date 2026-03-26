from .base_model import BaseModel

class SubscriptionModel(BaseModel):
    table_name = "subscriptions"
    id_field = "subscription_id"

    @classmethod
    def add(cls, client_id, type_id, employee_id, sale_date, start_date, end_date, visits_remaining):
        conn = cls.get_connection()
        if not conn:
            return False
        cur = conn.cursor()
        try:
            cur.execute("""
                INSERT INTO subscriptions (client_id, type_id, employee_id, sale_date, start_date, end_date, visits_remaining, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, 'active')
            """, (client_id, type_id, employee_id, sale_date, start_date, end_date, visits_remaining))
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
    def update(cls, subscription_id, client_id, type_id, employee_id, sale_date, start_date, end_date, visits_remaining, status):
        conn = cls.get_connection()
        if not conn:
            return False
        cur = conn.cursor()
        try:
            cur.execute("""
                UPDATE subscriptions
                SET client_id=%s, type_id=%s, employee_id=%s, sale_date=%s, start_date=%s, end_date=%s, visits_remaining=%s, status=%s
                WHERE subscription_id=%s
            """, (client_id, type_id, employee_id, sale_date, start_date, end_date, visits_remaining, status, subscription_id))
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
    def get_active_for_client(cls, client_id):
        conn = cls.get_connection()
        if not conn:
            return []
        cur = conn.cursor()
        cur.execute("""
            SELECT s.* FROM subscriptions s
            WHERE s.client_id = %s AND s.status = 'active'
              AND (s.end_date IS NULL OR s.end_date >= CURRENT_DATE)
              AND (s.visits_remaining IS NULL OR s.visits_remaining > 0)
            ORDER BY s.subscription_id
        """, (client_id,))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows

    @classmethod
    def use_visit(cls, subscription_id, employee_id, visit_date):
        conn = cls.get_connection()
        if not conn:
            return False
        cur = conn.cursor()
        try:
            # Уменьшаем visits_remaining, если абонемент с лимитом
            cur.execute("""
                UPDATE subscriptions
                SET visits_remaining = visits_remaining - 1
                WHERE subscription_id = %s AND visits_remaining IS NOT NULL AND visits_remaining > 0
            """, (subscription_id,))
            # Добавляем запись о посещении
            cur.execute("""
                INSERT INTO visits (client_id, subscription_id, employee_id, visit_date)
                SELECT client_id, %s, %s, %s FROM subscriptions WHERE subscription_id = %s
            """, (subscription_id, employee_id, visit_date, subscription_id))
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
            SELECT s.subscription_id, c.surname || ' ' || c.name AS client_name,
                   st.title AS type_name, e.surname || ' ' || e.name AS employee_name,
                   s.sale_date, s.start_date, s.end_date, s.visits_remaining, s.status
            FROM subscriptions s
            JOIN clients c ON s.client_id = c.client_id
            JOIN subscription_types st ON s.type_id = st.type_id
            JOIN employees e ON s.employee_id = e.employee_id
            ORDER BY s.subscription_id
        """)
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows