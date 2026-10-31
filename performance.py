
from database import connect_db


def save_marks(roll_no, marks):
    connection = connect_db()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "SELECT roll_no FROM students WHERE roll_no = ?",
            (roll_no,)
        )

        if cursor.fetchone() is None:
            return "Error: Student roll number not found."

        cursor.execute("""
            INSERT INTO marks (
                roll_no, subject1, subject2, subject3, subject4, subject5
            )
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(roll_no) DO UPDATE SET
                subject1 = excluded.subject1,
                subject2 = excluded.subject2,
                subject3 = excluded.subject3,
                subject4 = excluded.subject4,
                subject5 = excluded.subject5
        """, (roll_no, *marks))

        connection.commit()
        return "Marks saved successfully!"

    except Exception as error:
        return f"Error: {error}"

    finally:
        connection.close()


def get_performance(roll_no):
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT subject1, subject2, subject3, subject4, subject5
        FROM marks
        WHERE roll_no = ?
    """, (roll_no,))

    result = cursor.fetchone()
    connection.close()

    if result is None:
        return None

    total = sum(result)
    percentage = total / 5

    if percentage >= 90:
        grade = "A+"
    elif percentage >= 80:
        grade = "A"
    elif percentage >= 70:
        grade = "B"
    elif percentage >= 60:
        grade = "C"
    elif percentage >= 50:
        grade = "D"
    else:
        grade = "F"

    return {
        "marks": result,
        "total": total,
        "percentage": percentage,
        "grade": grade
    }
