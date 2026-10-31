
from database import connect_db


def add_student(name, roll_no, course, semester):
    connection = connect_db()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO students (name, roll_no, course, semester)
            VALUES (?, ?, ?, ?)
            """,
            (name, roll_no, course, semester)
        )
        connection.commit()
        return "Student added successfully!"

    except Exception as error:
        return f"Error: {error}"

    finally:
        connection.close()


def view_students():
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM students ORDER BY id")
    students = cursor.fetchall()

    connection.close()
    return students


def search_student(roll_no):
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM students WHERE roll_no = ?",
        (roll_no,)
    )
    student = cursor.fetchone()

    connection.close()
    return student


def delete_student(roll_no):
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM students WHERE roll_no = ?",
        (roll_no,)
    )

    connection.commit()
    deleted = cursor.rowcount > 0

    connection.close()
    return deleted
