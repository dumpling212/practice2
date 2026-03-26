from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from models.user_model import UserModel

class ChangePasswordWindow(QWidget):
    def __init__(self, user_id=None):
        super().__init__()
        self.user_id = user_id
        self.setWindowTitle("Смена пароля")
        self.resize(300, 150)
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Логин:"))
        self.username_input = QLineEdit()
        layout.addWidget(self.username_input)

        layout.addWidget(QLabel("Старый пароль:"))
        self.old_password_input = QLineEdit()
        self.old_password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.old_password_input)

        layout.addWidget(QLabel("Новый пароль:"))
        self.new_password_input = QLineEdit()
        self.new_password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.new_password_input)

        self.change_btn = QPushButton("Сменить")
        self.change_btn.clicked.connect(self.change)
        layout.addWidget(self.change_btn)

        self.setLayout(layout)

    def change(self):
        username = self.username_input.text().strip()
        old_pass = self.old_password_input.text().strip()
        new_pass = self.new_password_input.text().strip()
        if not username or not old_pass or not new_pass:
            QMessageBox.warning(self, "Ошибка", "Заполните все поля")
            return
        # Получаем user_id по username
        conn = UserModel.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT user_id FROM users WHERE username=%s", (username,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        if not row:
            QMessageBox.warning(self, "Ошибка", "Пользователь не найден")
            return
        user_id = row[0]
        if UserModel.change_password(user_id, old_pass, new_pass):
            QMessageBox.information(self, "Успех", "Пароль успешно изменён")
            self.close()
        else:
            QMessageBox.warning(self, "Ошибка", "Неверный старый пароль")