
import json
import os

DATA_FILE = os.path.join("data", "students.json")


def load_students():
    """Load student records from the JSON file."""
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            students = json.load(file)
            return students if isinstance(students, list) else []

    except FileNotFoundError:
        return []

    except json.JSONDecodeError:
        print("Error: Student data file contains invalid JSON.")
        return []


def save_students(students):
    """Save student records to the JSON file."""
    os.makedirs("data", exist_ok=True)

    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(students, file, indent=4)


def add_student():
    """Register a new student."""
    students = load_students()

    student_id = input("Enter student ID: ").strip()

    if not student_id:
        print("Student ID cannot be empty.")
        return

    if any(student["id"] == student_id for student in students):
        print("A student with this ID already exists.")
        return

    name = input("Enter student name: ").strip()

    if not name:
        print("Student name cannot be empty.")
        return

    try:
        marks = float(input("Enter student marks (0-100): "))

        if not 0 <= marks <= 100:
            print("Marks must be between 0 and 100.")
            return

    except ValueError:
        print("Invalid input. Please enter numeric marks.")
        return

    student = {
        "id": student_id,
        "name": name,
        "marks": marks,
        "grade": calculate_grade(marks)
    }

    students.append(student)
    save_students(students)

    print(f"Student '{name}' registered successfully!")


def view_students():
    """Display all registered students."""
    students = load_students()

    if not students:
        print("No student records found.")
        return

    print("\n========== STUDENT RECORDS ==========")

    for student in students:
        print(f"ID: {student['id']}")
        print(f"Name: {student['name']}")
        print(f"Marks: {student['marks']}")
        print(f"Grade: {student['grade']}")
        print("------------------------------------")


def calculate_grade(marks):
    """Calculate a student's grade based on marks."""
    if marks >= 70:
        return "A"
    elif marks >= 60:
        return "B"
    elif marks >= 50:
        return "C"
    elif marks >= 40:
        return "D"
    else:
        return "E"


def search_student():
    """Search for a student using their ID."""
    students = load_students()

    student_id = input("Enter student ID to search: ").strip()

    student = next(
        (student for student in students if student["id"] == student_id),
        None
    )

    if student is None:
        print("Student not found.")
        return

    print("\n========== STUDENT DETAILS ==========")
    print(f"ID: {student['id']}")
    print(f"Name: {student['name']}")
    print(f"Marks: {student['marks']}")
    print(f"Grade: {student['grade']}")


def delete_student():
    """Delete a student record using their ID."""
    students = load_students()

    student_id = input("Enter student ID to delete: ").strip()

    student = next(
        (student for student in students if student["id"] == student_id),
        None
    )

    if student is None:
        print("Student not found.")
        return

    students.remove(student)
    save_students(students)

    print(f"Student '{student['name']}' deleted successfully!")


def calculate_average():
    """Calculate the average marks of all registered students."""
    students = load_students()

    if not students:
        print("No student records available.")
        return

    total_marks = sum(student["marks"] for student in students)
    average = total_marks / len(students)

    print(f"Class Average: {average:.2f}%")
