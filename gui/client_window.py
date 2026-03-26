from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QDateEdit
from PyQt5.QtCore import QDate
from models.client_model import ClientModel

class ClientWindow(QWidget):
    def __init__(self, role):
        super().__init__()
        self.role = role
        self.selected_id = None
        self.setWindowTitle("Клиенты")
        self.resize(700, 500)

        layout = QVBoxLayout()

        # Таблица
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Фамилия", "Имя", "Отчество", "Телефон", "Дата рождения"])
        self.table.cellClicked.connect(self.select_row)
        layout.addWidget(self.table)

        # Форма ввода
        form_layout = QHBoxLayout()
        form_layout.addWidget(QLabel("Фамилия:"))
        self.surname_edit = QLineEdit()
        form_layout.addWidget(self.surname_edit)

        form_layout.addWidget(QLabel("Имя:"))
        self.name_edit = QLineEdit()
        form_layout.addWidget(self.name_edit)

        form_layout.addWidget(QLabel("Отчество:"))
        self.patronymic_edit = QLineEdit()
        form_layout.addWidget(self.patronymic_edit)

        form_layout.addWidget(QLabel("Телефон:"))
        self.phone_edit = QLineEdit()
        form_layout.addWidget(self.phone_edit)

        form_layout.addWidget(QLabel("Дата рождения:"))
        self.birth_edit = QDateEdit()
        self.birth_edit.setDate(QDate.currentDate())
        self.birth_edit.setCalendarPopup(True)
        form_layout.addWidget(self.birth_edit)

        layout.addLayout(form_layout)

        # Кнопки
        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("Добавить")
        self.add_btn.clicked.connect(self.add_client)
        btn_layout.addWidget(self.add_btn)

        self.update_btn = QPushButton("Изменить")
        self.update_btn.clicked.connect(self.update_client)
        btn_layout.addWidget(self.update_btn)

        self.delete_btn = QPushButton("Удалить")
        self.delete_btn.clicked.connect(self.delete_client)
        btn_layout.addWidget(self.delete_btn)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

        self.load_data()

    def load_data(self):
        rows = ClientModel.get_all(order_by="client_id")
        self.table.setRowCount(0)
        for row_idx, row in enumerate(rows):
            self.table.insertRow(row_idx)
            for col_idx, value in enumerate(row):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

    def select_row(self, row, col):
        self.selected_id = int(self.table.item(row, 0).text())
        self.surname_edit.setText(self.table.item(row, 1).text())
        self.name_edit.setText(self.table.item(row, 2).text())
        self.patronymic_edit.setText(self.table.item(row, 3).text())
        self.phone_edit.setText(self.table.item(row, 4).text())
        self.birth_edit.setDate(QDate.fromString(self.table.item(row, 5).text(), "yyyy-MM-dd"))

    def add_client(self):
        surname = self.surname_edit.text().strip()
        name = self.name_edit.text().strip()
        patronymic = self.patronymic_edit.text().strip()
        phone = self.phone_edit.text().strip()
        birth_date = self.birth_edit.date().toString("yyyy-MM-dd")
        if not surname or not name:
            QMessageBox.warning(self, "Ошибка", "Фамилия и имя обязательны")
            return
        if ClientModel.add(surname, name, patronymic, phone, birth_date):
            QMessageBox.information(self, "Успех", "Клиент добавлен")
            self.clear_form()
            self.load_data()
        else:
            QMessageBox.critical(self, "Ошибка", "Не удалось добавить клиента")

    def update_client(self):
        if not self.selected_id:
            QMessageBox.warning(self, "Ошибка", "Выберите клиента")
            return
        surname = self.surname_edit.text().strip()
        name = self.name_edit.text().strip()
        patronymic = self.patronymic_edit.text().strip()
        phone = self.phone_edit.text().strip()
        birth_date = self.birth_edit.date().toString("yyyy-MM-dd")
        if ClientModel.update(self.selected_id, surname, name, patronymic, phone, birth_date):
            QMessageBox.information(self, "Успех", "Данные обновлены")
            self.clear_form()
            self.load_data()
        else:
            QMessageBox.critical(self, "Ошибка", "Не удалось обновить данные")

    def delete_client(self):
        if not self.selected_id:
            QMessageBox.warning(self, "Ошибка", "Выберите клиента")
            return
        reply = QMessageBox.question(self, "Подтверждение", "Удалить клиента?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.No:
            return
        if ClientModel.delete(self.selected_id):
            QMessageBox.information(self, "Успех", "Клиент удалён")
            self.clear_form()
            self.load_data()
        else:
            QMessageBox.critical(self, "Ошибка", "Не удалось удалить клиента")

    def clear_form(self):
        self.selected_id = None
        self.surname_edit.clear()
        self.name_edit.clear()
        self.patronymic_edit.clear()
        self.phone_edit.clear()
        self.birth_edit.setDate(QDate.currentDate())