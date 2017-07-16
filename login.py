from Tkinter import *
import Tkinter
import os
import Main
import subprocess
import tkMessageBox
from PIL import ImageTk, Image

bgclr = "#282828"
fgclr = "#cecece"
clr = '#004a95'

users = [("admin", "0000"),
         ("admin2", "0000"),
         ("admin3", "0000")]

def login():
    if (user_Entry.get(), password_Entry.get()) in users:
        tkMessageBox.showwarning("Status", "Log In Successful")
    else:
        warn.config(text="Invalid username or Password", fg="red")


w = Tk()
w.title("System login")
w.geometry("500x400")
w.config(bg=bgclr)
w.resizable()

user = Label(w,
             text="User",
             font=("bold", 15),
             bg=bgclr,
             fg=fgclr)

user.place(x=30, y=40)

user_Entry = Entry(w, bg=bgclr,
                   fg="white",
                   relief=GROOVE,
                   highlightcolor="white",
                   highlightthickness=2,
                   highlightbackground=clr,
                   width=40,
                   font=10,
                   bd=5)
user_Entry.place(x=30, y=80)

password = Label(w,
                 text="Password",
                 font=("blod", 15),
                 bg=bgclr,
                 fg=fgclr)
password.place(x=30, y=120)

password_Entry = Entry(w, bg=bgclr,
                       fg="white",
                       relief=GROOVE,
                       highlightcolor="white",
                       highlightthickness=2,
                       highlightbackground=clr,
                       width=40,
                       font=10,
                       show="*",
                       bd=5)
password_Entry.place(x=30, y=160)

warn = Label(w,
             font=("bold", 10),
             bg=bgclr)

warn.place(x=30, y=200)

button = Button(w,
                text="Login",
                bg=clr,
                fg="white",
                relief=GROOVE,
                highlightcolor=clr,
                highlightthickness=4,
                width=40,
                font=10,
                command=os.system('python Main.py'))
button.place(x=30, y=240)

w.mainloop()