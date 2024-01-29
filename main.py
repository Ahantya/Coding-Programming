from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, \
    QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox, QDialog, QHBoxLayout, QComboBox, QTextEdit
from enum import Enum
import sqlite3

from login_dialog import LoginDialog
from role import Role
from partner_management_app import PartnerManagementApp

if __name__ == '__main__':
    app = QApplication([])

    exit_flag = False

    while not exit_flag:
        login_dialog = LoginDialog()
        result = login_dialog.exec_()

        if result == QDialog.Accepted:
            window = PartnerManagementApp(login_dialog.get_role())
            window.show()
            app.exec_()

            exit_flag = getattr(window, 'exit_flag', False)
        else:
            break
""" from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, \
    QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox, QDialog, QHBoxLayout, QComboBox, QTextEdit
from enum import Enum
import sqlite3

class Role(Enum):
    ADMIN = 1
    STUDENT = 2

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

class PartnerManagementApp(QWidget):
    def __init__(self, role):
        super().__init__()

        self.conn = sqlite3.connect('partners.db')
        self.c = self.conn.cursor()

        self.c.execute('''
            CREATE TABLE IF NOT EXISTS partners (
                id INTEGER PRIMARY KEY,
                name TEXT,
                organization_type TEXT,
                resources_available TEXT,
                contact_name TEXT,
                contact_email TEXT,
                contact_phone TEXT
            )
        ''')
        self.conn.commit()

        self.init_ui(role)

    def init_ui(self, role):
        if role == Role.ADMIN:
            self.labels = ["Name", "Organization Type", "Resources", "Contact Name", "Contact Email", "Contact Phone"]
            self.entries = [QLineEdit() for _ in range(6)]
            self.search_entry = QLineEdit()
            self.result_table = QTableWidget()

            self.add_button = QPushButton("Add Partner", clicked=self.add_partner)
            self.search_button = QPushButton("Search Partners", clicked=self.search_partners)
            self.logout_button = QPushButton("Logout", clicked=self.close)
            self.exit_button = QPushButton("Exit", clicked=self.logout)

            vbox = QVBoxLayout()

            for label, entry in zip(self.labels, self.entries):
                hbox = QHBoxLayout()
                hbox.addWidget(QLabel(f"{label}:"))
                hbox.addWidget(entry)
                vbox.addLayout(hbox)

            vbox.addWidget(QLabel("Search:"))
            vbox.addWidget(self.search_entry)
            vbox.addWidget(self.result_table)
            vbox.addWidget(self.add_button)
            vbox.addWidget(self.search_button)

            self.delete_all_button = QPushButton("Delete All Data", clicked=self.delete_all_data)
            vbox.addWidget(self.delete_all_button)

            vbox.addWidget(self.logout_button)
            vbox.addWidget(self.exit_button)

            self.setLayout(vbox)
            self.setWindowTitle("Partner Management System")

            self.search_partners()
        elif role == Role.STUDENT:
            self.result_table = QTableWidget()
            self.search_entry = QLineEdit()
            self.search_button = QPushButton("Search Partners", clicked=self.search_partners)
            self.logout_button = QPushButton("Logout", clicked=self.close)
            self.exit_button = QPushButton("Exit", clicked=self.logout)

            vbox = QVBoxLayout()

            vbox.addWidget(QLabel("Search:"))
            vbox.addWidget(self.search_entry)
            vbox.addWidget(self.result_table)

            vbox.addWidget(self.search_button)
            vbox.addWidget(self.logout_button)
            vbox.addWidget(self.exit_button)

            self.setLayout(vbox)
            self.setWindowTitle("Student View - Partner Management System")

            self.search_partners()
        else:
            self.close()

    def add_partner(self):
        values = [entry.text() for entry in self.entries]

        self.c.execute('''
            INSERT INTO partners (name, organization_type, resources_available, contact_name, contact_email, contact_phone)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', tuple(values))

        self.conn.commit()
        QMessageBox.information(self, "Success", "Partner added successfully!")

    def search_partners(self):
        keyword = self.search_entry.text()

        try:
            self.c.execute('''
                SELECT * FROM partners
                WHERE LOWER(name) LIKE ? OR LOWER(organization_type) LIKE ? OR LOWER(resources_available) LIKE ? OR LOWER(contact_name) LIKE ?
            ''', ('%' + keyword.lower() + '%', '%' + keyword.lower() + '%', '%' + keyword.lower() + '%', '%' + keyword.lower() + '%'))

            partners = self.c.fetchall()

            self.display_table(partners)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def display_table(self, data):
        self.result_table.clear()

        column_headers = ["ID", "Name", "Organization Type", "Resources", "Contact Name", "Contact Email", "Contact Phone"]
        self.result_table.setColumnCount(len(column_headers))
        self.result_table.setHorizontalHeaderLabels(column_headers)

        self.result_table.setRowCount(len(data))
        for row_index, row_data in enumerate(data):
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.result_table.setItem(row_index, col_index, item)

        self.result_table.resizeColumnsToContents()
        self.result_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def delete_all_data(self):
        reply = QMessageBox.question(self, "Delete All Data", "Are you sure you want to delete all data?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

        if reply == QMessageBox.Yes:
            try:
                self.c.execute('DELETE FROM partners')
                self.conn.commit()
                QMessageBox.information(self, "Success", "All data deleted successfully!")
                self.search_partners()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def closeEvent(self, event):
        self.conn.close()
        event.accept()

    def logout(self):
        self.exit_flag = True
        self.close()


if __name__ == '__main__':
    app = QApplication([])

    exit_flag = False

    while not exit_flag:
        login_dialog = LoginDialog()
        result = login_dialog.exec_()

        if result == QDialog.Accepted:
            window = PartnerManagementApp(login_dialog.get_role())
            window.show()
            app.exec_()

            exit_flag = getattr(window, 'exit_flag', False)
        else:
            break
            """
