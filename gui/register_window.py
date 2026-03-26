from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from models.user_model import UserModel

class RegisterWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Регистрация")
        self.resize(300, 150)
        self.setFixedSize(300, 150)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Логин:"))
        self.username_input = QLineEdit()
        layout.addWidget(self.username_input)

        layout.addWidget(QLabel("Пароль:"))
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        self.register_btn = QPushButton("Зарегистрироваться")
        self.register_btn.clicked.connect(self.register)
        layout.addWidget(self.register_btn)

        self.setLayout(layout)

    def register(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        if not username or not password:
            QMessageBox.warning(self, "Ошибка", "Заполните все поля")
            return
        if len(password) < 6:
            QMessageBox.warning(self, "Ошибка", "Пароль должен быть не менее 6 символов")
            return
        if UserModel.register(username, password):
            QMessageBox.information(self, "Успех", "Регистрация успешна")
            self.close()
        else:
            QMessageBox.warning(self, "Ошибка", "Пользователь с таким логином уже существует")