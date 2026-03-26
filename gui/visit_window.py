from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QDateEdit, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox
from PyQt5.QtCore import QDate
from models.visit_model import VisitModel
from models.subscription_model import SubscriptionModel
from models.client_model import ClientModel
from models.employee_model import EmployeeModel

class VisitWindow(QWidget):
    def __init__(self, user_id, role):
        super().__init__()
        self.user_id = user_id
        self.role = role
        self.selected_id = None
        self.setWindowTitle("Посещения")
        self.resize(700, 500)

        layout = QVBoxLayout()

        # Таблица
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Клиент", "Абонемент", "Сотрудник", "Дата"])
        self.table.cellClicked.connect(self.select_row)
        layout.addWidget(self.table)

        # Форма ввода
        form_layout = QHBoxLayout()
        form_layout.addWidget(QLabel("Клиент:"))
        self.client_combo = QComboBox()
        form_layout.addWidget(self.client_combo)

        form_layout.addWidget(QLabel("Абонемент:"))
        self.subscription_combo = QComboBox()
        form_layout.addWidget(self.subscription_combo)

        form_layout.addWidget(QLabel("Сотрудник:"))
        self.employee_combo = QComboBox()
        form_layout.addWidget(self.employee_combo)

        form_layout.addWidget(QLabel("Дата:"))
        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        form_layout.addWidget(self.date_edit)

        layout.addLayout(form_layout)

        # Кнопки
        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("Зарегистрировать посещение")
        self.add_btn.clicked.connect(self.add_visit)
        btn_layout.addWidget(self.add_btn)

        if role == "admin":
            self.update_btn = QPushButton("Изменить")
            self.update_btn.clicked.connect(self.update_visit)
            btn_layout.addWidget(self.update_btn)

            self.delete_btn = QPushButton("Удалить")
            self.delete_btn.clicked.connect(self.delete_visit)
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

        # Загружаем сотрудников
        employees = EmployeeModel.get_all()
        self.employee_combo.clear()
        for emp in employees:
            self.employee_combo.addItem(f"{emp[1]} {emp[2]}", emp[0])

        # При выборе клиента будем обновлять абонементы
        self.client_combo.currentIndexChanged.connect(self.update_subscription_combo)

    def update_subscription_combo(self):
        client_id = self.client_combo.currentData()
        self.subscription_combo.clear()
        if not client_id:
            return
        subscriptions = SubscriptionModel.get_active_for_client(client_id)
        for sub in subscriptions:
            sub_id = sub[0]
            type_name = sub[4]  # зависит от порядка полей, лучше сделать отдельный запрос с названием
            # Упростим: сделаем запрос с названием типа
            # Для простоты здесь используем метод, который возвращает читаемые данные
            # Но мы можем загрузить активные абонементы с названием типа
            # Сделаем дополнительный метод в модели
            pass
        # Для простоты переделаем: получим активные абонементы с названием типа
        conn = SubscriptionModel.get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT s.subscription_id, st.title
            FROM subscriptions s
            JOIN subscription_types st ON s.type_id = st.type_id
            WHERE s.client_id = %s AND s.status = 'active'
              AND (s.end_date IS NULL OR s.end_date >= CURRENT_DATE)
              AND (s.visits_remaining IS NULL OR s.visits_remaining > 0)
        """, (client_id,))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        self.subscription_combo.clear()
        for row in rows:
            self.subscription_combo.addItem(row[1], row[0])

    def load_data(self):
        rows = VisitModel.get_with_names()
        self.table.setRowCount(0)
        for row_idx, row in enumerate(rows):
            self.table.insertRow(row_idx)
            for col_idx, value in enumerate(row):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

    def select_row(self, row, col):
        self.selected_id = int(self.table.item(row, 0).text())
        client_text = self.table.item(row, 1).text()
        idx = self.client_combo.findText(client_text)
        if idx >= 0:
            self.client_combo.setCurrentIndex(idx)
        # Для абонемента нужно найти по ID, но в таблице выводим название, а не ID
        # Упростим: не будем заполнять абонемент, т.к. он может быть неактивным
        employee_text = self.table.item(row, 3).text()
        idx = self.employee_combo.findText(employee_text)
        if idx >= 0:
            self.employee_combo.setCurrentIndex(idx)
        self.date_edit.setDate(QDate.fromString(self.table.item(row, 4).text(), "yyyy-MM-dd"))

    def add_visit(self):
        client_id = self.client_combo.currentData()
        subscription_id = self.subscription_combo.currentData()
        employee_id = self.employee_combo.currentData()
        if not client_id or not subscription_id or not employee_id:
            QMessageBox.warning(self, "Ошибка", "Выберите клиента, абонемент и сотрудника")
            return
        visit_date = self.date_edit.date().toString("yyyy-MM-dd")
        # Используем метод модели для регистрации посещения
        if SubscriptionModel.use_visit(subscription_id, employee_id, visit_date):
            QMessageBox.information(self, "Успех", "Посещение зарегистрировано")
            self.load_data()
        else:
            QMessageBox.critical(self, "Ошибка", "Не удалось зарегистрировать посещение")

    def update_visit(self):
        if not self.selected_id:
            QMessageBox.warning(self, "Ошибка", "Выберите посещение")
            return
        client_id = self.client_combo.currentData()
        subscription_id = self.subscription_combo.currentData()
        employee_id = self.employee_combo.currentData()
        visit_date = self.date_edit.date().toString("yyyy-MM-dd")
        if VisitModel.update(self.selected_id, client_id, subscription_id, employee_id, visit_date):
            QMessageBox.information(self, "Успех", "Посещение обновлено")
            self.load_data()
        else:
            QMessageBox.critical(self, "Ошибка", "Не удалось обновить посещение")

    def delete_visit(self):
        if not self.selected_id:
            QMessageBox.warning(self, "Ошибка", "Выберите посещение")
            return
        reply = QMessageBox.question(self, "Подтверждение", "Удалить посещение?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.No:
            return
        if VisitModel.delete(self.selected_id):
            QMessageBox.information(self, "Успех", "Посещение удалено")
            self.load_data()
        else:
            QMessageBox.critical(self, "Ошибка", "Не удалось удалить посещение")