from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QSpinBox, QDoubleSpinBox, QTextEdit
from models.subscription_type_model import SubscriptionTypeModel

class SubscriptionTypeWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.selected_id = None
        self.setWindowTitle("Типы абонементов")
        self.resize(700, 500)

        layout = QVBoxLayout()

        # Таблица
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Название", "Описание", "Цена", "Дней", "Посещений"])
        self.table.cellClicked.connect(self.select_row)
        layout.addWidget(self.table)

        # Форма ввода
        form_layout = QHBoxLayout()
        form_layout.addWidget(QLabel("Название:"))
        self.title_edit = QLineEdit()
        form_layout.addWidget(self.title_edit)

        form_layout.addWidget(QLabel("Описание:"))
        self.desc_edit = QTextEdit()
        self.desc_edit.setMaximumHeight(60)
        form_layout.addWidget(self.desc_edit)

        form_layout.addWidget(QLabel("Цена:"))
        self.price_edit = QDoubleSpinBox()
        self.price_edit.setMaximum(100000)
        self.price_edit.setPrefix("₽ ")
        form_layout.addWidget(self.price_edit)

        form_layout.addWidget(QLabel("Дней:"))
        self.days_edit = QSpinBox()
        self.days_edit.setSpecialValueText("Безлимит по дням")
        self.days_edit.setMinimum(0)
        self.days_edit.setMaximum(1000)
        form_layout.addWidget(self.days_edit)

        form_layout.addWidget(QLabel("Посещений:"))
        self.visits_edit = QSpinBox()
        self.visits_edit.setSpecialValueText("Безлимит по посещениям")
        self.visits_edit.setMinimum(0)
        self.visits_edit.setMaximum(1000)
        form_layout.addWidget(self.visits_edit)

        layout.addLayout(form_layout)

        # Кнопки
        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("Добавить")
        self.add_btn.clicked.connect(self.add_type)
        btn_layout.addWidget(self.add_btn)

        self.update_btn = QPushButton("Изменить")
        self.update_btn.clicked.connect(self.update_type)
        btn_layout.addWidget(self.update_btn)

        self.delete_btn = QPushButton("Удалить")
        self.delete_btn.clicked.connect(self.delete_type)
        btn_layout.addWidget(self.delete_btn)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

        self.load_data()

    def load_data(self):
        rows = SubscriptionTypeModel.get_all(order_by="type_id")
        self.table.setRowCount(0)
        for row_idx, row in enumerate(rows):
            self.table.insertRow(row_idx)
            for col_idx, value in enumerate(row):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

    def select_row(self, row, col):
        self.selected_id = int(self.table.item(row, 0).text())
        self.title_edit.setText(self.table.item(row, 1).text())
        self.desc_edit.setPlainText(self.table.item(row, 2).text())
        self.price_edit.setValue(float(self.table.item(row, 3).text()))
        days = self.table.item(row, 4).text()
        self.days_edit.setValue(int(days) if days != 'None' else 0)
        visits = self.table.item(row, 5).text()
        self.visits_edit.setValue(int(visits) if visits != 'None' else 0)

    def add_type(self):
        title = self.title_edit.text().strip()
        description = self.desc_edit.toPlainText().strip()
        price = self.price_edit.value()
        duration_days = self.days_edit.value() if self.days_edit.value() > 0 else None
        max_visits = self.visits_edit.value() if self.visits_edit.value() > 0 else None
        if not title or price <= 0:
            QMessageBox.warning(self, "Ошибка", "Название и цена обязательны")
            return
        if SubscriptionTypeModel.add(title, description, price, duration_days, max_visits):
            QMessageBox.information(self, "Успех", "Тип абонемента добавлен")
            self.clear_form()
            self.load_data()
        else:
            QMessageBox.critical(self, "Ошибка", "Не удалось добавить тип")

    def update_type(self):
        if not self.selected_id:
            QMessageBox.warning(self, "Ошибка", "Выберите тип")
            return
        title = self.title_edit.text().strip()
        description = self.desc_edit.toPlainText().strip()
        price = self.price_edit.value()
        duration_days = self.days_edit.value() if self.days_edit.value() > 0 else None
        max_visits = self.visits_edit.value() if self.visits_edit.value() > 0 else None
        if SubscriptionTypeModel.update(self.selected_id, title, description, price, duration_days, max_visits):
            QMessageBox.information(self, "Успех", "Тип обновлён")
            self.clear_form()
            self.load_data()
        else:
            QMessageBox.critical(self, "Ошибка", "Не удалось обновить тип")

    def delete_type(self):
        if not self.selected_id:
            QMessageBox.warning(self, "Ошибка", "Выберите тип")
            return
        reply = QMessageBox.question(self, "Подтверждение", "Удалить тип абонемента?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.No:
            return
        if SubscriptionTypeModel.delete(self.selected_id):
            QMessageBox.information(self, "Успех", "Тип удалён")
            self.clear_form()
            self.load_data()
        else:
            QMessageBox.critical(self, "Ошибка", "Не удалось удалить тип")

    def clear_form(self):
        self.selected_id = None
        self.title_edit.clear()
        self.desc_edit.clear()
        self.price_edit.setValue(0)
        self.days_edit.setValue(0)
        self.visits_edit.setValue(0)