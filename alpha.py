import tkinter as tk # Python 3
import math
import get_time as gt
import re
import threading
root = tk.Tk()


def createWidgets(self):
    CANVAS_WIDTH = 200
    CANVAS_HEIGHT = 200
    self.canvas = tk.Canvas(self, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, highlightthickness=0,bg='green')
    self.canvas.pack()
    circle(self.canvas, CANVAS_WIDTH / 2, CANVAS_WIDTH / 2, CANVAS_WIDTH / 2 - 10, 'SlateGray')
    circle(self.canvas, CANVAS_WIDTH / 2, CANVAS_WIDTH / 2, CANVAS_WIDTH / 2 - 16, 'DarkSlateGray')
    circle(self.canvas, CANVAS_WIDTH / 2, CANVAS_WIDTH / 2, CANVAS_WIDTH / 2 - 18, 'white')
    time = gt.get_time()
    self.h = int(re.match('\d+-\d+-\d+ (\d+):\d+:\d+.*', time['datetime']).group(1))
    self.m = int(re.match('\d+-\d+-\d+ \d+:(\d+):\d+.*', time['datetime']).group(1))
    self.s = int(re.match('\d+-\d+-\d+ \d+:\d+:(\d+).*', time['datetime']).group(1))
    timer_h = threading.Timer(1, paint_h)
    timer_h.start()
    self.canvas.bind(sequence="<B1-Motion>", func=processMouseEvent)
    self.canvas.bind(sequence="<Button-1>", func=getMouseLocation)
    self.canvas.bind(sequence="<ButtonRelease-1>", func=resetMouseLocation)
    self.canvas.bind(sequence="<Double-Button-1>", func=closeClock)
    for deg in range(0, 360, 5):
        r = CANVAS_WIDTH / 2 - 18
        x = CANVAS_WIDTH / 2 + r * math.cos(deg / 180 * math.pi)
        y = CANVAS_WIDTH / 2 - r * math.sin(deg / 180 * math.pi)
        if deg % 30 == 0:
            end_x = CANVAS_WIDTH / 2 + (r - 10) * math.cos(deg / 180 * math.pi)
            end_y = CANVAS_WIDTH / 2 - (r - 10) * math.sin(deg / 180 * math.pi)
            self.canvas.create_line(x, y, end_x, end_y, fill='black', width=1.5)
            if int(((360 - deg) / 30 + 3) % 12) == 0:
                text = 12
            else:
                text = int(((360 - deg) / 30 + 3) % 12)
            end_text_x = CANVAS_WIDTH / 2 + (r - 14) * math.cos(deg / 180 * math.pi)
            end_text_y = CANVAS_WIDTH / 2 - (r - 14) * math.sin(deg / 180 * math.pi)
            self.canvas.create_text(end_text_x, end_text_y, text=text)
        else:
            end_x = CANVAS_WIDTH / 2 + (r - 5) * math.cos(deg / 180 * math.pi)
            end_y = CANVAS_WIDTH / 2 - (r - 5) * math.sin(deg / 180 * math.pi)
            self.canvas.create_line(x, y, end_x, end_y, fill='grey', width=1)


def circle(canvas, x, y, r, color):
    id = canvas.create_oval(x - r, y - r, x + r, y + r, fill=color, width=0)
    return id


def processMouseEvent(me):
    root.geometry("+%d+%d" %(me.x_root-root.x, me.y_root-root.y))


def getMouseLocation(me):
    root.x = me.x
    root.y = me.y


def resetMouseLocation(me):
    root.x=0
    root.y=0


def closeClock(me):
    root.destroy()


def paint_h():
    CANVAS_WIDTH = 200
    r = CANVAS_WIDTH / 2 - 18
    root.canvas.delete('h')
    root.canvas.delete('m')
    root.canvas.delete('s')
    h_deg = (90 - (root.h + root.m / 60 + root.s / 3600) % 12 * 30) / 180 * math.pi
    end_x_h = CANVAS_WIDTH / 2 + (r - 40) * math.cos(h_deg)
    end_y_h = CANVAS_WIDTH / 2 - (r - 40) * math.sin(h_deg)
    root.canvas.create_line(CANVAS_WIDTH / 2, CANVAS_WIDTH / 2, end_x_h, end_y_h, width=3.2, tag='h')
    m_deg = (90 - (root.m + root.s / 60) * 6) / 180 * math.pi
    end_x_m = CANVAS_WIDTH / 2 + (r - 30) * math.cos(m_deg)
    end_y_m = CANVAS_WIDTH / 2 - (r - 30) * math.sin(m_deg)
    root.canvas.create_line(CANVAS_WIDTH / 2, CANVAS_WIDTH / 2, end_x_m, end_y_m, width=1, tag='m')
    s_deg = (90 - root.s * 6) / 180 * math.pi
    end_x_s = CANVAS_WIDTH / 2 + (r - 20) * math.cos(s_deg)
    end_y_s = CANVAS_WIDTH / 2 - (r - 20) * math.sin(s_deg)
    root.canvas.create_line(CANVAS_WIDTH / 2, CANVAS_WIDTH / 2, end_x_s, end_y_s, width=1, fill='red', tag='s')
    if root.s + 1 < 60:
        root.s = root.s + 1
    else:
        if root.m + 1 < 60:
            root.m = root.m + 1
            root.s = 0
        else:
            if root.h + 1 < 24:
                root.h = root.h + 1
                root.m = 0
                root.s = 0
            else:
                root.h = 0
                root.m = 0
                root.s = 0
    global timer
    timer = threading.Timer(1, paint_h)
    timer.start()


root.overrideredirect(True)
root.geometry("-50+50")
root.lift()
root.wm_attributes("-topmost", True)
root.wm_attributes("-disabled",False)
root.wm_attributes("-transparentcolor", "green")
createWidgets(root)
root.mainloop()