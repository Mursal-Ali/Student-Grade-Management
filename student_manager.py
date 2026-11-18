
import json
import math
from pathlib import Path


DATA_FILE = Path(__file__).resolve().parent / "data" / "students.json"


def load_students():
    """Load student records from the JSON file."""
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

    if not DATA_FILE.exists():
        save_students([])
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            students = json.load(file)

        if not isinstance(students, list):
            raise ValueError("Student data must be a list.")

        return students

    except json.JSONDecodeError as error:
        raise ValueError("The student data file contains invalid JSON.") from error


def save_students(students):
    """Save student records to the JSON file."""
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(students, file, indent=4)


def calculate_grade(marks):
    """Calculate a student's grade based on their marks."""
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


def add_student(student_id, name, marks):
    """Register a new student."""
    student_id = student_id.strip()
    name = name.strip()

    if not student_id:
        raise ValueError("Student ID is required.")

    if not name:
        raise ValueError("Student name is required.")

    try:
        marks = float(marks)
    except (TypeError, ValueError):
        raise ValueError("Please enter valid numeric marks.")

    if not math.isfinite(marks) or not 0 <= marks <= 100:
        raise ValueError("Marks must be between 0 and 100.")

    students = load_students()

    if any(
        student["id"].lower() == student_id.lower()
        for student in students
    ):
        raise ValueError("A student with this ID already exists.")

    student = {
        "id": student_id,
        "name": name,
        "marks": marks,
        "grade": calculate_grade(marks)
    }

    students.append(student)
    save_students(students)

    return student


def view_students():
    """Return all registered students."""
    return load_students()


def search_student(student_id):
    """Find a student using their ID."""
    student_id = student_id.strip().lower()

    students = load_students()

    for student in students:
        if student["id"].lower() == student_id:
            return student

    return None


def delete_student(student_id):
    """Delete a student using their ID."""
    student_id = student_id.strip().lower()

    students = load_students()

    updated_students = [
        student for student in students
        if student["id"].lower() != student_id
    ]

    if len(updated_students) == len(students):
        return False

    save_students(updated_students)

    return True


def calculate_average():
    """Calculate the average marks of all students."""
    students = load_students()

    if not students:
        return None

    total_marks = sum(student["marks"] for student in students)

    return total_marks / len(students)
