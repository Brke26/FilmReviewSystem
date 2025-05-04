from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QLineEdit, QTextEdit, QPushButton, QMessageBox
from db_config import connect

class RateWindow(QWidget):
    def __init__(self, user_id, movie_id, movie_title):
        super().__init__()
        self.user_id = user_id
        self.movie_id = movie_id
        self.setWindowTitle(f"Rate: {movie_title}")
        self.setGeometry(400, 250, 500, 500)

        self.label = QLabel(f"Rate '{movie_title}' (1–10):")
        self.input_rating = QLineEdit()
        self.input_rating.setPlaceholderText("Enter rating (e.g., 8)")

        self.input_review = QTextEdit()
        self.input_review.setPlaceholderText("Write your review here")

        self.button_submit = QPushButton("Submit")
        self.button_submit.clicked.connect(self.submit_rating)

        self.label_reviews = QLabel("Previous Reviews:")
        self.reviews_display = QTextEdit()
        self.reviews_display.setReadOnly(True)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.input_rating)
        layout.addWidget(self.input_review)
        layout.addWidget(self.button_submit)
        layout.addWidget(self.label_reviews)
        layout.addWidget(self.reviews_display)

        self.setLayout(layout)

        self.load_reviews()

    def submit_rating(self):
        rating = self.input_rating.text()
        review = self.input_review.toPlainText()

        if not rating.isdigit() or not (1 <= int(rating) <= 10):
            QMessageBox.warning(self, "Invalid", "Rating must be a number between 1 and 10.")
            return

        conn = connect()
        if conn is None:
            QMessageBox.critical(self, "Error", "Database connection failed")
            return

        cur = conn.cursor()
        try:
            # Aynı kullanıcı bu filme daha önce puan vermiş mi?
            cur.execute("""
                SELECT id FROM ratings
                WHERE user_id = %s AND movie_id = %s
            """, (self.user_id, self.movie_id))
            existing = cur.fetchone()

            if existing:
                QMessageBox.warning(self, "Warning", "You have already rated this movie.")
                return  # çıkış yap


            cur.execute("""
                INSERT INTO ratings (user_id, movie_id, rating, review)
                VALUES (%s, %s, %s, %s)
            """, (self.user_id, self.movie_id, int(rating), review))
            conn.commit()
            QMessageBox.information(self, "Success", "Rating submitted!")
            self.input_rating.clear()
            self.input_review.clear()
            self.load_reviews()

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            conn.rollback()
        finally:
            cur.close()
            conn.close()

    def load_reviews(self):
        conn = connect()
        if conn is None:
            return

        cur = conn.cursor()
        try:
            cur.execute("""
                SELECT u.username, r.rating, r.review, r.review_date
                FROM ratings r
                JOIN users u ON r.user_id = u.id
                WHERE r.movie_id = %s
                ORDER BY r.review_date DESC
            """, (self.movie_id,))
            reviews = cur.fetchall()

            display_text = ""
            for r in reviews:
                username, rating, comment, date = r
                display_text += f"{username} | {date.strftime('%Y-%m-%d')} | Rating: {rating}\n{comment}\n\n"

            self.reviews_display.setText(display_text if display_text else "No reviews yet.")

        except Exception as e:
            self.reviews_display.setText("Error loading reviews.")
            print("Error loading reviews:", e)

        finally:
            cur.close()
            conn.close()
