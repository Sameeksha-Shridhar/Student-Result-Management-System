import sqlite3

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
    id = input("Enter ID: ")
    name = input("Enter Name: ")

    cursor.execute("INSERT INTO students(id, name) VALUES(?, ?)", (id, name))
    conn.commit()
    print("Student added successfully!")


def add_marks():
    id =input("Enter Student ID: ")

    s1 = int(input("Enter marks for Subject 1: "))
    s2 = int(input("Enter marks for Subject 2: "))
    s3 = int(input("Enter marks for Subject 3: "))

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
    """, (s1, s2, s3, total, percentage, grade, id))

    conn.commit()
    print("Marks added successfully!")


def view_result():
    id = input("Enter Student ID: ")

    cursor.execute("SELECT * FROM students WHERE id=?", (id,))
    data = cursor.fetchone()

    if data:
        print("\n--- RESULT ---")
        print("ID:", data[0])
        print("Name:", data[1])
        print("Total:", data[5])
        print("Percentage:", data[6])
        print("Grade:", data[7])
    else:
        print("Student not found!")


def delete_student():
    id = input("Enter ID: ")
    cursor.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()
    print("Deleted successfully!")


def display_all():
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()

    for row in rows:
        print(row)



while True:
    print("\n1. Add Student")
    print("2. Add Marks")
    print("3. View Result")
    print("4. Display All")
    print("5. Delete Student")
    print("6. Exit")

    choice = int(input("Enter choice: "))

    if choice == 1:
        add_student()
    elif choice == 2:
        add_marks()
    elif choice == 3:
        view_result()
    elif choice == 4:
        display_all()
    elif choice == 5:
        delete_student()
    elif choice == 6:
        print("Exiting...")
        break   
    else:
        print("Invalid choice!")