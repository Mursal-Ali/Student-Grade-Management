
from student_manager import (
    add_student,
    view_students,
    search_student,
    delete_student,
    calculate_average
)


def display_menu():
    """Display the main application menu."""
    print("\n======================================")
    print("     STUDENT GRADE MANAGEMENT SYSTEM")
    print("======================================")
    print("1. Register New Student")
    print("2. View All Students")
    print("3. Search Student")
    print("4. Delete Student")
    print("5. Calculate Class Average")
    print("6. Exit")
    print("======================================")


def main():
    """Run the Student Grade Management System."""
    print("\nWelcome to Student Grade Management System!")

    while True:
        display_menu()

        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            add_student()

        elif choice == "2":
            view_students()

        elif choice == "3":
            search_student()

        elif choice == "4":
            delete_student()

        elif choice == "5":
            calculate_average()

        elif choice == "6":
            print("\nThank you for using the Student Grade Management System!")
            print("Goodbye!")
            break

        else:
            print("\nInvalid choice. Please select a number between 1 and 6.")


if __name__ == "__main__":
    main()
