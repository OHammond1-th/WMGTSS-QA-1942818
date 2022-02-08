import datetime
import tkinter as tk
import pathlib
from psycopg2 import DatabaseError
from postrgesql_api import DB_API
import create_user
import create_course
import enroll_user

#database = DB_API("WMGTSS_QA", "administrator", "default")

print(f"{pathlib.Path().resolve()}\\Images\\WMG.png")

class CreateUserForm(tk.Toplevel):

    def __init__(self, root, role, **kw):
        super().__init__(root, **kw)

        self.root = root

        self.role = role
        self.user_data = []

        username = tk.StringVar()
        username_label = tk.Label(self, text=f"{role} username").pack()
        username_entry = tk.Entry(self, textvariable=username).pack()
        self.user_data.append(username)

        firstname = tk.StringVar()
        firstname_label = tk.Label(self, text=f"{role} firstname").pack()
        firstname_entry = tk.Entry(self, textvariable=firstname).pack()
        self.user_data.append(firstname)

        lastname = tk.StringVar()
        lastname_label = tk.Label(self, text=f"{role} lastname").pack()
        lastname_entry = tk.Entry(self, textvariable=lastname).pack()
        self.user_data.append(lastname)


        day = tk.StringVar()
        month = tk.StringVar()
        year = tk.StringVar()
        dateofbirth_label = tk.Label(self, text=f"{role} date of birth (dd/mm/yyyy)").pack()
        day_entry = tk.Entry(self, textvariable=day).pack(side=tk.LEFT)
        month_entry = tk.Entry(self, textvariable=month).pack(side=tk.LEFT)
        year_entry = tk.Entry(self, textvariable=year).pack(side=tk.LEFT)

        self.dob = ({
            "day": day,
            "month": month,
            "year": year
        })

        button_frame = tk.Frame(self)
        create_button = tk.Button(button_frame, text="Create", command=self.insert_data).pack()
        exit_button = tk.Button(button_frame, text="Done", command=self.exit).pack()
        button_frame.pack(side=tk.BOTTOM)

        self.root.grab_set()


    def insert_data(self):

        dateofbirth = datetime.date(
            int(self.dob["year"].get()),
            int(self.dob["month"].get()),
            int(self.dob["day"].get())
        )

        create_user.create_new_user(self.role, *self.user_data, dateofbirth)

    def exit(self):
        self.root.grab_release()
        self.destroy()


class CreateCourseForm(tk.Toplevel):

    def __init__(self, root, **kw):
        super().__init__(root, **kw)

        self.root = root

        self.name = tk.StringVar()
        name_label = tk.Label(self, text="Name").pack()
        name_entry = tk.Entry(self, textvariable=self.name).pack()

        start_day = tk.StringVar()
        start_month = tk.StringVar()
        start_year = tk.StringVar()
        start_date_label = tk.Label(self, text="Start Date (dd/mm/yyyy)").pack()
        start_day_entry = tk.Entry(self, textvariable=start_day).pack(side=tk.LEFT)
        start_month_entry = tk.Entry(self, textvariable=start_month).pack(side=tk.LEFT)
        start_year_entry = tk.Entry(self, textvariable=start_year).pack(side=tk.LEFT)

        self.start_date = ({
            "day": start_day,
            "month": start_month,
            "year": start_year
        })

        end_day = tk.StringVar()
        end_month = tk.StringVar()
        end_year = tk.StringVar()
        end_date_label = tk.Label(self, text="End Date (dd/mm/yyyy)").pack()
        end_day_entry = tk.Entry(self, textvariable=end_day).pack(side=tk.LEFT)
        end_month_entry = tk.Entry(self, textvariable=end_month).pack(side=tk.LEFT)
        end_year_entry = tk.Entry(self, textvariable=end_year).pack(side=tk.LEFT)

        self.end_date = ({
            "day": end_day,
            "month": end_month,
            "year": end_year
        })

        button_frame = tk.Frame(self)
        create_button = tk.Button(button_frame, text="Create", command=self.insert_data).pack()
        exit_button = tk.Button(button_frame, text="Done", command=self.exit).pack()
        button_frame.pack(side=tk.BOTTOM)

        self.root.grab_set()

    def insert_data(self):

        start_date = datetime.date(
            int(self.start_date["year"].get()),
            int(self.start_date["month"].get()),
            int(self.start_date["day"].get())
        )

        end_date = datetime.date(
            int(self.end_date["year"].get()),
            int(self.end_date["month"].get()),
            int(self.end_date["day"].get())
        )

        create_course.create_new_course(self.name.get(), start_date, end_date)

    def exit(self):
        self.root.grab_release()
        self.destroy()


