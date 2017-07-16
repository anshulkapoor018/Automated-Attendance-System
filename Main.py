from Tkinter import *
import Final
import facerec
import os
from PIL import ImageTk, Image
import cv2
import attendance_Generator

bgclr = "#282828"
fgclr = "#cecece"
clr = '#004a95'

users = [("admin", "0000"),
         ("admin2", "0000"),
         ("admin3", "0000")]

w = Tk()
w.title("JIIT Attendance System")
w.geometry("1366x750")
w.config(bg=bgclr)
w.resizable()

w.bind('<Escape>', lambda e: w.quit())
lmain = Label(w)
lmain.pack()

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
width, height = 600,400
cap = cv2.VideoCapture(0)

def open():
    os.startfile("b.csv")

def attendanceG():
    attendance_Generator.convert()

def login():
    if (user_Entry.get(), password_Entry.get()) in users:
        tkMessageBox.showwarning("Status", "Log In Successful")
    else:
        warn.config(text="Invalid username or Password", fg="red")

def show_frame():
    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    font = cv2.FONT_HERSHEY_SIMPLEX
    thickness = 1
    white = (255,) * 3
    size = 1
    #left = (x, y + h + 12)

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, 'Some Person', (x-10, y-10), font, size, white, thickness)

    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(10, show_frame)

def open():
    os.startfile("b.csv")

def quit():
    w.destroy()

def adding():
    Final.add_person("face_recognition_system/people/", "rectangle", person1.get())

def attendance():
    Final.recognize_people("face_recognition_system/people/", "rectangle")

canvas = Canvas(w, width=1366, height=768)
canvas.pack()

mainImage = Image.open("attendance.jpg")
mainImage = mainImage.resize((1366,750), Image.ANTIALIAS)
mainImage = ImageTk.PhotoImage(mainImage)
canvas.create_image(681, 350, image=mainImage)

#Take Attendance Module
b1 = Button(w,
                text="Take Attendance",
                bg=clr,
                fg="white",
                relief=GROOVE,
                highlightcolor=clr,
                highlightthickness=4,
                width=30,
                height=3,
                font=10,
                command=attendance)
b1.place(x=1020, y=80)

#Add Students to Database
user1 = Label(w,
             text="Enter Student's Enrollment Number : ",
             font=("bold", 15),
             bg=bgclr,
             fg=fgclr)
user1.place(x=30, y=540)

person1 = StringVar()

user1_Entry = Entry(w, bg=bgclr,
                   fg="white",
                   relief=GROOVE,
                   highlightcolor="white",
                   highlightthickness=2,
                   highlightbackground=clr,
                   width=40,
                   textvariable = person1,
                   font=10,
                   bd=5)
user1_Entry.place(x=30, y=580)

button1 = Button(w,
                text="ADD Student Data",
                bg=clr,
                fg="white",
                relief=GROOVE,
                highlightcolor=clr,
                highlightthickness=4,
                width=40,
                font=10,
                command=adding)
button1.place(x=30, y=640)

#Check Camera Module Button
b5 = Button(w,
                text="Check Camera",
                bg=clr,
                fg="white",
                relief=GROOVE,
                highlightcolor=clr,
                highlightthickness=4,
                width=30,
                height=3,
                font=10,
                command=show_frame)
b5.place(x=1020, y=230)

#Log Out Button
b4 = Button(w,
                text="Log Out",
                bg=clr,
                fg="white",
                relief=GROOVE,
                highlightcolor=clr,
                highlightthickness=4,
                width=30,
                height=1,
                font=10,
                command=quit)

b4.place(x=1020, y=640)

#User Details LOGIN
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
                command=login)
button.place(x=30, y=240)

#Attendance Generator buttons

b2 = Button(w,
                text="Generate Attendace",
                bg=clr,
                fg="white",
                relief=GROOVE,
                highlightcolor=clr,
                highlightthickness=4,
                width=30,
                height=3,
                font=10,
                command=attendanceG())

b2.place(x=1020, y=380)

b3 = Button(w,
                text="View Attendance Sheet",
                bg=clr,
                fg="white",
                relief=GROOVE,
                highlightcolor=clr,
                highlightthickness=4,
                width=30,
                height=3,
                font=10,
                command = open)

b3.place(x=1020, y=520)

w.mainloop()
