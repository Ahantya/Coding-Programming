from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QTextEdit, QVBoxLayout, QHBoxLayout, QMessageBox, QDialog, QVBoxLayout
import sqlite3

class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login")
        self.username_label = QLabel("Username:")
        self.password_label = QLabel("Password:")
        self.username_entry = QLineEdit()
        self.password_entry = QLineEdit()
        self.login_button = QPushButton("Login", clicked=self.authenticate)

        layout = QVBoxLayout()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_entry)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_entry)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def authenticate(self):
        username = self.username_entry.text()
        password = self.password_entry.text()

        if username == "Joe Sharma" and password == "joesanchit":
            self.accept()
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password.")

class PartnerManagementApp(QWidget):
    def __init__(self):
        super().__init__()

        self.conn = sqlite3.connect('partners.db')
        self.c = self.conn.cursor()

        # Create the 'partners' table if it doesn't exist
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

        self.init_ui()

    def init_ui(self):
        self.login_dialog = LoginDialog()
        result = self.login_dialog.exec_()

        if result == QDialog.Accepted:
            # Widgets
            self.labels = ["Name", "Organization Type", "Resources", "Contact Name", "Contact Email", "Contact Phone"]
            self.entries = [QLineEdit() for _ in range(6)]
            self.search_entry = QLineEdit()
            self.result_text = QTextEdit()

            self.add_button = QPushButton("Add Partner", clicked=self.add_partner)
            self.search_button = QPushButton("Search Partners", clicked=self.search_partners)
            self.exit_button = QPushButton("Exit", clicked=self.close)

            # Layout
            vbox = QVBoxLayout()

            for label, entry in zip(self.labels, self.entries):
                hbox = QHBoxLayout()
                hbox.addWidget(QLabel(f"{label}:"))
                hbox.addWidget(entry)
                vbox.addLayout(hbox)

            vbox.addWidget(QLabel("Search:"))
            vbox.addWidget(self.search_entry)
            vbox.addWidget(self.result_text)

            vbox.addWidget(self.add_button)
            vbox.addWidget(self.search_button)
            vbox.addWidget(self.exit_button)

            self.setLayout(vbox)
            self.setWindowTitle("Partner Management System")
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

            if partners:
                self.result_text.setPlainText('\n'.join(map(str, partners)))
            else:
                QMessageBox.information(self, "No Results", "No matching partners found.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def closeEvent(self, event):
        self.conn.close()
        event.accept()

if __name__ == '__main__':
    app = QApplication([])
    window = PartnerManagementApp()
    window.show()
    app.exec_()
