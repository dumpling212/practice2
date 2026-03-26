from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox
from models.employee_model import EmployeeModel

class EmployeeWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.selected_id = None
        self.setWindowTitle("Сотрудники")
        self.resize(600, 400)

        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Фамилия", "Имя", "Отчество", "Телефон"])
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

        layout.addLayout(form_layout)

        # Кнопки
        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("Добавить")
        self.add_btn.clicked.connect(self.add_employee)
        btn_layout.addWidget(self.add_btn)

        self.update_btn = QPushButton("Изменить")
        self.update_btn.clicked.connect(self.update_employee)
        btn_layout.addWidget(self.update_btn)

        self.delete_btn = QPushButton("Удалить")
        self.delete_btn.clicked.connect(self.delete_employee)
        btn_layout.addWidget(self.delete_btn)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

        self.load_data()

    def load_data(self):
        rows = EmployeeModel.get_all(order_by="employee_id")
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

    def add_employee(self):
        surname = self.surname_edit.text().strip()
        name = self.name_edit.text().strip()
        patronymic = self.patronymic_edit.text().strip()
        phone = self.phone_edit.text().strip()
        if not surname or not name:
            QMessageBox.warning(self, "Ошибка", "Фамилия и имя обязательны")
            return
        if EmployeeModel.add(surname, name, patronymic, phone):
            QMessageBox.information(self, "Успех", "Сотрудник добавлен")
            self.clear_form()
            self.load_data()
        else:
            QMessageBox.critical(self, "Ошибка", "Не удалось добавить сотрудника")

    def update_employee(self):
        if not self.selected_id:
            QMessageBox.warning(self, "Ошибка", "Выберите сотрудника")
            return
        surname = self.surname_edit.text().strip()
        name = self.name_edit.text().strip()
        patronymic = self.patronymic_edit.text().strip()
        phone = self.phone_edit.text().strip()
        if EmployeeModel.update(self.selected_id, surname, name, patronymic, phone):
            QMessageBox.information(self, "Успех", "Данные обновлены")
            self.clear_form()
            self.load_data()
        else:
            QMessageBox.critical(self, "Ошибка", "Не удалось обновить данные")

    def delete_employee(self):
        if not self.selected_id:
            QMessageBox.warning(self, "Ошибка", "Выберите сотрудника")
            return
        reply = QMessageBox.question(self, "Подтверждение", "Удалить сотрудника?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.No:
            return
        if EmployeeModel.delete(self.selected_id):
            QMessageBox.information(self, "Успех", "Сотрудник удалён")
            self.clear_form()
            self.load_data()
        else:
            QMessageBox.critical(self, "Ошибка", "Не удалось удалить сотрудника")

    def clear_form(self):
        self.selected_id = None
        self.surname_edit.clear()
        self.name_edit.clear()
        self.patronymic_edit.clear()
        self.phone_edit.clear()