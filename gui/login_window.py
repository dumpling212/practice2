import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import Qt
from models.user_model import UserModel
from gui.main_menu import MainMenu
from gui.register_window import RegisterWindow
from gui.change_password_window import ChangePasswordWindow

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Авторизация - Фитнес-клуб")
        self.resize(300, 200)
        self.setFixedSize(300, 200)

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Логин:"))
        self.username_input = QLineEdit()
        layout.addWidget(self.username_input)

        layout.addWidget(QLabel("Пароль:"))
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        self.login_btn = QPushButton("Войти")
        self.login_btn.clicked.connect(self.login)
        layout.addWidget(self.login_btn)

        self.register_btn = QPushButton("Регистрация")
        self.register_btn.clicked.connect(self.open_register)
        layout.addWidget(self.register_btn)

        self.change_pass_btn = QPushButton("Сменить пароль")
        self.change_pass_btn.clicked.connect(self.open_change_password)
        layout.addWidget(self.change_pass_btn)

        self.setLayout(layout)

    def login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        if not username or not password:
            QMessageBox.warning(self, "Ошибка", "Введите логин и пароль")
            return
        user = UserModel.authenticate(username, password)
        if user:
            user_id, username, role = user
            self.main_menu = MainMenu(user_id, username, role)
            self.main_menu.show()
            self.close()
        else:
            QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль")

    def open_register(self):
        self.register_window = RegisterWindow()
        self.register_window.show()

    def open_change_password(self):
        self.change_pass_window = ChangePasswordWindow()
        self.change_pass_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())