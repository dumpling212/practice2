from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QMessageBox, QLabel, QComboBox
from models.user_model import UserModel
from database.db_connection import get_connection

class AdminPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Панель администратора")
        self.resize(600, 400)
        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["ID", "Логин", "Роль"])
        self.table.cellClicked.connect(self.select_row)
        layout.addWidget(self.table)

        # Форма для редактирования роли
        form = QHBoxLayout()
        form.addWidget(QLabel("Выберите роль:"))
        self.role_combo = QComboBox()
        self.role_combo.addItems(["user", "manager", "admin"])
        form.addWidget(self.role_combo)
        self.change_role_btn = QPushButton("Изменить роль")
        self.change_role_btn.clicked.connect(self.change_role)
        form.addWidget(self.change_role_btn)
        layout.addLayout(form)

        self.delete_btn = QPushButton("Удалить пользователя")
        self.delete_btn.clicked.connect(self.delete_user)
        layout.addWidget(self.delete_btn)

        self.setLayout(layout)
        self.selected_id = None
        self.load_data()

    def load_data(self):
        rows = UserModel.get_all()
        self.table.setRowCount(0)
        for row_idx, row in enumerate(rows):
            self.table.insertRow(row_idx)
            for col_idx, value in enumerate(row[:3]):  # id, username, role
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

    def select_row(self, row, col):
        self.selected_id = int(self.table.item(row, 0).text())
        current_role = self.table.item(row, 2).text()
        self.role_combo.setCurrentText(current_role)

    def change_role(self):
        if not self.selected_id:
            QMessageBox.warning(self, "Ошибка", "Выберите пользователя")
            return
        new_role = self.role_combo.currentText()
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("UPDATE users SET role=%s WHERE user_id=%s", (new_role, self.selected_id))
        conn.commit()
        cur.close()
        conn.close()
        QMessageBox.information(self, "Успех", "Роль изменена")
        self.load_data()

    def delete_user(self):
        if not self.selected_id:
            QMessageBox.warning(self, "Ошибка", "Выберите пользователя")
            return
        reply = QMessageBox.question(self, "Подтверждение", "Удалить пользователя?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.No:
            return
        UserModel.delete(self.selected_id)
        QMessageBox.information(self, "Успех", "Пользователь удалён")
        self.load_data()