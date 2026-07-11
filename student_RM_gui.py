import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox


conn = sqlite3.connect("result.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students(
    id TEXT PRIMARY KEY,
    name TEXT,
    sub1 INTEGER,
    sub2 INTEGER,
    sub3 INTEGER,
    total INTEGER,
    percentage REAL,
    grade TEXT
)
""")
conn.commit()


def add_student():
    student_id = entry_id.get()
    name = entry_name.get()

    if not student_id or not name:
        messagebox.showerror("Error", "ID and Name are required")
        return

    try:
        cursor.execute("INSERT INTO students(id, name) VALUES(?, ?)", (student_id, name))
        conn.commit()
        messagebox.showinfo("Success", "Student added successfully!")
        clear_fields()
        load_all_students()
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Student ID already exists")

def add_marks():
    student_id = entry_id.get()

    if not student_id:
        messagebox.showerror("Error", "Enter Student ID")
        return

    try:
        s1 = int(entry_sub1.get())
        s2 = int(entry_sub2.get())
        s3 = int(entry_sub3.get())
    except ValueError:
        messagebox.showerror("Error", "Marks must be integers")
        return

    total = s1 + s2 + s3
    percentage = total / 3

    if percentage >= 90:
        grade = 'A'
    elif percentage >= 75:
        grade = 'B'
    elif percentage >= 50:
        grade = 'C'
    else:
        grade = 'F'

    cursor.execute("""
    UPDATE students 
    SET sub1=?, sub2=?, sub3=?, total=?, percentage=?, grade=? 
    WHERE id=?
    """, (s1, s2, s3, total, percentage, grade, student_id))

    if cursor.rowcount == 0:
        messagebox.showerror("Error", "Student ID not found")
    else:
        conn.commit()
        messagebox.showinfo("Success", "Marks added successfully!")
        clear_fields()
        load_all_students()

def view_result():
    student_id = entry_id.get()

    if not student_id:
        messagebox.showerror("Error", "Enter Student ID")
        return

    cursor.execute("SELECT * FROM students WHERE id=?", (student_id,))
    data = cursor.fetchone()

    if data:
        result_text.set(
            f"ID: {data[0]}\n"
            f"Name: {data[1]}\n"
            f"Subject 1: {data[2]}\n"
            f"Subject 2: {data[3]}\n"
            f"Subject 3: {data[4]}\n"
            f"Total: {data[5]}\n"
            f"Percentage: {data[6]:.2f}\n"
            f"Grade: {data[7]}"
        )
    else:
        messagebox.showerror("Error", "Student not found")

def delete_student():
    student_id = entry_id.get()

    if not student_id:
        messagebox.showerror("Error", "Enter Student ID")
        return

    cursor.execute("DELETE FROM students WHERE id=?", (student_id,))
    conn.commit()

    if cursor.rowcount == 0:
        messagebox.showerror("Error", "Student not found")
    else:
        messagebox.showinfo("Success", "Deleted successfully!")
        clear_fields()
        load_all_students()
        result_text.set("")

def load_all_students():
    for row in tree.get_children():
        tree.delete(row)

    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()

    for row in rows:
        tree.insert("", tk.END, values=row)

def clear_fields():
    entry_id.delete(0, tk.END)
    entry_name.delete(0, tk.END)
    entry_sub1.delete(0, tk.END)
    entry_sub2.delete(0, tk.END)
    entry_sub3.delete(0, tk.END)

root = tk.Tk()
root.title("Student Result Management System")
root.geometry("950x600")
root.configure(bg="#f0f4f8")

title = tk.Label(root, text="Student Result Management System", font=("Arial", 18, "bold"), bg="#f0f4f8", fg="#1f3b4d")
title.pack(pady=10)

form_frame = tk.Frame(root, bg="#f0f4f8")
form_frame.pack(pady=10)

tk.Label(form_frame, text="Student ID", bg="#f0f4f8", font=("Arial", 11)).grid(row=0, column=0, padx=10, pady=5)
entry_id = tk.Entry(form_frame, font=("Arial", 11))
entry_id.grid(row=0, column=1, padx=10, pady=5)

tk.Label(form_frame, text="Name", bg="#f0f4f8", font=("Arial", 11)).grid(row=1, column=0, padx=10, pady=5)
entry_name = tk.Entry(form_frame, font=("Arial", 11))
entry_name.grid(row=1, column=1, padx=10, pady=5)

tk.Label(form_frame, text="Subject 1", bg="#f0f4f8", font=("Arial", 11)).grid(row=0, column=2, padx=10, pady=5)
entry_sub1 = tk.Entry(form_frame, font=("Arial", 11))
entry_sub1.grid(row=0, column=3, padx=10, pady=5)

tk.Label(form_frame, text="Subject 2", bg="#f0f4f8", font=("Arial", 11)).grid(row=1, column=2, padx=10, pady=5)
entry_sub2 = tk.Entry(form_frame, font=("Arial", 11))
entry_sub2.grid(row=1, column=3, padx=10, pady=5)

tk.Label(form_frame, text="Subject 3", bg="#f0f4f8", font=("Arial", 11)).grid(row=2, column=2, padx=10, pady=5)
entry_sub3 = tk.Entry(form_frame, font=("Arial", 11))
entry_sub3.grid(row=2, column=3, padx=10, pady=5)

button_frame = tk.Frame(root, bg="#f0f4f8")
button_frame.pack(pady=10)

tk.Button(button_frame, text="Add Student", command=add_student, bg="#4caf50", fg="white", width=15).grid(row=0, column=0, padx=8, pady=5)
tk.Button(button_frame, text="Add Marks", command=add_marks, bg="#2196f3", fg="white", width=15).grid(row=0, column=1, padx=8, pady=5)
tk.Button(button_frame, text="View Result", command=view_result, bg="#ff9800", fg="white", width=15).grid(row=0, column=2, padx=8, pady=5)
tk.Button(button_frame, text="Delete Student", command=delete_student, bg="#f44336", fg="white", width=15).grid(row=0, column=3, padx=8, pady=5)
tk.Button(button_frame, text="Clear Fields", command=clear_fields, bg="#607d8b", fg="white", width=15).grid(row=0, column=4, padx=8, pady=5)

result_text = tk.StringVar()
result_label = tk.Label(root, textvariable=result_text, font=("Arial", 12), bg="#ffffff", fg="#222", width=50, height=8, relief="solid", anchor="nw", justify="left")
result_label.pack(pady=15)

columns = ("ID", "Name", "Sub1", "Sub2", "Sub3", "Total", "Percentage", "Grade")
tree = ttk.Treeview(root, columns=columns, show="headings", height=10)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=100, anchor="center")

tree.pack(pady=10, fill="x")

load_all_students()

root.mainloop()

conn.close()
