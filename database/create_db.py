import psycopg2
import hashlib
from datetime import datetime, timedelta
from db_connection import get_connection

def create_database():
    conn = get_connection()
    if not conn:
        print("Не удалось подключиться к базе данных.")
        return

    cur = conn.cursor()

    # Таблица пользователей (для авторизации)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(256) NOT NULL,
            role VARCHAR(20) NOT NULL DEFAULT 'user'
        )
    """)

    # Таблица сотрудников
    cur.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            employee_id SERIAL PRIMARY KEY,
            surname VARCHAR(50) NOT NULL,
            name VARCHAR(50) NOT NULL,
            patronymic VARCHAR(50),
            phone VARCHAR(20)
        )
    """)

    # Таблица клиентов
    cur.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            client_id SERIAL PRIMARY KEY,
            surname VARCHAR(50) NOT NULL,
            name VARCHAR(50) NOT NULL,
            patronymic VARCHAR(50),
            phone VARCHAR(20),
            birth_date DATE
        )
    """)

    # Таблица типов абонементов
    cur.execute("""
        CREATE TABLE IF NOT EXISTS subscription_types (
            type_id SERIAL PRIMARY KEY,
            title VARCHAR(100) NOT NULL,
            description TEXT,
            price DECIMAL(10,2) NOT NULL,
            duration_days INT,
            max_visits INT
        )
    """)

    # Таблица абонементов (привязанных к клиентам)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS subscriptions (
            subscription_id SERIAL PRIMARY KEY,
            client_id INTEGER REFERENCES clients(client_id) ON DELETE CASCADE,
            type_id INTEGER REFERENCES subscription_types(type_id),
            employee_id INTEGER REFERENCES employees(employee_id),
            sale_date DATE NOT NULL,
            start_date DATE NOT NULL,
            end_date DATE,
            visits_remaining INT,
            status VARCHAR(20) DEFAULT 'active'
        )
    """)

    # Таблица посещений
    cur.execute("""
        CREATE TABLE IF NOT EXISTS visits (
            visit_id SERIAL PRIMARY KEY,
            client_id INTEGER REFERENCES clients(client_id) ON DELETE CASCADE,
            subscription_id INTEGER REFERENCES subscriptions(subscription_id),
            employee_id INTEGER REFERENCES employees(employee_id),
            visit_date DATE NOT NULL
        )
    """)

    # --- Добавление тестовых данных ---

    # Пользователи (пароли хранятся в захешированном виде)
    users = [
        ("admin", "admin123", "admin"),
        ("manager", "manager123", "manager"),
        ("user", "user123", "user")
    ]
    for username, password, role in users:
        try:
            pwd_hash = hashlib.sha256(password.encode()).hexdigest()
            cur.execute(
                "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
                (username, pwd_hash, role)
            )
            print(f"Пользователь {username} ({role}) создан")
        except psycopg2.Error:
            print(f"Пользователь {username} уже существует")

    # Сотрудники
    employees = [
        ("Иванова", "Мария", "Петровна", "+79001234567"),
        ("Петров", "Сергей", "Иванович", "+79007654321")
    ]
    for emp in employees:
        cur.execute("""
            INSERT INTO employees (surname, name, patronymic, phone)
            VALUES (%s, %s, %s, %s)
        """, emp)

    # Клиенты
    clients = [
        ("Сидоров", "Алексей", "Викторович", "+79111111111", "1990-05-15"),
        ("Кузнецова", "Елена", "Андреевна", "+79222222222", "1985-08-22"),
        ("Смирнов", "Дмитрий", "Олегович", "+79333333333", "1995-12-10")
    ]
    for client in clients:
        cur.execute("""
            INSERT INTO clients (surname, name, patronymic, phone, birth_date)
            VALUES (%s, %s, %s, %s, %s)
        """, client)

    # Типы абонементов
    types = [
        ("Месячный", "Безлимит на 30 дней", 2500.00, 30, None),
        ("Годовой", "Безлимит на 365 дней", 20000.00, 365, None),
        ("10 посещений", "10 тренировок без ограничения по времени", 1500.00, None, 10),
        ("Разовое", "Одно посещение", 300.00, None, 1)
    ]
    for t in types:
        cur.execute("""
            INSERT INTO subscription_types (title, description, price, duration_days, max_visits)
            VALUES (%s, %s, %s, %s, %s)
        """, t)

    # Абонементы (продажи) – добавим для теста
    # Сначала получим id клиентов, сотрудников, типов
    cur.execute("SELECT client_id FROM clients ORDER BY client_id")
    client_ids = [row[0] for row in cur.fetchall()]
    cur.execute("SELECT employee_id FROM employees ORDER BY employee_id")
    employee_ids = [row[0] for row in cur.fetchall()]
    cur.execute("SELECT type_id, duration_days, max_visits FROM subscription_types")
    type_data = cur.fetchall()

    for i, client_id in enumerate(client_ids):
        type_id, dur_days, max_vis = type_data[i % len(type_data)]
        start_date = datetime.now().date()
        end_date = start_date + timedelta(days=dur_days) if dur_days else None
        visits_rem = max_vis if max_vis else None

        cur.execute("""
            INSERT INTO subscriptions (client_id, type_id, employee_id, sale_date, start_date, end_date, visits_remaining, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, 'active')
        """, (client_id, type_id, employee_ids[i % len(employee_ids)], start_date, start_date, end_date, visits_rem))

    # Посещения (тестовые)
    cur.execute("SELECT client_id, subscription_id FROM subscriptions")
    subs = cur.fetchall()
    for client_id, sub_id in subs[:2]:  # первые два клиента
        cur.execute("""
            INSERT INTO visits (client_id, subscription_id, employee_id, visit_date)
            VALUES (%s, %s, %s, %s)
        """, (client_id, sub_id, employee_ids[0], datetime.now().date() - timedelta(days=2)))

    conn.commit()
    cur.close()
    conn.close()
    print("База данных успешно создана и заполнена тестовыми данными.")

if __name__ == "__main__":
    create_database()