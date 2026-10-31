
import tkinter as tk
from tkinter import messagebox

from performance import save_marks, get_performance


def open_marks_window():
    window = tk.Toplevel()
    window.title("Student Marks & Performance")
    window.geometry("520x610")
    window.configure(bg="#F4F6FA")
    window.resizable(False, False)

    tk.Label(
        window,
        text="Marks & Performance",
        font=("Arial", 21, "bold"),
        bg="#F4F6FA",
        fg="#243B64"
    ).pack(pady=22)

    tk.Label(
        window,
        text="Enter marks out of 100 for each subject",
        font=("Arial", 10),
        bg="#F4F6FA",
        fg="#555555"
    ).pack(pady=(0, 15))

    form = tk.Frame(window, bg="#F4F6FA")
    form.pack(padx=25)

    tk.Label(
        form,
        text="Student Roll Number",
        font=("Arial", 11),
        bg="#F4F6FA"
    ).grid(row=0, column=0, sticky="w", pady=10)

    roll_entry = tk.Entry(form, font=("Arial", 11), width=22)
    roll_entry.grid(row=0, column=1, padx=10, pady=10)

    entries = []

    for index in range(5):
        tk.Label(
            form,
            text=f"Subject {index + 1} Marks",
            font=("Arial", 11),
            bg="#F4F6FA"
        ).grid(row=index + 1, column=0, sticky="w", pady=10)

        entry = tk.Entry(form, font=("Arial", 11), width=22)
        entry.grid(row=index + 1, column=1, padx=10, pady=10)
        entries.append(entry)

    def save():
        roll_no = roll_entry.get().strip()

        if not roll_no:
            messagebox.showwarning(
                "Missing Roll Number",
                "Enter the student's roll number.",
                parent=window
            )
            return

        try:
            marks = [float(entry.get()) for entry in entries]

            if any(mark < 0 or mark > 100 for mark in marks):
                raise ValueError

        except ValueError:
            messagebox.showerror(
                "Invalid Marks",
                "Enter valid marks from 0 to 100 in all five subjects.",
                parent=window
            )
            return

        result = save_marks(roll_no, marks)

        if result == "Marks saved successfully!":
            messagebox.showinfo("Success", result, parent=window)
        else:
            messagebox.showerror("Error", result, parent=window)

    def view_result():
        roll_no = roll_entry.get().strip()

        if not roll_no:
            messagebox.showwarning(
                "Missing Roll Number",
                "Enter the student's roll number first.",
                parent=window
            )
            return

        result = get_performance(roll_no)

        if result is None:
            messagebox.showwarning(
                "No Result",
                "No marks have been saved for this student.",
                parent=window
            )
            return

        messagebox.showinfo(
            "Student Result",
            f"Roll Number: {roll_no}\n\n"
            f"Subject Marks: {result['marks']}\n"
            f"Total: {result['total']}/500\n"
            f"Percentage: {result['percentage']:.2f}%\n"
            f"Grade: {result['grade']}",
            parent=window
        )

    buttons = tk.Frame(window, bg="#F4F6FA")
    buttons.pack(pady=25)

    tk.Button(
        buttons,
        text="Save Marks",
        command=save,
        font=("Arial", 11, "bold"),
        bg="#3157A4",
        fg="white",
        padx=20,
        pady=10
    ).pack(side="left", padx=8)

    tk.Button(
        buttons,
        text="View Result",
        command=view_result,
        font=("Arial", 11, "bold"),
        bg="#243B64",
        fg="white",
        padx=20,
        pady=10
    ).pack(side="left", padx=8)

    return window


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()

    window = open_marks_window()
    root.wait_window(window)

    root.destroy()