class AdminTool(tk.Tk):

    def __init__(self):
        super().__init__("WMG admin")

        self.geometry("500x700")

        # Setup list-boxes
        self.course_list = None
        self.user_list = None
        self.enrollment_list = []

        self.database = None
        self.connection_status = tk.StringVar()
        self.password = tk.StringVar()

        self.enrollment_window = None

        self.withdraw()
        self.login_window = None
        self.login()

        self.admin_dashboard()

        self.mainloop()

    def login(self):
        self.login_window = tk.Toplevel(self)
        self.login_window.title("WMG Login")
        self.login_window.geometry("1000x400")

        logo_canvas = tk.Canvas(self.login_window, width=900, height=300)
        self.logo_img = tk.PhotoImage(file=f"{pathlib.Path().resolve()}/Images/WMG.png")
        logo_canvas.create_image(20, 20, anchor="nw", image=self.logo_img)
        logo_canvas.pack()

        password_label = tk.Label(self.login_window, text="Password", font=20).pack()

        password_entry = tk.Entry(self.login_window, textvariable=self.password, show='*').pack()

        login_button = tk.Button(self.login_window, text="Login", font=20, command=self.connect).pack()

        status_label = tk.Message(self.login_window, textvariable=self.connection_status, width=400).pack()

    def connect(self):
        print("here", self.password.get())
        try:
            self.database = DB_API("WMGTSS_QA", "wmg_admin", self.password.get())

            create_user.set_database(self.database)
            create_course.set_database(self.database)
            enroll_user.set_database(self.database)

            self.deiconify()
            self.login_window.destroy()
        except DatabaseError as e:
            self.connection_status.set(e)
            print(e)

    def admin_dashboard(self):
        add_options = tk.Frame(self).pack(side=tk.TOP)
        add_student = tk.Button(add_options, text="Add Students", command=lambda: CreateUserForm(self, "student")).pack(fill=tk.X)
        add_teacher = tk.Button(add_options, text="Add Teacher", command=lambda: CreateUserForm(self, "teacher")).pack(fill=tk.X)
        add_moderator = tk.Button(add_options, text="Add Moderator", command=lambda: CreateUserForm(self, "moderator")).pack(fill=tk.X)
        add_course = tk.Button(add_options, text="Add Course", command=lambda: CreateCourseForm(self)).pack(fill=tk.X)

        self.course_list = tk.Listbox(self)
        self.course_list.bind('<Double-1>', lambda x: self.open_course(self.course_list.get(tk.ACTIVE), x))
        self.course_list.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=40, pady=20)

        refresh_button = tk.Button(self, text="Refresh", command=self.refresh_database).pack(fill=tk.X)

    def open_course(self, course, debug):

        self.enrollment_window = tk.Toplevel(self)
        self.enrollment_window.title("Enrollments")
        self.enrollment_window.geometry("500x500")

        relevant_enrollments = [enrollment for enrollment in self.enrollment_list if int(course) == enrollment[0]]

    def refresh_database(self):
        courses = self.database.query("SELECT * FROM courses")
        users = self.database.query("SELECT * FROM users")
        enrollments = self.database.query("SELECT * FROM enrollments")


if __name__ == "__main__":
    test = AdminTool()
