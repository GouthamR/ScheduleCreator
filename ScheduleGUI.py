from tkinter import *
from Schedule import *
from Course import *

class ScheduleGUI:
    CANVAS_WIDTH = 400
    CANVAS_HEIGHT = 400
    NUMBER_OF_DAYS = 5
    MINUTES_IN_DAY = 1440
    BLOCK_WIDTH = CANVAS_WIDTH/NUMBER_OF_DAYS
    BLOCK_COLORS = ("white", "red", "green", "blue", "cyan", "yellow", "magenta")
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
        # invoke canvas
        self.canvas = Canvas(root, width=ScheduleGUI.CANVAS_WIDTH, height=ScheduleGUI.CANVAS_HEIGHT)
        self.canvas.pack()
    def getCanvasY(minutes):
        return minutes / ScheduleGUI.MINUTES_IN_DAY * ScheduleGUI.CANVAS_HEIGHT
    def drawSchedule(self):
        self.canvas.delete("all")
        classes = self.schedules[self.scheduleIndex].classes
        for i in range(len(classes)):
            currClass = classes[i]
            currColor = ScheduleGUI.BLOCK_COLORS[i]
            for day in currClass.days.days:
                startMin = currClass.classTime.start.getTotalMinutes()
                endMin = currClass.classTime.end.getTotalMinutes()
                x = day * ScheduleGUI.BLOCK_WIDTH
                y = ScheduleGUI.getCanvasY(startMin)
                w = ScheduleGUI.BLOCK_WIDTH
                h = ScheduleGUI.getCanvasY(endMin - startMin)
                self.canvas.create_rectangle(x, y, x + w, y + h, fill=currColor)
    def __init__(self, schedules):
        self.schedules = schedules
        self.scheduleIndex = 0
        self.initGUI()
        self.drawSchedule()
        mainloop()

if __name__ == "__main__":
    ScheduleGUI(None)
