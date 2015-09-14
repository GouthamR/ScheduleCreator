from tkinter import *
from Schedule import *
from Course import *

class ScheduleGUI:
    CANVAS_WIDTH = 600
    CANVAS_HEIGHT = 600
    NUMBER_OF_DAYS = 5
    MINUTES_IN_DAY = 1440
    TIME_LABEL_WIDTH = CANVAS_WIDTH / (NUMBER_OF_DAYS + 1) / 2
    BLOCK_WIDTH = (CANVAS_WIDTH - TIME_LABEL_WIDTH) / NUMBER_OF_DAYS
    BLOCK_COLORS = ("white", "red", "green", "blue", "cyan", "yellow", "magenta")
    def switchSchedule(self, forward):
        if forward:
            self.scheduleIndex += 1
            if self.scheduleIndex == len(self.schedules):
                self.scheduleIndex = 0
        else:
            self.scheduleIndex -= 1
            if self.scheduleIndex == -1:
                self.scheduleIndex = len(self.schedules) - 1
        print("switch to " + str(self.scheduleIndex))
        self.drawSchedule()
    def initGUI(self):
        root = Tk()
        root.protocol('WM_DELETE_WINDOW', root.destroy)
        root.title("Schedule Creator - Schedule Viewer. By Goutham Rajeev")
        # create frame
        frame = Frame(root, bg="grey", width=400, height=40)
        frame.pack(fill='x')
        #create button
        def switchForward():
            self.switchSchedule(True)
        def switchBackward():
            self.switchSchedule(False)
        forwardButton = Button(frame, text="Next", command=switchForward)
        forwardButton.pack(side="right", padx=10)
        #create label
        self.codeLabel = Text(frame, height=1, borderwidth=0)
        self.codeLabel.configure(inactiveselectbackground=self.codeLabel.cget("selectbackground"))
        self.codeLabel.pack(side="left")
        # invoke canvas
        self.canvas = Canvas(root, width=ScheduleGUI.CANVAS_WIDTH, height=ScheduleGUI.CANVAS_HEIGHT)
        self.canvas.pack()
    def getCanvasY(minutes, minMinutes, maxMinutes):
        return (minutes - minMinutes) / (maxMinutes - minMinutes) * ScheduleGUI.CANVAS_HEIGHT
    def drawSchedule(self):
        self.canvas.delete("all")

        classes = self.schedules[self.scheduleIndex].classes
        minHour = min(classes, key=lambda currClass : currClass.classTime.start).classTime.start.hour
        minMinutes = minHour * 60
        maxHour = max(classes, key=lambda currClass : currClass.classTime.start).classTime.end.hour + 1
        maxMinutes = maxHour * 60
        for i in range(len(classes)):
            currClass = classes[i]
            currColor = ScheduleGUI.BLOCK_COLORS[i]
            for day in currClass.days.days:
                startMin = currClass.classTime.start.getTotalMinutes()
                endMin = currClass.classTime.end.getTotalMinutes()
                x = day * ScheduleGUI.BLOCK_WIDTH + ScheduleGUI.TIME_LABEL_WIDTH
                yStart = ScheduleGUI.getCanvasY(startMin, minMinutes, maxMinutes)
                w = ScheduleGUI.BLOCK_WIDTH
                yEnd = ScheduleGUI.getCanvasY(endMin, minMinutes, maxMinutes)
                self.canvas.create_rectangle(x, yStart, x + w, yEnd, fill=currColor)
                self.canvas.create_text(x, yStart, anchor="nw",text="%s: %s" % (currClass.name, currClass.code))

        HOUR_LABEL_HEIGHT = ScheduleGUI.getCanvasY(minHour + 1, minHour, maxHour)
        for i in range(minHour, maxHour + 1):
            self.canvas.create_text(0, (i - minHour) * HOUR_LABEL_HEIGHT, anchor="nw", text=str(i))

        self.codeLabel.config(state='normal')
        self.codeLabel.delete(1.0, 'end')
        self.codeLabel.insert('end', ",".join(str(i) for i in self.schedules[self.scheduleIndex].getClassCodes()))
        self.codeLabel.config(state='disabled')
    def __init__(self, schedules):
        self.schedules = schedules
        self.scheduleIndex = 0
        self.initGUI()
        self.drawSchedule()
        mainloop()
