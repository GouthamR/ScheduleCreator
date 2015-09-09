from tkinter import *

class ScheduleGUI:
    def __init__(self, schedules):
        root = Tk()
        root.title("Schedule Creator - Schedule Viewer. By Goutham Rajeev")
        self.schedules = schedules
        # create frame to put control buttons onto
        frame = Frame(root, bg="grey", width=400, height=40)
        frame.pack(fill='x')
        button1 = Button(frame, text="Switch")
        button1.pack(side="right", padx=10)
        # set canvas properties
        width = 400
        height = 400
        # invoke canvas
        c = Canvas(root, width=width, height=height)
        c.pack()
        c.create_text(10, 20, anchor=SW, text="Schedule")
        c.create_rectangle(50, 25, 150, 75, fill="blue")
