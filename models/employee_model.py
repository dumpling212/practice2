from .base_model import BaseModel

class EmployeeModel(BaseModel):
    table_name = "employees"
    id_field = "employee_id"

    @classmethod
    def add(cls, surname, name, patronymic, phone):
        conn = cls.get_connection()
        if not conn:
            return False
        cur = conn.cursor()
        try:
            cur.execute("""
                INSERT INTO employees (surname, name, patronymic, phone)
                VALUES (%s, %s, %s, %s)
            """, (surname, name, patronymic, phone))
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
    def update(cls, employee_id, surname, name, patronymic, phone):
        conn = cls.get_connection()
        if not conn:
            return False
        cur = conn.cursor()
        try:
            cur.execute("""
                UPDATE employees
                SET surname=%s, name=%s, patronymic=%s, phone=%s
                WHERE employee_id=%s
            """, (surname, name, patronymic, phone, employee_id))
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            print(e)
            return False
        finally:
            cur.close()
            conn.close()