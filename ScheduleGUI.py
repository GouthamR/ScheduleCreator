from tkinter import *

class ScheduleGUI:
    def switchSchedule(self):
        self.scheduleIndex += 1
        print("switch to " + str(self.scheduleIndex))
    def initGUI(self):
        root = Tk()
        root.protocol('WM_DELETE_WINDOW', root.destroy)
        root.title("Schedule Creator - Schedule Viewer. By Goutham Rajeev")
        # create frame
        frame = Frame(root, bg="grey", width=400, height=40)
        frame.pack(fill='x')
        button1 = Button(frame, text="Switch", command=self.switchSchedule)
        button1.pack(side="right", padx=10)
        # set canvas properties
        width = 400
        height = 400
        # invoke canvas
        c = Canvas(root, width=width, height=height)
        c.pack()
        c.create_text(10, 20, anchor=SW, text="Schedule")
        c.create_rectangle(50, 25, 150, 75, fill="blue")
    def __init__(self, schedules):
        self.schedules = schedules
        self.scheduleIndex = 0
        self.initGUI()
        mainloop()

if __name__ == "__main__":
    ScheduleGUI(None)
