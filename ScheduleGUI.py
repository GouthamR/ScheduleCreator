from tkinter import *
from Schedule import *
from Course import *

class ScheduleGUI:
    def switchSchedule(self):
        self.scheduleIndex += 1
        print("switch to " + str(self.scheduleIndex))
        drawSchedule()
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
        self.canvas = Canvas(root, width=width, height=height)
        self.canvas.pack()
    def drawSchedule(self):
        self.canvas.create_text(10, 20, anchor=SW, text="Schedule")
        self.canvas.create_rectangle(50, 25, 150, 75, fill="blue")
        for i in range(len(self.schedules[self.scheduleIndex].classes)):
            currClass = self.schedules[self.scheduleIndex].classes[i]
            self.canvas.create_text(i*10, i*20, anchor=SW, text=currClass.code)
    def __init__(self, schedules):
        self.schedules = schedules
        self.scheduleIndex = 0
        self.initGUI()
        self.drawSchedule()
        mainloop()

if __name__ == "__main__":
    ScheduleGUI(None)
