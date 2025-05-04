from PyQt5.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QLabel
from db_config import connect
from rate_window import RateWindow


class FilmListWindow(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.setWindowTitle("Film List")
        self.setGeometry(350, 200, 700, 400)

        self.label = QLabel("All Movies")
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Title", "Genre", "IMDB Rating"])

        self.table.cellDoubleClicked.connect(self.open_rate_window)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.table)
        self.setLayout(layout)

        self.load_movies()

    def load_movies(self):
        conn = connect()
        if conn is None:
            return

        cur = conn.cursor()
        try:
            cur.execute("SELECT title, genre, imdb_rating FROM movies")
            results = cur.fetchall()
            self.table.setRowCount(len(results))
            for row_idx, row_data in enumerate(results):
                for col_idx, value in enumerate(row_data):
                    self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))
        except Exception as e:
            print("Error loading movies:", e)
        finally:
            cur.close()
            conn.close()

    def open_rate_window(self, row, column):
        title_item = self.table.item(row, 0)
        if title_item:
            movie_title = title_item.text()

            conn = connect()
            cur = conn.cursor()
            try:
                cur.execute("SELECT id FROM movies WHERE title = %s", (movie_title,))
                result = cur.fetchone()
                if result:
                    movie_id = result[0]

                    self.rate_win = RateWindow(
                        user_id=self.user_id,  # ← Giriş yapan kullanıcıdan alınan ID
                        movie_id=movie_id,
                        movie_title=movie_title
                    )
                    self.rate_win.show()
            except Exception as e:
                print("Error fetching movie ID:", e)
            finally:
                cur.close()
                conn.close()

