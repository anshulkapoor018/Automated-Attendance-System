from Tkinter import *
import os
import attendance_Generator

def quit():
    w.destroy()

def open():
    os.startfile("b.csv")

def attendance():
    attendance_Generator.convert()

bgclr = "#282828"
fgclr = "#cecece"
clr = '#004a95'


w = Tk()
w.title("Attendance Manager")
w.geometry("480x400")
w.config(bg=bgclr)
w.resizable()


b2 = Button(w,
                text="Generate Attendace",
                bg=clr,
                fg="white",
                relief=GROOVE,
                highlightcolor=clr,
                highlightthickness=4,
                width=40,
                height=3,
                font=10,
                command=attendance)

b2.place(x=50, y=80)

b3 = Button(w,
                text="View Attendance Sheet",
                bg=clr,
                fg="white",
                relief=GROOVE,
                highlightcolor=clr,
                highlightthickness=4,
                width=40,
                height=3,
                font=10,
                command = open)

b3.place(x=50, y=180)

b4 = Button(w,
                text="Exit",
                bg=clr,
                fg="white",
                relief=GROOVE,
                highlightcolor=clr,
                highlightthickness=4,
                width=10,
                height=2,
                font=10,
                command=quit)

b4.place(x=180, y=280)

w.mainloop()