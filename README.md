# Информационная система "Учет абонементов в фитнес-клубе"

## Описание
Автоматизация фитнес-клуба: учет клиентов, абонементов, посещений, отчеты. Разграничение прав (admin/manager/user).

## Технологии
- Python 3.8+
- PyQt5 (GUI)
- PostgreSQL (БД)
- psycopg2, python-docx

## Структура проекта
```
fitness_club_system/
├── database/
│   ├── db_connection.py      # подключение к БД
│   └── create_db.py          # создание таблиц и тестовых данных
├── models/                   # CRUD-модели (client, subscription, visit, user и др.)
├── gui/                      # окна (login, register, main_menu, client_window, admin_panel и др.)
├── main.py                   # точка входа
```

## Установка и запуск

### 1. Установите PostgreSQL и создайте БД
```sql
CREATE DATABASE fitness_club_db;
```

### 2. Настройте подключение в `database/db_connection.py`
```python
host="localhost"
dbname="fitness_club_db"
user="postgres"
password="12345"
```

### 3. Создайте таблицы и тестовые данные
```bash
python database/create_db.py
```

### 4. Запустите приложение
```bash
python main.py
```

## Тестовые учетные записи
| Логин | Пароль | Роль |
|-------|--------|------|
| admin | admin123 | admin |
| manager | manager123 | manager |
| user | user123 | user |

## Основные функции
- **Клиенты**: добавление, редактирование, удаление
- **Абонементы**: продажа, продление, проверка активности
- **Посещения**: регистрация с автоматическим списанием
- **Отчеты**: активные/истекающие абонементы, продажи, посещаемость (экспорт в Word)
- **Администрирование**: управление пользователями и ролями (только admin)

