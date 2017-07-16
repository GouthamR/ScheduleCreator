import tkinter as tk
import schedule

class ScheduleGUI:
    _CANVAS_WIDTH = 600
    _CANVAS_HEIGHT = 600
    _NUMBER_OF_DAYS = 5
    _TIME_LABEL_WIDTH = _CANVAS_WIDTH / (_NUMBER_OF_DAYS + 1) / 2
    _BLOCK_WIDTH = (_CANVAS_WIDTH - _TIME_LABEL_WIDTH) / _NUMBER_OF_DAYS
    _BLOCK_COLORS = ("white", "orange red", "pale green", "dodger blue", "turquoise", "goldenrod", "violet", "steelblue1")
    
    def _switchSchedule(self, forward):
        if not self.isSchedulesInit:
            raise ValueError("ScheduleGUI._switchSchedule: schedules not init")

        if forward:
            self.scheduleIndex += 1
            if self.scheduleIndex == len(self.schedules):
                self.scheduleIndex = 0
        else:
            self.scheduleIndex -= 1
            if self.scheduleIndex == -1:
                self.scheduleIndex = len(self.schedules) - 1
        self._drawSchedule()
    
    def _initEmptyGUI(self, root: tk.Tk):
        # create frame
        frame = tk.Frame(root, bg="grey", width=400, height=40)
        frame.pack(fill='x')
        #create buttons
        def switchForward():
            self._switchSchedule(True)
        def switchBackward():
            self._switchSchedule(False)
        self._forwardButton = tk.Button(frame, text="Next", command=switchForward)
        self._forwardButton.pack(side="right", padx=10)
        self._forwardButton.config(state='disabled')
        self._backButton = tk.Button(frame, text="Previous", command=switchBackward)
        self._backButton.pack(side="right", padx=10)
        self._backButton.config(state='disabled')
        #create index label
        self.indexLabel = tk.Text(frame, height=1, padx=10, width=6)
        self.indexLabel.configure(inactiveselectbackground=self.indexLabel.cget("selectbackground"))
        self.indexLabel.pack(side="left")
        #create code label
        self.codeLabel = tk.Text(frame, height=1, padx=10, borderwidth=0)
        self.codeLabel.configure(inactiveselectbackground=self.codeLabel.cget("selectbackground"))
        self.codeLabel.pack(side="left")
        # invoke canvas
        self.canvas = tk.Canvas(root, width=ScheduleGUI._CANVAS_WIDTH, height=ScheduleGUI._CANVAS_HEIGHT)
        self.canvas.pack()
    
    @staticmethod
    def _getCanvasY(minutes, minMinutes, maxMinutes):
        return (minutes - minMinutes) / (maxMinutes - minMinutes) * ScheduleGUI._CANVAS_HEIGHT
    
    def _drawSchedule(self):
        if not self.isSchedulesInit:
            raise ValueError("ScheduleGUI._drawSchedule: schedules not init")

        self.canvas.delete("all")

        classes = self.schedules[self.scheduleIndex].classes
        minHour = min(classes, key=lambda currClass : currClass.classTime.start).classTime.start.hour
        minMinutes = minHour * 60
        maxHour = max(classes, key=lambda currClass : currClass.classTime.start).classTime.end.hour + 1
        maxMinutes = maxHour * 60
        for i in range(len(classes)):
            currClass = classes[i]
            currColor = ScheduleGUI._BLOCK_COLORS[i % len(ScheduleGUI._BLOCK_COLORS)]
            for day in currClass.days.days:
                startMin = currClass.classTime.start.getTotalMinutes()
                endMin = currClass.classTime.end.getTotalMinutes()
                x = day * ScheduleGUI._BLOCK_WIDTH + ScheduleGUI._TIME_LABEL_WIDTH
                yStart = ScheduleGUI._getCanvasY(startMin, minMinutes, maxMinutes)
                w = ScheduleGUI._BLOCK_WIDTH
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
    
    def initSchedules(self, schedules: [schedule.Schedule]):
        self.isSchedulesInit = True
        self.schedules = schedules
        self.scheduleIndex = 0

        self._forwardButton.config(state='normal')
        self._backButton.config(state='normal')

        self._drawSchedule()
    
    def __init__(self, root: tk.Tk):
        self.isSchedulesInit = False
        self.schedules = []
        self.scheduleIndex = 0
        self._initEmptyGUI(root)
