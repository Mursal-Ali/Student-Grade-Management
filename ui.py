
import tkinter as tk
from tkinter import ttk, messagebox

import student_manager


class StudentGradeManagementApp:
    """Main application window for the Student Grade Management System."""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Student Grade Management System")
        self.root.geometry("1150x750")
        self.root.minsize(1000, 650)
        self.root.configure(bg="#F4F6FB")

        self.colors = {
            "sidebar": "#172554",
            "sidebar_hover": "#263B70",
            "primary": "#4F46E5",
            "primary_hover": "#4338CA",
            "background": "#F4F6FB",
            "white": "#FFFFFF",
            "text": "#1E293B",
            "muted": "#64748B",
            "border": "#E2E8F0",
            "success": "#15803D",
            "danger": "#DC2626",
        }

        self.student_id_var = tk.StringVar()
        self.name_var = tk.StringVar()
        self.marks_var = tk.StringVar()
        self.search_var = tk.StringVar()

        self.pages = {}
        self.stat_labels = {}

        self.configure_styles()
        self.build_layout()
        self.build_dashboard_page()
        self.build_students_page()

        self.show_page("dashboard")
        self.refresh_data()

    def configure_styles(self):
        """Configure the appearance of ttk widgets."""
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Treeview",
            background=self.colors["white"],
            foreground=self.colors["text"],
            rowheight=38,
            fieldbackground=self.colors["white"],
            font=("Segoe UI", 10),
        )

        style.configure(
            "Treeview.Heading",
            background="#F1F5F9",
            foreground=self.colors["text"],
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            padding=10,
        )

        style.map(
            "Treeview",
            background=[("selected", "#E0E7FF")],
            foreground=[("selected", self.colors["text"])],
        )

    def build_layout(self):
        """Create the main application layout."""
        container = tk.Frame(self.root, bg=self.colors["background"])
        container.pack(fill="both", expand=True)

        self.sidebar = tk.Frame(
            container,
            bg=self.colors["sidebar"],
            width=230,
        )
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        self.content = tk.Frame(
            container,
            bg=self.colors["background"],
        )
        self.content.pack(side="right", fill="both", expand=True)

        self.build_sidebar()
        self.build_header()

        self.page_container = tk.Frame(
            self.content,
            bg=self.colors["background"],
        )
        self.page_container.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(10, 25),
        )

    def build_sidebar(self):
        """Create the navigation sidebar."""
        tk.Label(
            self.sidebar,
            text="SGMS",
            bg=self.colors["sidebar"],
            fg=self.colors["white"],
            font=("Segoe UI", 24, "bold"),
        ).pack(anchor="w", padx=25, pady=(30, 0))

        tk.Label(
            self.sidebar,
            text="STUDENT MANAGEMENT",
            bg=self.colors["sidebar"],
            fg="#A5B4FC",
            font=("Segoe UI", 8, "bold"),
        ).pack(anchor="w", padx=27, pady=(2, 35))

        tk.Label(
            self.sidebar,
            text="MAIN MENU",
            bg=self.colors["sidebar"],
            fg="#94A3B8",
            font=("Segoe UI", 9, "bold"),
        ).pack(anchor="w", padx=25, pady=(0, 12))

        self.create_nav_button("Dashboard", "dashboard")
        self.create_nav_button("Student Records", "students")

        tk.Frame(
            self.sidebar,
            bg="#334155",
            height=1,
        ).pack(fill="x", padx=20, pady=25)

        tk.Label(
            self.sidebar,
            text="Student Grade\nManagement System",
            bg=self.colors["sidebar"],
            fg="#CBD5E1",
            font=("Segoe UI", 9),
            justify="left",
        ).pack(anchor="w", padx=25, side="bottom", pady=25)

    def create_nav_button(self, text, page_name):
        """Create a sidebar navigation button."""
        button = tk.Button(
            self.sidebar,
            text=f"   {text}",
            command=lambda: self.show_page(page_name),
            bg=self.colors["sidebar"],
            fg="#E2E8F0",
            activebackground=self.colors["sidebar_hover"],
            activeforeground=self.colors["white"],
            font=("Segoe UI", 10, "bold"),
            anchor="w",
            relief="flat",
            bd=0,
            padx=15,
            pady=13,
            cursor="hand2",
        )
        button.pack(fill="x", padx=12, pady=3)

    def build_header(self):
        """Create the application header."""
        header = tk.Frame(
            self.content,
            bg=self.colors["white"],
            height=85,
        )
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="Student Grade Management",
            bg=self.colors["white"],
            fg=self.colors["text"],
            font=("Segoe UI", 17, "bold"),
        ).pack(side="left", padx=30)

        tk.Label(
            header,
            text="Academic Records System",
            bg=self.colors["white"],
            fg=self.colors["muted"],
            font=("Segoe UI", 10),
        ).pack(side="right", padx=30)

    def build_dashboard_page(self):
        """Build the dashboard page."""
        page = tk.Frame(
            self.page_container,
            bg=self.colors["background"],
        )
        self.pages["dashboard"] = page

        self.add_page_heading(
            page,
            "Dashboard",
            "Overview of student academic performance.",
        )

        cards_frame = tk.Frame(
            page,
            bg=self.colors["background"],
        )
        cards_frame.pack(fill="x", pady=(20, 25))

        cards = [
            ("Total Students", "total", "#EEF2FF", "#4338CA"),
            ("Class Average", "average", "#ECFDF5", "#15803D"),
            ("Highest Grade", "grade", "#FFF7ED", "#C2410C"),
        ]

        for title, key, background, foreground in cards:
            card = tk.Frame(
                cards_frame,
                bg=self.colors["white"],
                highlightbackground=self.colors["border"],
                highlightthickness=1,
            )
            card.pack(
                side="left",
                fill="both",
                expand=True,
                padx=(0, 15),
            )

            tk.Label(
                card,
                text=title,
                bg=self.colors["white"],
                fg=self.colors["muted"],
                font=("Segoe UI", 10),
            ).pack(anchor="w", padx=20, pady=(18, 8))

            value = tk.Label(
                card,
                text="0",
                bg=self.colors["white"],
                fg=foreground,
                font=("Segoe UI", 25, "bold"),
            )
            value.pack(anchor="w", padx=20, pady=(0, 18))

            self.stat_labels[key] = value

        overview = tk.Frame(
            page,
            bg=self.colors["white"],
            highlightbackground=self.colors["border"],
            highlightthickness=1,
        )
        overview.pack(fill="both", expand=True)

        tk.Label(
            overview,
            text="Welcome to your Dashboard",
            bg=self.colors["white"],
            fg=self.colors["text"],
            font=("Segoe UI", 15, "bold"),
        ).pack(anchor="w", padx=25, pady=(25, 10))

        tk.Label(
            overview,
            text=(
                "Manage student records, calculate grades, and monitor "
                "academic performance from one place."
            ),
            bg=self.colors["white"],
            fg=self.colors["muted"],
            font=("Segoe UI", 10),
            wraplength=650,
            justify="left",
        ).pack(anchor="w", padx=25, pady=(0, 20))

        tk.Button(
            overview,
            text="Manage Students",
            command=lambda: self.show_page("students"),
            bg=self.colors["primary"],
            fg=self.colors["white"],
            activebackground=self.colors["primary_hover"],
            activeforeground=self.colors["white"],
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            bd=0,
            padx=20,
            pady=11,
            cursor="hand2",
        ).pack(anchor="w", padx=25, pady=(0, 25))

    def build_students_page(self):
        """Build the student registration and records page."""
        page = tk.Frame(
            self.page_container,
            bg=self.colors["background"],
        )
        self.pages["students"] = page

        self.add_page_heading(
            page,
            "Student Records",
            "Register, search, and manage student academic records.",
        )

        form_card = tk.Frame(
            page,
            bg=self.colors["white"],
            highlightbackground=self.colors["border"],
            highlightthickness=1,
        )
        form_card.pack(fill="x", pady=(18, 15))

        tk.Label(
            form_card,
            text="Register New Student",
            bg=self.colors["white"],
            fg=self.colors["text"],
            font=("Segoe UI", 13, "bold"),
        ).pack(anchor="w", padx=20, pady=(18, 12))

        fields = tk.Frame(form_card, bg=self.colors["white"])
        fields.pack(fill="x", padx=20, pady=(0, 15))

        self.create_form_field(fields, "Student ID", self.student_id_var)
        self.create_form_field(fields, "Student Name", self.name_var)
        self.create_form_field(fields, "Marks (0-100)", self.marks_var)

        tk.Button(
            form_card,
            text="Register Student",
            command=self.register_student,
            bg=self.colors["primary"],
            fg=self.colors["white"],
            activebackground=self.colors["primary_hover"],
            activeforeground=self.colors["white"],
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            bd=0,
            padx=20,
            pady=10,
            cursor="hand2",
        ).pack(anchor="e", padx=20, pady=(0, 18))

        records_card = tk.Frame(
            page,
            bg=self.colors["white"],
            highlightbackground=self.colors["border"],
            highlightthickness=1,
        )
        records_card.pack(fill="both", expand=True)

        top = tk.Frame(records_card, bg=self.colors["white"])
        top.pack(fill="x", padx=20, pady=(18, 12))

        tk.Label(
            top,
            text="All Students",
            bg=self.colors["white"],
            fg=self.colors["text"],
            font=("Segoe UI", 13, "bold"),
        ).pack(side="left")

        search_frame = tk.Frame(top, bg=self.colors["white"])
        search_frame.pack(side="right")

        search_entry = ttk.Entry(
            search_frame,
            textvariable=self.search_var,
            width=25,
            font=("Segoe UI", 10),
        )
        search_entry.pack(side="left", padx=(0, 8))
        search_entry.bind("<Return>", lambda event: self.search_students())

        tk.Button(
            search_frame,
            text="Search",
            command=self.search_students,
            bg="#E0E7FF",
            fg="#3730A3",
            relief="flat",
            padx=12,
            pady=6,
            cursor="hand2",
        ).pack(side="left", padx=(0, 6))

        tk.Button(
            search_frame,
            text="Refresh",
            command=self.refresh_data,
            bg="#F1F5F9",
            fg=self.colors["text"],
            relief="flat",
            padx=12,
            pady=6,
            cursor="hand2",
        ).pack(side="left")

        table_frame = tk.Frame(records_card, bg=self.colors["white"])
        table_frame.pack(fill="both", expand=True, padx=20, pady=(0, 12))

        columns = ("id", "name", "marks", "grade")

        self.student_table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            selectmode="browse",
        )

        self.student_table.heading("id", text="STUDENT ID")
        self.student_table.heading("name", text="STUDENT NAME")
        self.student_table.heading("marks", text="MARKS")
        self.student_table.heading("grade", text="GRADE")

        self.student_table.column("id", width=150, anchor="center")
        self.student_table.column("name", width=300, anchor="w")
        self.student_table.column("marks", width=120, anchor="center")
        self.student_table.column("grade", width=100, anchor="center")

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.student_table.yview,
        )
        self.student_table.configure(yscrollcommand=scrollbar.set)

        self.student_table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        actions = tk.Frame(records_card, bg=self.colors["white"])
        actions.pack(fill="x", padx=20, pady=(0, 18))

        tk.Button(
            actions,
            text="Delete Selected Student",
            command=self.delete_selected_student,
            bg="#FEE2E2",
            fg=self.colors["danger"],
            activebackground="#FECACA",
            relief="flat",
            padx=15,
            pady=9,
            cursor="hand2",
        ).pack(side="right")

    def create_form_field(self, parent, label_text, variable):
        """Create a labeled form input."""
        field = tk.Frame(parent, bg=self.colors["white"])
        field.pack(side="left", fill="x", expand=True, padx=(0, 15))

        tk.Label(
            field,
            text=label_text,
            bg=self.colors["white"],
            fg=self.colors["muted"],
            font=("Segoe UI", 9, "bold"),
        ).pack(anchor="w", pady=(0, 7))

        ttk.Entry(
            field,
            textvariable=variable,
            font=("Segoe UI", 10),
        ).pack(fill="x", ipady=7)

    def add_page_heading(self, parent, title, subtitle):
        """Add a page title and description."""
        tk.Label(
            parent,
            text=title,
            bg=self.colors["background"],
            fg=self.colors["text"],
            font=("Segoe UI", 21, "bold"),
        ).pack(anchor="w")

        tk.Label(
            parent,
            text=subtitle,
            bg=self.colors["background"],
            fg=self.colors["muted"],
            font=("Segoe UI", 10),
        ).pack(anchor="w", pady=(5, 0))

    def show_page(self, page_name):
        """Display the selected application page."""
        for page in self.pages.values():
            page.pack_forget()

        self.pages[page_name].pack(fill="both", expand=True)

        if page_name == "students":
            self.refresh_data()

    def register_student(self):
        """Validate and register a student."""
        try:
            student = student_manager.add_student(
                self.student_id_var.get(),
                self.name_var.get(),
                self.marks_var.get(),
            )

            self.student_id_var.set("")
            self.name_var.set("")
            self.marks_var.set("")

            self.refresh_data()

            messagebox.showinfo(
                "Registration Successful",
                (
                    f"{student['name']} has been registered successfully.\n"
                    f"Grade: {student['grade']}"
                ),
            )

        except ValueError as error:
            messagebox.showerror("Registration Error", str(error))

        except (OSError, TypeError) as error:
            messagebox.showerror(
                "System Error",
                f"Unable to save the student record:\n{error}",
            )

    def refresh_data(self):
        """Refresh student records and dashboard statistics."""
        try:
            students = student_manager.view_students()
            average = student_manager.calculate_average()

            if "total" in self.stat_labels:
                self.stat_labels["total"].config(text=str(len(students)))

                self.stat_labels["average"].config(
                    text=f"{average:.1f}%" if average is not None else "0.0%"
                )

                grades = [student["grade"] for student in students]
                highest_grade = (
                    min(grades, key=lambda grade: "ABCDE".index(grade))
                    if grades else "-"
                )

                self.stat_labels["grade"].config(text=highest_grade)

            if hasattr(self, "student_table"):
                self.populate_table(students)

        except (ValueError, OSError, KeyError, TypeError) as error:
            messagebox.showerror(
                "Data Error",
                f"Unable to load student records:\n{error}",
            )

    def populate_table(self, students):
        """Display student records in the table."""
        for item in self.student_table.get_children():
            self.student_table.delete(item)

        for student in students:
            self.student_table.insert(
                "",
                "end",
                values=(
                    student["id"],
                    student["name"],
                    f"{student['marks']:g}",
                    student["grade"],
                ),
            )

    def search_students(self):
        """Search students by ID or name."""
        search_term = self.search_var.get().strip().lower()

        try:
            students = student_manager.view_students()

            if search_term:
                students = [
                    student for student in students
                    if search_term in student["id"].lower()
                    or search_term in student["name"].lower()
                ]

            self.populate_table(students)

            if not students:
                messagebox.showinfo(
                    "Search Results",
                    "No matching student records were found.",
                )

        except (ValueError, OSError, KeyError, TypeError) as error:
            messagebox.showerror("Search Error", str(error))

    def delete_selected_student(self):
        """Delete the currently selected student."""
        selected = self.student_table.selection()

        if not selected:
            messagebox.showwarning(
                "No Selection",
                "Please select a student record to delete.",
            )
            return

        values = self.student_table.item(selected[0], "values")
        student_id = values[0]
        student_name = values[1]

        confirmed = messagebox.askyesno(
            "Confirm Deletion",
            f"Are you sure you want to delete {student_name}?",
        )

        if not confirmed:
            return

        try:
            deleted = student_manager.delete_student(student_id)

            if deleted:
                self.search_var.set("")
                self.refresh_data()

                messagebox.showinfo(
                    "Deletion Successful",
                    "The student record has been deleted.",
                )
            else:
                messagebox.showwarning(
                    "Record Not Found",
                    "The selected student record could not be found.",
                )

        except (ValueError, OSError) as error:
            messagebox.showerror("Deletion Error", str(error))

    def run(self):
        """Start the application."""
        self.root.mainloop()
