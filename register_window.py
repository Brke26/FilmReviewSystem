from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton, QMessageBox
from db_config import connect
import psycopg2

class RegisterWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Register New User")
        self.setGeometry(400, 250, 400, 400)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Password")

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")

        self.age_input = QLineEdit()
        self.age_input.setPlaceholderText("Age")

        self.gender_input = QLineEdit()
        self.gender_input.setPlaceholderText("Gender (M/F)")

        self.country_input = QLineEdit()
        self.country_input.setPlaceholderText("Country")

        self.register_button = QPushButton("Register")
        self.register_button.clicked.connect(self.register_user)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Create an account:"))
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.email_input)
        layout.addWidget(self.age_input)
        layout.addWidget(self.gender_input)
        layout.addWidget(self.country_input)
        layout.addWidget(self.register_button)

        self.setLayout(layout)

    def register_user(self):
        username = self.username_input.text()
        password = self.password_input.text()
        email = self.email_input.text()
        age = self.age_input.text()
        gender = self.gender_input.text()
        country = self.country_input.text()

        if not (username and password and email and age and gender and country):
            QMessageBox.warning(self, "Warning", "Please fill in all fields.")
            return

        if not age.isdigit():
            QMessageBox.warning(self, "Warning", "Age must be a number.")
            return

        conn = connect()
        if conn is None:
            QMessageBox.critical(self, "Error", "Database connection failed")
            return

        cur = conn.cursor()
        try:
            cur.execute("""
                INSERT INTO users (username, password, email, age, gender, country)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (username, password, email, int(age), gender.upper(), country))
            conn.commit()
            QMessageBox.information(self, "Success", "User registered successfully!")
            self.close()
        except psycopg2.errors.UniqueViolation:
            conn.rollback()
            QMessageBox.warning(self, "Error", "Username already exists.")
        except Exception as e:
            conn.rollback()
            QMessageBox.critical(self, "Error", str(e))
        finally:
            cur.close()
            conn.close()
