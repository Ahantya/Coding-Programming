from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, \
    QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox, QDialog, QHBoxLayout, QComboBox, QTextEdit
from enum import Enum
import sqlite3
from role import Role
from login_dialog import LoginDialog

class PartnerEditDialog(QDialog):
    def __init__(self, partner_data):
        super().__init__()

        self.setWindowTitle("Edit Partner")

        self.labels = ["Name", "Organization Type", "Resources", "Contact Name", "Contact Email", "Contact Phone"]
        self.entries = [QLineEdit(partner_data[i]) for i in range(1, len(partner_data))]

        self.edit_button = QPushButton("Edit", clicked=self.accept)
        self.cancel_button = QPushButton("Cancel", clicked=self.reject)

        vbox = QVBoxLayout()

        for label, entry in zip(self.labels, self.entries):
            hbox = QHBoxLayout()
            hbox.addWidget(QLabel(f"{label}:"))
            hbox.addWidget(entry)
            vbox.addLayout(hbox)

        vbox.addWidget(self.edit_button)
        vbox.addWidget(self.cancel_button)

        self.setLayout(vbox)

    def get_edited_values(self):
        return [entry.text() for entry in self.entries]


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
            self.edit_button = QPushButton("Edit Partner", clicked=self.edit_partner)
            self.delete_button = QPushButton("Delete Partner", clicked=self.delete_partner)  # Added Delete button
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
            vbox.addWidget(self.edit_button)
            vbox.addWidget(self.delete_button)  # Added Delete button

            self.delete_all_button = QPushButton("Delete All Data", clicked=self.delete_all_data)
            vbox.addWidget(self.delete_all_button)

            vbox.addWidget(self.logout_button)
            vbox.addWidget(self.exit_button)

            self.setLayout(vbox)
            self.setWindowTitle("Partner Management System")
            self.result_table.setEditTriggers(QTableWidget.NoEditTriggers)  #to disable direct editing
            self.result_table.setSelectionBehavior(QTableWidget.SelectRows)  #and only select entire rows
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
            ''', ('%' + keyword.lower() + '%', '%' + keyword.lower() + '%', '%' + keyword.lower() + '%',
                  '%' + keyword.lower() + '%'))

            partners = self.c.fetchall()

            self.display_table(partners)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def display_table(self, data):
        self.result_table.clear()

        column_headers = ["ID", "Name", "Organization Type", "Resources", "Contact Name", "Contact Email",
                          "Contact Phone"]
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

    def edit_partner(self):
        selected_rows = self.result_table.selectionModel().selectedRows()

        if not selected_rows:
            QMessageBox.warning(self, "Error", "Please select a row to edit.")
            return

        selected_row = selected_rows[0].row()

        partner_id = self.result_table.item(selected_row, 0).text()
        partner_data = self.get_partner_data_by_id(partner_id)

        if partner_data:
            edit_dialog = PartnerEditDialog(partner_data)
            result = edit_dialog.exec_()

            if result == QDialog.Accepted:
                edited_values = edit_dialog.get_edited_values()

                try:
                    self.c.execute('''
                        UPDATE partners
                        SET name=?, organization_type=?, resources_available=?, contact_name=?, contact_email=?, contact_phone=?
                        WHERE id=?
                    ''', (*edited_values, partner_id))

                    self.conn.commit()
                    QMessageBox.information(self, "Success", "Partner edited successfully!")
                    self.search_partners()
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def delete_partner(self):
        selected_rows = self.result_table.selectionModel().selectedRows()

        if not selected_rows:
            QMessageBox.warning(self, "Error", "Please select a row to delete.")
            return

        selected_row = selected_rows[0].row()

        partner_id = self.result_table.item(selected_row, 0).text()

        reply = QMessageBox.question(self, "Delete Partner",
                                     f"Are you sure you want to delete partner with ID {partner_id}?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

        if reply == QMessageBox.Yes:
            try:
                self.c.execute('DELETE FROM partners WHERE id=?', (partner_id,))
                self.conn.commit()
                QMessageBox.information(self, "Success", "Partner deleted successfully!")
                self.search_partners()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def get_partner_data_by_id(self, partner_id):
        try:
            self.c.execute('SELECT * FROM partners WHERE id=?', (partner_id,))
            return self.c.fetchone()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
            return None

    def closeEvent(self, event):
        self.conn.close()
        event.accept()

    def logout(self):
        self.exit_flag = Truefrom PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, \
    QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox, QDialog, QHBoxLayout, QComboBox, QTextEdit
from enum import Enum
import sqlite3
from role import Role
from login_dialog import LoginDialog

class PartnerEditDialog(QDialog):
    def __init__(self, partner_data):
        super().__init__()

        self.setWindowTitle("Edit Partner")

        self.labels = ["Name", "Organization Type", "Resources", "Contact Name", "Contact Email", "Contact Phone"]
        self.entries = [QLineEdit(partner_data[i]) for i in range(1, len(partner_data))]

        self.edit_button = QPushButton("Edit", clicked=self.accept)
        self.cancel_button = QPushButton("Cancel", clicked=self.reject)

        vbox = QVBoxLayout()

        for label, entry in zip(self.labels, self.entries):
            hbox = QHBoxLayout()
            hbox.addWidget(QLabel(f"{label}:"))
            hbox.addWidget(entry)
            vbox.addLayout(hbox)

        vbox.addWidget(self.edit_button)
        vbox.addWidget(self.cancel_button)

        self.setLayout(vbox)

    def get_edited_values(self):
        return [entry.text() for entry in self.entries]


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
            self.edit_button = QPushButton("Edit Partner", clicked=self.edit_partner)
            self.delete_button = QPushButton("Delete Partner", clicked=self.delete_partner)  # Added Delete button
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
            vbox.addWidget(self.edit_button)
            vbox.addWidget(self.delete_button)  # Added Delete button

            self.delete_all_button = QPushButton("Delete All Data", clicked=self.delete_all_data)
            vbox.addWidget(self.delete_all_button)

            vbox.addWidget(self.logout_button)
            vbox.addWidget(self.exit_button)

            self.setLayout(vbox)
            self.setWindowTitle("Partner Management System")
            self.result_table.setEditTriggers(QTableWidget.NoEditTriggers)  #to disable direct editing
            self.result_table.setSelectionBehavior(QTableWidget.SelectRows)  #and only select entire rows
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
            ''', ('%' + keyword.lower() + '%', '%' + keyword.lower() + '%', '%' + keyword.lower() + '%',
                  '%' + keyword.lower() + '%'))

            partners = self.c.fetchall()

            self.display_table(partners)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def display_table(self, data):
        self.result_table.clear()

        column_headers = ["ID", "Name", "Organization Type", "Resources", "Contact Name", "Contact Email",
                          "Contact Phone"]
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

    def edit_partner(self):
        selected_rows = self.result_table.selectionModel().selectedRows()

        if not selected_rows:
            QMessageBox.warning(self, "Error", "Please select a row to edit.")
            return

        selected_row = selected_rows[0].row()

        partner_id = self.result_table.item(selected_row, 0).text()
        partner_data = self.get_partner_data_by_id(partner_id)

        if partner_data:
            edit_dialog = PartnerEditDialog(partner_data)
            result = edit_dialog.exec_()

            if result == QDialog.Accepted:
                edited_values = edit_dialog.get_edited_values()

                try:
                    self.c.execute('''
                        UPDATE partners
                        SET name=?, organization_type=?, resources_available=?, contact_name=?, contact_email=?, contact_phone=?
                        WHERE id=?
                    ''', (*edited_values, partner_id))

                    self.conn.commit()
                    QMessageBox.information(self, "Success", "Partner edited successfully!")
                    self.search_partners()
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def delete_partner(self):
        selected_rows = self.result_table.selectionModel().selectedRows()

        if not selected_rows:
            QMessageBox.warning(self, "Error", "Please select a row to delete.")
            return

        selected_row = selected_rows[0].row()

        partner_id = self.result_table.item(selected_row, 0).text()

        reply = QMessageBox.question(self, "Delete Partner",
                                     f"Are you sure you want to delete partner with ID {partner_id}?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

        if reply == QMessageBox.Yes:
            try:
                self.c.execute('DELETE FROM partners WHERE id=?', (partner_id,))
                self.conn.commit()
                QMessageBox.information(self, "Success", "Partner deleted successfully!")
                self.search_partners()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def get_partner_data_by_id(self, partner_id):
        try:
            self.c.execute('SELECT * FROM partners WHERE id=?', (partner_id,))
            return self.c.fetchone()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
            return None

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
