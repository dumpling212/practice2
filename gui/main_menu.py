from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox
from gui.client_window import ClientWindow
from gui.subscription_type_window import SubscriptionTypeWindow
from gui.subscription_window import SubscriptionWindow
from gui.visit_window import VisitWindow
from gui.employee_window import EmployeeWindow
from gui.report_window import ReportWindow
from gui.admin_panel import AdminPanel

class MainMenu(QMainWindow):
    def __init__(self, user_id, username, role):
        super().__init__()
        self.user_id = user_id
        self.username = username
        self.role = role
        self.setWindowTitle(f"Главное меню - {username} ({role})")
        self.resize(400, 350)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout()

        layout.addWidget(QLabel(f"Добро пожаловать, {username}!"))
        layout.addWidget(QLabel(f"Ваша роль: {role}"))

        # Кнопки в зависимости от роли
        self.client_btn = QPushButton("Клиенты")
        self.client_btn.clicked.connect(self.open_clients)
        layout.addWidget(self.client_btn)

        if role == "admin":
            self.subscription_type_btn = QPushButton("Типы абонементов")
            self.subscription_type_btn.clicked.connect(self.open_subscription_types)
            layout.addWidget(self.subscription_type_btn)

        self.subscription_btn = QPushButton("Абонементы клиентов")
        self.subscription_btn.clicked.connect(self.open_subscriptions)
        layout.addWidget(self.subscription_btn)

        self.visit_btn = QPushButton("Посещения")
        self.visit_btn.clicked.connect(self.open_visits)
        layout.addWidget(self.visit_btn)

        if role == "admin":
            self.employee_btn = QPushButton("Сотрудники")
            self.employee_btn.clicked.connect(self.open_employees)
            layout.addWidget(self.employee_btn)

        self.report_btn = QPushButton("Отчеты")
        self.report_btn.clicked.connect(self.open_reports)
        layout.addWidget(self.report_btn)

        if role == "admin":
            self.admin_btn = QPushButton("Панель администратора")
            self.admin_btn.clicked.connect(self.open_admin_panel)
            layout.addWidget(self.admin_btn)

        self.logout_btn = QPushButton("Выход")
        self.logout_btn.clicked.connect(self.close)
        layout.addWidget(self.logout_btn)

        central.setLayout(layout)

    def open_clients(self):
        self.client_window = ClientWindow(self.role)
        self.client_window.show()

    def open_subscription_types(self):
        self.subscription_type_window = SubscriptionTypeWindow()
        self.subscription_type_window.show()

    def open_subscriptions(self):
        self.subscription_window = SubscriptionWindow(self.user_id, self.role)
        self.subscription_window.show()

    def open_visits(self):
        self.visit_window = VisitWindow(self.user_id, self.role)
        self.visit_window.show()

    def open_employees(self):
        self.employee_window = EmployeeWindow()
        self.employee_window.show()

    def open_reports(self):
        self.report_window = ReportWindow()
        self.report_window.show()

    def open_admin_panel(self):
        self.admin_panel = AdminPanel()
        self.admin_panel.show()