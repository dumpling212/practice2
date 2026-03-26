from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QDateEdit, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QSpinBox
from PyQt5.QtCore import QDate
from models.subscription_model import SubscriptionModel
from models.client_model import ClientModel
from models.subscription_type_model import SubscriptionTypeModel
from models.employee_model import EmployeeModel
from datetime import datetime, timedelta

class SubscriptionWindow(QWidget):
    def __init__(self, user_id, role):
        super().__init__()
        self.user_id = user_id
        self.role = role
        self.selected_id = None
        self.setWindowTitle("Абонементы клиентов")
        self.resize(800, 500)

        layout = QVBoxLayout()

        # Таблица
        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels(["ID", "Клиент", "Тип", "Сотрудник", "Дата продажи", "Начало", "Окончание", "Осталось посещ.", "Статус"])
        self.table.cellClicked.connect(self.select_row)
        layout.addWidget(self.table)

        # Форма ввода
        form_layout = QHBoxLayout()
        form_layout.addWidget(QLabel("Клиент:"))
        self.client_combo = QComboBox()
        self.client_combo.setMinimumWidth(150)
        form_layout.addWidget(self.client_combo)

        form_layout.addWidget(QLabel("Тип:"))
        self.type_combo = QComboBox()
        form_layout.addWidget(self.type_combo)

        form_layout.addWidget(QLabel("Сотрудник:"))
        self.employee_combo = QComboBox()
        form_layout.addWidget(self.employee_combo)

        form_layout.addWidget(QLabel("Дата продажи:"))
        self.sale_date = QDateEdit()
        self.sale_date.setDate(QDate.currentDate())
        self.sale_date.setCalendarPopup(True)
        form_layout.addWidget(self.sale_date)

        form_layout.addWidget(QLabel("Начало:"))
        self.start_date = QDateEdit()
        self.start_date.setDate(QDate.currentDate())
        self.start_date.setCalendarPopup(True)
        form_layout.addWidget(self.start_date)

        form_layout.addWidget(QLabel("Окончание:"))
        self.end_date = QDateEdit()
        self.end_date.setDate(QDate.currentDate().addDays(30))
        self.end_date.setCalendarPopup(True)
        form_layout.addWidget(self.end_date)

        form_layout.addWidget(QLabel("Осталось:"))
        self.visits_rem = QSpinBox()
        self.visits_rem.setMinimum(0)
        form_layout.addWidget(self.visits_rem)

        form_layout.addWidget(QLabel("Статус:"))
        self.status_combo = QComboBox()
        self.status_combo.addItems(["active", "expired", "cancelled"])
        form_layout.addWidget(self.status_combo)

        layout.addLayout(form_layout)

        # Кнопки
        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("Добавить")
        self.add_btn.clicked.connect(self.add_subscription)
        btn_layout.addWidget(self.add_btn)

        self.update_btn = QPushButton("Изменить")
        self.update_btn.clicked.connect(self.update_subscription)
        btn_layout.addWidget(self.update_btn)

        self.delete_btn = QPushButton("Удалить")
        self.delete_btn.clicked.connect(self.delete_subscription)
        btn_layout.addWidget(self.delete_btn)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

        self.load_combo_data()
        self.load_data()

    def load_combo_data(self):
        # Загружаем клиентов
        clients = ClientModel.get_all()
        self.client_combo.clear()
        self.client_combo.addItem("", None)
        for cl in clients:
            self.client_combo.addItem(f"{cl[1]} {cl[2]}", cl[0])

        # Загружаем типы
        types = SubscriptionTypeModel.get_all()
        self.type_combo.clear()
        for tp in types:
            self.type_combo.addItem(tp[1], tp[0])

        # Загружаем сотрудников
        employees = EmployeeModel.get_all()
        self.employee_combo.clear()
        for emp in employees:
            self.employee_combo.addItem(f"{emp[1]} {emp[2]}", emp[0])

    def load_data(self):
        rows = SubscriptionModel.get_with_names()
        self.table.setRowCount(0)
        for row_idx, row in enumerate(rows):
            self.table.insertRow(row_idx)
            for col_idx, value in enumerate(row):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

    def select_row(self, row, col):
        self.selected_id = int(self.table.item(row, 0).text())
        # Поиск индексов в комбобоксах
        client_text = self.table.item(row, 1).text()
        idx = self.client_combo.findText(client_text)
        if idx >= 0:
            self.client_combo.setCurrentIndex(idx)

        type_text = self.table.item(row, 2).text()
        idx = self.type_combo.findText(type_text)
        if idx >= 0:
            self.type_combo.setCurrentIndex(idx)

        employee_text = self.table.item(row, 3).text()
        idx = self.employee_combo.findText(employee_text)
        if idx >= 0:
            self.employee_combo.setCurrentIndex(idx)

        self.sale_date.setDate(QDate.fromString(self.table.item(row, 4).text(), "yyyy-MM-dd"))
        self.start_date.setDate(QDate.fromString(self.table.item(row, 5).text(), "yyyy-MM-dd"))
        end = self.table.item(row, 6).text()
        if end != 'None':
            self.end_date.setDate(QDate.fromString(end, "yyyy-MM-dd"))
        else:
            self.end_date.clear()
        rem = self.table.item(row, 7).text()
        if rem != 'None':
            self.visits_rem.setValue(int(rem))
        else:
            self.visits_rem.setValue(0)
        status = self.table.item(row, 8).text()
        idx = self.status_combo.findText(status)
        if idx >= 0:
            self.status_combo.setCurrentIndex(idx)

    def add_subscription(self):
        client_id = self.client_combo.currentData()
        type_id = self.type_combo.currentData()
        employee_id = self.employee_combo.currentData()
        if not client_id or not type_id or not employee_id:
            QMessageBox.warning(self, "Ошибка", "Заполните все поля")
            return
        sale_date = self.sale_date.date().toString("yyyy-MM-dd")
        start_date = self.start_date.date().toString("yyyy-MM-dd")
        end_date = self.end_date.date().toString("yyyy-MM-dd") if self.end_date.date() else None
        visits_remaining = self.visits_rem.value() if self.visits_rem.value() > 0 else None
        if SubscriptionModel.add(client_id, type_id, employee_id, sale_date, start_date, end_date, visits_remaining):
            QMessageBox.information(self, "Успех", "Абонемент добавлен")
            self.load_data()
        else:
            QMessageBox.critical(self, "Ошибка", "Не удалось добавить абонемент")

    def update_subscription(self):
        if not self.selected_id:
            QMessageBox.warning(self, "Ошибка", "Выберите абонемент")
            return
        client_id = self.client_combo.currentData()
        type_id = self.type_combo.currentData()
        employee_id = self.employee_combo.currentData()
        if not client_id or not type_id or not employee_id:
            QMessageBox.warning(self, "Ошибка", "Заполните все поля")
            return
        sale_date = self.sale_date.date().toString("yyyy-MM-dd")
        start_date = self.start_date.date().toString("yyyy-MM-dd")
        end_date = self.end_date.date().toString("yyyy-MM-dd") if self.end_date.date() else None
        visits_remaining = self.visits_rem.value() if self.visits_rem.value() > 0 else None
        status = self.status_combo.currentText()
        if SubscriptionModel.update(self.selected_id, client_id, type_id, employee_id, sale_date, start_date, end_date, visits_remaining, status):
            QMessageBox.information(self, "Успех", "Абонемент обновлён")
            self.load_data()
        else:
            QMessageBox.critical(self, "Ошибка", "Не удалось обновить абонемент")

    def delete_subscription(self):
        if not self.selected_id:
            QMessageBox.warning(self, "Ошибка", "Выберите абонемент")
            return
        reply = QMessageBox.question(self, "Подтверждение", "Удалить абонемент?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.No:
            return
        if SubscriptionModel.delete(self.selected_id):
            QMessageBox.information(self, "Успех", "Абонемент удалён")
            self.load_data()
        else:
            QMessageBox.critical(self, "Ошибка", "Не удалось удалить абонемент")