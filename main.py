
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

from student import view_students, search_student, delete_student
from database import connect_db
from add_student import open_add_student
from marks_gui import open_marks_window
from performance import get_performance


root = tk.Tk()
root.title("EduTrack - Student Performance Analytics")
root.geometry("1100x700")
root.configure(bg="#F4F6FA")
root.resizable(False, False)


# ---------------- HEADER ----------------

header = tk.Frame(root, bg="#243B64", height=115)
header.pack(fill="x")
header.pack_propagate(False)

tk.Label(
    header,
    text="EduTrack",
    font=("Arial", 28, "bold"),
    bg="#243B64",
    fg="white"
).pack(pady=(18, 2))

tk.Label(
    header,
    text="Student Performance Analytics System",
    font=("Arial", 12),
    bg="#243B64",
    fg="#E0E7FF"
).pack()


# ---------------- SUMMARY CARDS ----------------

summary = tk.Frame(root, bg="#F4F6FA")
summary.pack(fill="x", padx=25, pady=25)


def create_card(parent, title):
    card = tk.Frame(
        parent,
        bg="white",
        highlightbackground="#D9DFEA",
        highlightthickness=1,
        width=320,
        height=105
    )
    card.pack(side="left", expand=True, fill="x", padx=8)
    card.pack_propagate(False)

    tk.Label(
        card,
        text=title,
        font=("Arial", 11),
        bg="white",
        fg="#555555"
    ).pack(pady=(17, 5))

    value = tk.Label(
        card,
        text="0",
        font=("Arial", 23, "bold"),
        bg="white",
        fg="#243B64"
    )
    value.pack()

    return value


total_label = create_card(summary, "Total Students")
average_label = create_card(summary, "Average Percentage")
highest_label = create_card(summary, "Highest Percentage")


# ---------------- DASHBOARD CONTENT ----------------

content = tk.Frame(root, bg="#F4F6FA")
content.pack(fill="both", expand=True, padx=35, pady=5)

tk.Label(
    content,
    text="Student Management",
    font=("Arial", 17, "bold"),
    bg="#F4F6FA",
    fg="#243B64"
).pack(anchor="w", pady=(5, 15))


def refresh_dashboard():
    students = view_students()
    total_label.config(text=str(len(students)))

    percentages = []

    for student in students:
        result = get_performance(student[2])

        if result is not None:
            percentages.append(result["percentage"])

    if percentages:
        average_label.config(
            text=f"{sum(percentages) / len(percentages):.2f}%"
        )
        highest_label.config(
            text=f"{max(percentages):.2f}%"
        )
    else:
        average_label.config(text="N/A")
        highest_label.config(text="N/A")


def create_button(parent, text, command, color="#3157A4"):
    return tk.Button(
        parent,
        text=text,
        command=command,
        font=("Arial", 11, "bold"),
        bg=color,
        fg="white",
        activebackground="#1E3A70",
        activeforeground="white",
        padx=15,
        pady=12,
        width=19,
        cursor="hand2"
    )


# ---------------- ADD STUDENT ----------------

def open_add_form():
    window = open_add_student()
    root.wait_window(window)
    refresh_dashboard()


# ---------------- ENTER MARKS ----------------

def open_marks_form():
    window = open_marks_window()
    root.wait_window(window)
    refresh_dashboard()


# ---------------- VIEW STUDENTS ----------------

def show_students():
    students = view_students()

    window = tk.Toplevel(root)
    window.title("All Students")
    window.geometry("850x420")
    window.configure(bg="#F4F6FA")

    tk.Label(
        window,
        text="Registered Students",
        font=("Arial", 19, "bold"),
        bg="#F4F6FA",
        fg="#243B64"
    ).pack(pady=18)

    columns = ("ID", "Name", "Roll Number", "Course", "Semester")

    table = ttk.Treeview(
        window,
        columns=columns,
        show="headings",
        height=12
    )

    for column in columns:
        table.heading(column, text=column)
        table.column(column, width=145, anchor="center")

    table.pack(fill="both", expand=True, padx=20, pady=10)

    for student in students:
        table.insert("", "end", values=student)

    if not students:
        messagebox.showinfo(
            "No Students",
            "No students have been added yet.",
            parent=window
        )


# ---------------- SEARCH STUDENT ----------------

