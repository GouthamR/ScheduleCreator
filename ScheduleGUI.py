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
    BLOCK_COLORS = ("white", "orange red", "pale green", "dodger blue", "turquoise", "goldenrod", "violet", "steelblue1")
    def _switchSchedule(self, forward):
        if forward:
            self.scheduleIndex += 1
            if self.scheduleIndex == len(self.schedules):
                self.scheduleIndex = 0
        else:
            self.scheduleIndex -= 1
            if self.scheduleIndex == -1:
                self.scheduleIndex = len(self.schedules) - 1
        self._drawSchedule()
    def _initGUI(self):
        root = Tk()
        root.protocol('WM_DELETE_WINDOW', root.destroy)
        root.title("Schedule Creator - Schedule Viewer. By Goutham Rajeev")
        # create frame
        frame = Frame(root, bg="grey", width=400, height=40)
        frame.pack(fill='x')
        #create buttons
        def switchForward():
            self._switchSchedule(True)
        def switchBackward():
            self._switchSchedule(False)
        forwardButton = Button(frame, text="Next", command=switchForward)
        forwardButton.pack(side="right", padx=10)
        backButton = Button(frame, text="Previous", command=switchBackward)
        backButton.pack(side="right", padx=10)
        #create index label
        self.indexLabel = Text(frame, height=1, padx=10, width=6)
        self.indexLabel.configure(inactiveselectbackground=self.indexLabel.cget("selectbackground"))
        self.indexLabel.pack(side="left")
        #create code label
        self.codeLabel = Text(frame, height=1, padx=10, borderwidth=0)
        self.codeLabel.configure(inactiveselectbackground=self.codeLabel.cget("selectbackground"))
        self.codeLabel.pack(side="left")
        # invoke canvas
        self.canvas = Canvas(root, width=ScheduleGUI.CANVAS_WIDTH, height=ScheduleGUI.CANVAS_HEIGHT)
        self.canvas.pack()
    def _getCanvasY(minutes, minMinutes, maxMinutes):
        return (minutes - minMinutes) / (maxMinutes - minMinutes) * ScheduleGUI.CANVAS_HEIGHT
    def _drawSchedule(self):
        self.canvas.delete("all")

        classes = self.schedules[self.scheduleIndex].classes
        minHour = min(classes, key=lambda currClass : currClass.classTime.start).classTime.start.hour
        minMinutes = minHour * 60
        maxHour = max(classes, key=lambda currClass : currClass.classTime.start).classTime.end.hour + 1
        maxMinutes = maxHour * 60
        for i in range(len(classes)):
            currClass = classes[i]
            currColor = ScheduleGUI.BLOCK_COLORS[i % len(ScheduleGUI.BLOCK_COLORS)]
            for day in currClass.days.days:
                startMin = currClass.classTime.start.getTotalMinutes()
                endMin = currClass.classTime.end.getTotalMinutes()
                x = day * ScheduleGUI.BLOCK_WIDTH + ScheduleGUI.TIME_LABEL_WIDTH
                yStart = ScheduleGUI._getCanvasY(startMin, minMinutes, maxMinutes)
                w = ScheduleGUI.BLOCK_WIDTH
                yEnd = ScheduleGUI._getCanvasY(endMin, minMinutes, maxMinutes)
                self.canvas.create_rectangle(x, yStart, x + w, yEnd, fill=currColor)
                self.canvas.create_text(x, yStart, anchor="nw",text="%s: %s\n%s - %s" % (currClass.getFullName(), currClass.code, currClass.classTime.start.getFormatted(), currClass.classTime.end.getFormatted()))

        HOUR_LABEL_HEIGHT = ScheduleGUI._getCanvasY(minHour + 1, minHour, maxHour)
        for i in range(minHour, maxHour + 1):
            self.canvas.create_text(0, (i - minHour) * HOUR_LABEL_HEIGHT, anchor="nw", text=str(i))

        self.codeLabel.config(state='normal')
        self.codeLabel.delete(1.0, 'end')
        self.codeLabel.insert('end', ",".join(str(i) for i in self.schedules[self.scheduleIndex].getClassCodes()))
        self.codeLabel.config(state='disabled')

        self.indexLabel.config(state='normal')
        self.indexLabel.delete(1.0, 'end')
        self.indexLabel.insert('end', self.scheduleIndex)
        self.indexLabel.config(state='disabled')
    def __init__(self, schedules):
        self.schedules = schedules
        self.scheduleIndex = 0
        self._initGUI()
        self._drawSchedule()
        mainloop()
