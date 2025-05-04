import sys
import psycopg2
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from db_config import connect
from register_window import RegisterWindow  # kayıt penceresi


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Film Review System - Login")
        self.setGeometry(300, 200, 400, 220)

        # Giriş alanları
        self.label_username = QLabel("Username:")
        self.input_username = QLineEdit()

        self.label_password = QLabel("Password:")
        self.input_password = QLineEdit()
        self.input_password.setEchoMode(QLineEdit.Password)

        # Giriş butonu
        self.button_login = QPushButton("Login")
        self.button_login.clicked.connect(self.login)

        # Kayıt butonu
        self.button_register = QPushButton("Register")
        self.button_register.clicked.connect(self.open_register)

        # Arayüz düzeni
        layout = QVBoxLayout()
        layout.addWidget(self.label_username)
        layout.addWidget(self.input_username)
        layout.addWidget(self.label_password)
        layout.addWidget(self.input_password)
        layout.addWidget(self.button_login)
        layout.addWidget(self.button_register)

        self.setLayout(layout)

    def login(self):
        username = self.input_username.text()
        password = self.input_password.text()

        conn = connect()
        if conn is None:
            QMessageBox.critical(self, "Error", "Database connection failed")
            return

        cur = conn.cursor()
        try:
            cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
            user = cur.fetchone()
            if user:
                QMessageBox.information(self, "Success", f"Welcome, {user[1]}!")
                self.close()

                from film_list import FilmListWindow
                self.film_window = FilmListWindow(user_id=user[0])
                self.film_window.show()
            else:
                QMessageBox.warning(self, "Failed", "Invalid username or password")

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
        finally:
            cur.close()
            conn.close()

    def open_register(self):
        self.register_window = RegisterWindow()
        self.register_window.show()


# Pyqt 5 uygulama başlatma
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())
