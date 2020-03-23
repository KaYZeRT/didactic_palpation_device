import pandas as pd
import tkinter as tk
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation

import pandas as pd

from matplotlib import style
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import filedialog

LARGE_FONT = ("Verdana", 12)
style.use("ggplot")

pd.set_option('display.expand_frame_repr', False)
matplotlib.use("TkAgg")

f = Figure(figsize=(5,5))
a = f.add_subplot(111)
# ani = animation.FuncAnimation(f, animate, interval=1000)


def animate(interval):
    pullData = open("src/live_plot_test.txt", "r").read()
    dataList = pullData.split('\n')
    xList = []
    yList = []
    for eachLine in dataList:
        if len(eachLine)>1:
            x,y = eachLine.split(',')
            xList.append(int(x))
            yList.append(int(y))
    a.clear()
    a.plot(xList, yList)



class RealTimePlotWindow(tk.Tk):

    def __init__(self, root):
        self.root = root

        self.savePlotButton = tk.Button(self.root, text='SAVE PLOT', padx=10)
        self.savePlotButton.pack()

        self.plot()

        # ani = animation.FuncAnimation(f, animate, interval=1000)


    def plot(self):
        pullData = open("src/live_plot_test.txt", "r").read()
        dataList = pullData.split('\n')
        xList = []
        yList = []

        for eachLine in dataList:
            if len(eachLine) > 1:
                x, y = eachLine.split(',')
                xList.append(int(x))
                yList.append(int(y))

        # f = Figure(figsize=(8, 8))
        # a = f.add_subplot(111)
        a.plot(xList, yList, marker='x', color='blue')
        a.grid(True)

        a.set_title(" vs TIME", fontsize=16)
        a.set_ylabel("Y", fontsize=14)
        a.set_xlabel("elapsed_time(µs)", fontsize=14)

        canvas = FigureCanvasTkAgg(f, master=self.root)
        canvas.get_tk_widget().pack()
        canvas.draw()

        return canvas