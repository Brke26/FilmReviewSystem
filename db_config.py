import psycopg2

def connect():
    try:
        conn = psycopg2.connect(
            dbname="film_review_db",
            user="postgres",
            password="Berke007",
            host="localhost",
            port="5432"
        )
        print("connection succesful")
        return conn
    except Exception as e:
        print("error", e)
        return None
