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

class CreateUserForm(tk.Frame):

    def __init__(self, root, role, **kw):
        super().__init__(**kw)

        self.role = role
        self.user_data = []

        username = tk.StringVar()
        self.username_label = tk.Label(root, text="{role} username").pack()
        self.username_entry = tk.Entry(root, textvariable=username).pack()
        self.user_data.append(username)

        firstname = tk.StringVar()
        self.firstname_label = tk.Label(root, text="{role} firstname").pack()
        self.firstname_entry = tk.Entry(root, textvariable=firstname).pack()
        self.user_data.append(firstname)

        lastname = tk.StringVar()
        self.lastname_label = tk.Label(root, text="{role} lastname").pack()
        self.lastname_entry = tk.Entry(root, textvariable=lastname).pack()
        self.user_data.append(lastname)


        day = tk.StringVar()
        month = tk.StringVar()
        year = tk.StringVar()
        self.dateofbirth_label = tk.Label(root, text="{role} date of birth (dd/mm/yyyy)").pack()
        self.day_entry = tk.Entry(root, textvariable=day).pack(fill=tk.X)
        self.month_entry = tk.Entry(root, textvariable=month).pack(fill=tk.X)
        self.year_entry = tk.Entry(root, textvariable=year).pack(fill=tk.X)

        self.dob = ({
            "day": day,
            "month": month,
            "year": year
        })

        self.create_button = tk.Button(root, text="Create", command=self.insert_data)

    def insert_data(self):

        dateofbirth = datetime.date(
            int(self.dob["year"].get()),
            int(self.dob["month"].get()),
            int(self.dob["day"].get())
        )

        create_user.create_new_user(self.role, *self.user_data, dateofbirth)

        self.clear_data()

    def clear_data(self):

        self.role = ""


class CreateCourseForm(tk.Frame):

    def __init__(self, root, **kw):
        super().__init__(**kw)

        self.name = tk.StringVar()
        self.name_label = tk.Label(root, text="username").pack()
        self.name_entry = tk.Entry(root, textvariable=self.name).pack()

        start_day = tk.StringVar()
        start_month = tk.StringVar()
        start_year = tk.StringVar()
        self.start_date_label = tk.Label(root, text="start date (dd/mm/yyyy)").pack()
        self.start_day_entry = tk.Entry(root, textvariable=start_day).pack(fill=tk.X)
        self.start_month_entry = tk.Entry(root, textvariable=start_month).pack(fill=tk.X)
        self.start_year_entry = tk.Entry(root, textvariable=start_year).pack(fill=tk.X)

        self.start_date = ({
            "day": start_day,
            "month": start_month,
            "year": start_year
        })

        end_day = tk.StringVar()
        end_month = tk.StringVar()
        end_year = tk.StringVar()
        self.end_date_label = tk.Label(root, text="end date (dd/mm/yyyy)").pack()
        self.end_day_entry = tk.Entry(root, textvariable=end_day).pack(fill=tk.X)
        self.end_month_entry = tk.Entry(root, textvariable=end_month).pack(fill=tk.X)
        self.end_year_entry = tk.Entry(root, textvariable=end_year).pack(fill=tk.X)

        self.end_date = ({
            "day": end_day,
            "month": end_month,
            "year": end_year
        })

        self.create_button = tk.Button(root, text="Create", command=self.insert_data)

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

        create_course.create_new_course(self.name, start_date, end_date)

        self.destroy()


class AdminTool(tk.Tk):

    def __init__(self):
        super().__init__("WMG admin")

        self.database = None
        self.connection_status = tk.StringVar()
        self.password = tk.StringVar()

        self.withdraw()
        self.login_window = None
        self.login()

        self.admin_dashboard()

        self.mainloop()

    def login(self):
        self.login_window = tk.Toplevel(self)
        self.login_window.title("WMG Login")
        self.login_window.geometry("500x150")

        logo_canvas = tk.Canvas(self, width=300, height=300)
        logo_img = tk.PhotoImage(file=f"{pathlib.Path().resolve()}/Images/WMG.png")
        logo_canvas.create_image(20, 20, anchor="nw", image=logo_img)
        logo_canvas.pack()

        password_label = tk.Label(self.login_window, text="Password * ").pack()

        password_entry = tk.Entry(self.login_window, textvariable=self.password, show='*').pack()

        login_button = tk.Button(self.login_window, text="Login", command=self.connect).pack()

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



if __name__ == "__main__":
    test = AdminTool()
