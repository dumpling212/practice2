from .base_model import BaseModel

class ClientModel(BaseModel):
    table_name = "clients"
    id_field = "client_id"

    @classmethod
    def add(cls, surname, name, patronymic, phone, birth_date):
        conn = cls.get_connection()
        if not conn:
            return False
        cur = conn.cursor()
        try:
            cur.execute("""
                INSERT INTO clients (surname, name, patronymic, phone, birth_date)
                VALUES (%s, %s, %s, %s, %s)
            """, (surname, name, patronymic, phone, birth_date))
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
    def update(cls, client_id, surname, name, patronymic, phone, birth_date):
        conn = cls.get_connection()
        if not conn:
            return False
        cur = conn.cursor()
        try:
            cur.execute("""
                UPDATE clients SET surname=%s, name=%s, patronymic=%s, phone=%s, birth_date=%s
                WHERE client_id=%s
            """, (surname, name, patronymic, phone, birth_date, client_id))
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            print(e)
            return False
        finally:
            cur.close()
            conn.close()