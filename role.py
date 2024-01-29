from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, \
    QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox, QDialog, QHBoxLayout, QComboBox, QTextEdit
from enum import Enum
import sqlite3


class Role(Enum):
    ADMIN = 1
    STUDENT = 2
