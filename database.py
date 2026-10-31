
import sqlite3


def connect_db():
    return sqlite3.connect("edutrack.db")


def create_table():
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            roll_no TEXT UNIQUE NOT NULL,
            course TEXT NOT NULL,
            semester INTEGER NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS marks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            roll_no TEXT UNIQUE NOT NULL,
            subject1 REAL NOT NULL,
            subject2 REAL NOT NULL,
            subject3 REAL NOT NULL,
            subject4 REAL NOT NULL,
            subject5 REAL NOT NULL,
            FOREIGN KEY (roll_no) REFERENCES students(roll_no)
        )
    """)

    connection.commit()
    connection.close()


if __name__ == "__main__":
    create_table()
    print("Database and tables are ready!")
