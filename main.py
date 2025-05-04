import psycopg2
from db_config import connect


def register_user():
    conn = connect()
    if conn is None:
        return

    cur = conn.cursor()

    print("=== Register User ===")
    username = input("Username: ")
    password = input("Password: ")
    email = input("Email: ")
    age = int(input("Age: "))
    gender = input("Gender (M/F): ")
    country = input("Country: ")

    try:
        cur.execute("""
            INSERT INTO users (username, password, email, age, gender, country)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (username, password, email, age, gender, country))
        conn.commit()
        print("User registered successfully.")

    except psycopg2.errors.UniqueViolation:
        print("Username already exist. Try another one.")
        conn.rollback()

    except Exception as e:
        print("Error registering user:", e)
        conn.rollback()

    finally:
        cur.close()
        conn.close()


def login_user():
    conn = connect()
    if conn is None:
        return

    cur = conn.cursor()

    print("=== Login User ===")
    username = input("Username: ")
    password = input("Password: ")

    try:
        cur.execute("""
            SELECT * FROM users WHERE username = %s AND password = %s
        """, (username, password))
        user = cur.fetchone()

        if user:
            print(f"Login successful. Welcome, {user[1]}!")
            cur.close()
            conn.close()
            main_menu(user[0])

        else:
            print("Invalid username or password.")

    except Exception as e:
        print("Error logging in:", e)

    finally:
        if not cur.closed:
            cur.close()
        if conn and not conn.closed:
            conn.close()






def list_movies():
    conn = connect()
    if conn is None:
        return

    cur = conn.cursor()

    print("=== Movie List ===")

    try:
        cur.execute("SELECT id, title, genre, imdb_rating FROM movies")
        movies = cur.fetchall()

        if not movies:
            print("No movies found.")
            return

        for movie in movies:
            print(f"[{movie[0]}] {movie[1]} | Genre: {movie[2]} | IMDB Rating: {movie[3]}")

    except Exception as e:
        print("Error retrieving movies:", e)

    finally:
        cur.close()
        conn.close()





def rate_movie(user_id):
    conn = connect()
    if conn is None:
        return

    cur = conn.cursor()

    try:
        print("=== Rate a Movie ===")
        movie_id = int(input("Enter the ID of the movie you want to rate: "))
        rating = int(input("Rating (1–10): "))
        review = input("Your review: ")

        cur.execute("""
            INSERT INTO ratings (user_id, movie_id, rating, review)
            VALUES (%s, %s, %s, %s)
        """, (user_id, movie_id, rating, review))
        conn.commit()
        print("Your rating and review have been submitted successfully.")

    except psycopg2.errors.UniqueViolation:
        print("You have already rated this movie.")
        conn.rollback()

    except Exception as e:
        print("Error while rating the movie:", e)
        conn.rollback()

    finally:
        cur.close()
        conn.close()




def show_reviews():
    conn = connect()
    if conn is None:
        return

    cur = conn.cursor()

    try:
        print("=== Show Reviews for a Movie ===")
        movie_id = int(input("Enter the ID of the movie: "))

        cur.execute("""
            SELECT u.username, r.rating, r.review, r.review_date
            FROM ratings r
            JOIN users u ON r.user_id = u.id
            WHERE r.movie_id = %s
            ORDER BY r.review_date DESC
        """, (movie_id,))
        reviews = cur.fetchall()

        if not reviews:
            print("No reviews found for this movie.")
            return

        print(f"\n--- Reviews for Movie ID {movie_id} ---")
        for review in reviews:
            print(f"{review[0]} | Rating: {review[1]} | {review[2]} | {review[3]}")

    except Exception as e:
        print("Error retrieving reviews:", e)

    finally:
        cur.close()
        conn.close()



def show_user_reviews(user_id):
    conn = connect()
    if conn is None:
        return

    cur = conn.cursor()

    try:
        print("=== Your Reviews ===")

        cur.execute("""
            SELECT m.title, r.rating, r.review, r.review_date
            FROM ratings r
            JOIN movies m ON r.movie_id = m.id
            WHERE r.user_id = %s
            ORDER BY r.review_date DESC
        """, (user_id,))
        results = cur.fetchall()

        if not results:
            print("You haven't submitted any reviews yet.")
            return

        for row in results:
            print(f"{row[0]} | Rating: {row[1]} | {row[2]} | {row[3]}")

    except Exception as e:
        print("Error retrieving your reviews:", e)

    finally:
        cur.close()
        conn.close()


def main_menu(user_id):  #menu system
    while True:
        print("\n=== Main Menu ===")
        print("1. List Movies")
        print("2. Rate a Movie")
        print("3. Show All Reviews for a Movie")
        print("4. Show My Reviews")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == "1":
            list_movies()
        elif choice == "2":
            rate_movie(user_id)
        elif choice == "3":
            show_reviews()
        elif choice == "4":
            show_user_reviews(user_id)
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")



if __name__ == "__main__":
    login_user()
