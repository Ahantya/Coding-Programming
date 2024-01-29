from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, \
    QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox, QDialog, QHBoxLayout, QComboBox, QTextEdit
from enum import Enum
import sqlite3
from role import Role

class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login")

        self.username_label = QLabel("Username:")
        self.password_label = QLabel("Password:")
        self.role_label = QLabel("Role:")

        self.username_entry = QLineEdit()
        self.password_entry = QLineEdit()
        self.password_entry.setEchoMode(QLineEdit.Password)
        self.role_combobox = QComboBox()
        self.role_combobox.addItem("Admin")
        self.role_combobox.addItem("Student")

        self.login_button = QPushButton("Login", clicked=self.authenticate)

        layout = QVBoxLayout()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_entry)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_entry)
        layout.addWidget(self.role_label)
        layout.addWidget(self.role_combobox)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

        self.selected_role = None

    def update_echo_mode(self, text, entry):
        if text:
            entry.setEchoMode(QLineEdit.Password)
        else:
            entry.setEchoMode(QLineEdit.Normal)

    def authenticate(self):
        username = self.username_entry.text()
        password = self.password_entry.text()
        selected_role = self.role_combobox.currentText()

        if selected_role == "Admin" and username == "admin" and password == "adminpass":
            self.selected_role = Role.ADMIN
            self.accept()
        elif selected_role == "Student" and username == "student" and password == "studentpass":
            self.selected_role = Role.STUDENT
            self.accept()
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username, password, or role.")

    def get_role(self):
        return self.selected_role
