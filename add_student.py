
import tkinter as tk
from tkinter import messagebox

from student import add_student


def open_add_student():
    window = tk.Toplevel()
    window.title("Add Student - EduTrack")
    window.geometry("450x450")
    window.configure(bg="#F4F6FA")
    window.resizable(False, False)

    tk.Label(
        window,
        text="Add New Student",
        font=("Arial", 21, "bold"),
        bg="#F4F6FA",
        fg="#243B64"
    ).pack(pady=25)

    form = tk.Frame(window, bg="#F4F6FA")
    form.pack(padx=35, pady=5)

    fields = [
        ("Student Name", 0),
        ("Roll Number", 1),
        ("Course", 2),
        ("Semester", 3)
    ]

    entries = {}

    for label_text, row in fields:
        tk.Label(
            form,
            text=label_text,
            font=("Arial", 11),
            bg="#F4F6FA"
        ).grid(row=row, column=0, sticky="w", pady=12)

        entry = tk.Entry(form, font=("Arial", 11), width=24)
        entry.grid(row=row, column=1, padx=12, pady=12)

        entries[label_text] = entry

    def save_student():
        name = entries["Student Name"].get().strip()
        roll_no = entries["Roll Number"].get().strip()
        course = entries["Course"].get().strip()
        semester_text = entries["Semester"].get().strip()

        if not all([name, roll_no, course, semester_text]):
            messagebox.showwarning(
                "Missing Information",
                "Please fill in all fields.",
                parent=window
            )
            return

        try:
            semester = int(semester_text)

            if semester < 1 or semester > 12:
                raise ValueError

        except ValueError:
            messagebox.showerror(
                "Invalid Semester",
                "Enter a valid semester number from 1 to 12.",
                parent=window
            )
            return

        result = add_student(name, roll_no, course, semester)

        if result == "Student added successfully!":
            messagebox.showinfo("Success", result, parent=window)

            for entry in entries.values():
                entry.delete(0, tk.END)

            entries["Student Name"].focus_set()

        else:
            messagebox.showerror("Error", result, parent=window)

    tk.Button(
        window,
        text="Save Student",
        command=save_student,
        font=("Arial", 11, "bold"),
        bg="#3157A4",
        fg="white",
        padx=25,
        pady=10
    ).pack(pady=25)

    return window


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()

    window = open_add_student()
    root.wait_window(window)

    root.destroy()
