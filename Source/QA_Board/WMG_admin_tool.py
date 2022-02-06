import tkinter as tk
from postrgesql_api import DB_API
import create_user as user
import create_course as course
import enroll_user as enroll

database = DB_API("WMGTSS_QA", , "default")

def login(root):
    login_window = tk.Toplevel(root)
    login_window.title("WMG Login")
    login_window.geometry("300x250")

    password = tk.StringVar()

    logo_canvas = tk.Canvas(root, width = 300, height = 300).pack()
    logo_img = tk.PhotoImage(file="/Images/WMG.png")
    logo_canvas.create_image(20,20, anchor="NW", image=logo_img)

    password_label = tk.Label(login_window, text="Password * ").pack()

    password_entry = tk.Entry(login_window, textvariable=password, show='*').pack()

    login_button = tk.Button()


class AdminTool(tk.Tk):

    def __init__(self):
        super().__init__("WMG admin")


