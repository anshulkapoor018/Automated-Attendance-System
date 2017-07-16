from Tkinter import *
import Final

def adding():
    Final.add_person("face_recognition_system/people/", "rectangle", person1.get())

bgclr = "#282828"
fgclr = "#cecece"
clr = '#004a95'

w = Tk()
w.title("Add a Student")
w.geometry("1366x750")
w.config(bg=bgclr)
w.resizable()

user1 = Label(w,
             text="Enter Student's Enrollment Number : ",
             font=("blod", 15),
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
                text="ADD",
                bg=clr,
                fg="white",
                relief=GROOVE,
                highlightcolor=clr,
                highlightthickness=4,
                width=40,
                font=10,
                command=adding)
button1.place(x=30, y=640)
w.mainloop()