def search_student_form():
    roll_no = simpledialog.askstring(
        "Search Student",
        "Enter student roll number:",
        parent=root
    )

    if roll_no is None:
        return

    roll_no = roll_no.strip()

    if not roll_no:
        messagebox.showwarning(
            "Missing Information",
            "Please enter a roll number.",
            parent=root
        )
        return

    student = search_student(roll_no)

    if student is None:
        messagebox.showinfo(
            "Not Found",
            "No student found with this roll number.",
            parent=root
        )
        return

    result = get_performance(roll_no)

    details = (
        f"Student ID: {student[0]}\n"
        f"Name: {student[1]}\n"
        f"Roll Number: {student[2]}\n"
        f"Course: {student[3]}\n"
        f"Semester: {student[4]}\n"
    )

    if result:
        details += (
            f"\nTotal Marks: {result['total']}/500"
            f"\nPercentage: {result['percentage']:.2f}%"
            f"\nGrade: {result['grade']}"
        )
    else:
        details += "\nMarks: Not entered yet"

    messagebox.showinfo("Student Details", details, parent=root)


# ---------------- DELETE STUDENT ----------------

def delete_student_form():
    roll_no = simpledialog.askstring(
        "Delete Student",
        "Enter the roll number of the student to delete:",
        parent=root
    )

    if roll_no is None:
        return

    roll_no = roll_no.strip()

    if not roll_no:
        messagebox.showwarning(
            "Missing Information",
            "Please enter a roll number.",
            parent=root
        )
        return

    student = search_student(roll_no)

    if student is None:
        messagebox.showinfo(
            "Not Found",
            "No student found with this roll number.",
            parent=root
        )
        return

    confirm = messagebox.askyesno(
        "Confirm Delete",
        f"Delete student {student[1]} ({roll_no})?\n"
        "Their saved marks will also be deleted.",
        parent=root
    )

    if not confirm:
        return

    connection = connect_db()

    try:
        cursor = connection.cursor()
        cursor.execute(
            "DELETE FROM marks WHERE roll_no = ?",
            (roll_no,)
        )
        connection.commit()
    finally:
        connection.close()

    deleted = delete_student(roll_no)

    if deleted:
        messagebox.showinfo(
            "Deleted",
            "Student and their marks were deleted successfully.",
            parent=root
        )
        refresh_dashboard()


# ---------------- PERFORMANCE CHART ----------------

def show_chart():
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        messagebox.showerror(
            "Missing Library",
            "Matplotlib is not installed.\n"
            "Install it using: python -m pip install matplotlib",
            parent=root
        )
        return

    students = view_students()
    names = []
    percentages = []

    for student in students:
        result = get_performance(student[2])

        if result is not None:
            names.append(student[1])
            percentages.append(result["percentage"])

    if not percentages:
        messagebox.showinfo(
            "No Performance Data",
            "Add students and save their marks before viewing the chart.",
            parent=root
        )
        return

    plt.figure(figsize=(9, 5))
    plt.bar(names, percentages)
    plt.title("Student Performance Comparison")
    plt.xlabel("Students")
    plt.ylabel("Percentage (%)")
    plt.ylim(0, 100)
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.show()


# ---------------- BUTTONS ----------------

row_one = tk.Frame(content, bg="#F4F6FA")
row_one.pack(anchor="w", pady=5)

create_button(
    row_one, "+ Add Student", open_add_form
).pack(side="left", padx=8, pady=8)

create_button(
    row_one, "View All Students", show_students
).pack(side="left", padx=8, pady=8)

create_button(
    row_one, "Search Student", search_student_form
).pack(side="left", padx=8, pady=8)


row_two = tk.Frame(content, bg="#F4F6FA")
row_two.pack(anchor="w", pady=5)

create_button(
    row_two, "Enter Marks", open_marks_form
).pack(side="left", padx=8, pady=8)

create_button(
    row_two, "Delete Student", delete_student_form,
    "#B93838"
).pack(side="left", padx=8, pady=8)

create_button(
    row_two, "Performance Chart", show_chart,
    "#247A59"
).pack(side="left", padx=8, pady=8)


tk.Label(
    root,
    text="EduTrack | Student Performance Analytics System",
    font=("Arial", 9),
    bg="#F4F6FA",
    fg="#777777"
).pack(pady=12)


refresh_dashboard()
root.mainloop()
