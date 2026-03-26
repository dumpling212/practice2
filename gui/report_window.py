from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTextEdit, QDateEdit, QLabel, QHBoxLayout
from PyQt5.QtCore import QDate
from database.db_connection import get_connection
from models.subscription_model import SubscriptionModel
from models.visit_model import VisitModel
from models.client_model import ClientModel
from docx import Document
import os

class ReportWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Отчеты")
        self.resize(600, 500)

        layout = QVBoxLayout()

        self.report_text = QTextEdit()
        layout.addWidget(self.report_text)

        # Кнопки для отчетов
        btn_layout = QHBoxLayout()
        self.active_btn = QPushButton("Активные абонементы")
        self.active_btn.clicked.connect(self.active_report)
        btn_layout.addWidget(self.active_btn)

        self.expiring_btn = QPushButton("Скоро истекающие")
        self.expiring_btn.clicked.connect(self.expiring_report)
        btn_layout.addWidget(self.expiring_btn)

        layout.addLayout(btn_layout)

        # Отчет за период
        period_layout = QHBoxLayout()
        period_layout.addWidget(QLabel("С:"))
        self.start_date = QDateEdit()
        self.start_date.setDate(QDate.currentDate().addDays(-30))
        period_layout.addWidget(self.start_date)
        period_layout.addWidget(QLabel("По:"))
        self.end_date = QDateEdit()
        self.end_date.setDate(QDate.currentDate())
        period_layout.addWidget(self.end_date)
        self.sales_btn = QPushButton("Продажи за период")
        self.sales_btn.clicked.connect(self.sales_report)
        period_layout.addWidget(self.sales_btn)
        self.visits_btn = QPushButton("Посещаемость за период")
        self.visits_btn.clicked.connect(self.visits_report)
        period_layout.addWidget(self.visits_btn)
        layout.addLayout(period_layout)

        self.setLayout(layout)

    def active_report(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT c.surname, c.name, st.title, s.end_date, s.visits_remaining
            FROM subscriptions s
            JOIN clients c ON s.client_id = c.client_id
            JOIN subscription_types st ON s.type_id = st.type_id
            WHERE s.status = 'active' AND (s.end_date >= CURRENT_DATE OR s.end_date IS NULL)
              AND (s.visits_remaining > 0 OR s.visits_remaining IS NULL)
        """)
        rows = cur.fetchall()
        cur.close()
        conn.close()
        text = "Активные абонементы:\n\n"
        for row in rows:
            text += f"{row[0]} {row[1]} - {row[2]} (до {row[3]}, осталось {row[4] if row[4] else '∞'} посещ.)\n"
        self.report_text.setText(text)

    def expiring_report(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT c.surname, c.name, st.title, s.end_date
            FROM subscriptions s
            JOIN clients c ON s.client_id = c.client_id
            JOIN subscription_types st ON s.type_id = st.type_id
            WHERE s.end_date BETWEEN CURRENT_DATE AND CURRENT_DATE + 7
            ORDER BY s.end_date
        """)
        rows = cur.fetchall()
        cur.close()
        conn.close()
        text = "Абонементы, истекающие в ближайшие 7 дней:\n\n"
        for row in rows:
            text += f"{row[0]} {row[1]} - {row[2]} истекает {row[3]}\n"
        self.report_text.setText(text)

    def sales_report(self):
        start = self.start_date.date().toString("yyyy-MM-dd")
        end = self.end_date.date().toString("yyyy-MM-dd")
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT s.sale_date, c.surname, c.name, st.title, st.price
            FROM subscriptions s
            JOIN clients c ON s.client_id = c.client_id
            JOIN subscription_types st ON s.type_id = st.type_id
            WHERE s.sale_date BETWEEN %s AND %s
            ORDER BY s.sale_date
        """, (start, end))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        total = sum(row[4] for row in rows)
        text = f"Продажи за период с {start} по {end}:\n\n"
        for row in rows:
            text += f"{row[0]} - {row[1]} {row[2]} купил {row[3]} за {row[4]} руб.\n"
        text += f"\nОбщая выручка: {total} руб."
        self.report_text.setText(text)

    def visits_report(self):
        start = self.start_date.date().toString("yyyy-MM-dd")
        end = self.end_date.date().toString("yyyy-MM-dd")
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT visit_date, COUNT(*)
            FROM visits
            WHERE visit_date BETWEEN %s AND %s
            GROUP BY visit_date
            ORDER BY visit_date
        """, (start, end))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        text = f"Посещаемость с {start} по {end}:\n\n"
        for row in rows:
            text += f"{row[0]}: {row[1]} посещений\n"
        self.report_text.setText(text)