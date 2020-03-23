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

# f = Figure(figsize=(5,5))
# a = f.add_subplot(111)

import threading
import time
from random import randint

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

def data_points():
    f = open("data.txt", "w")
    for i in range(10):
        f.write(str(randint(0, 10)) + '\n')
    f.close()

    f = open("data.txt", "r")
    data = f.readlines()
    f.close()

    l = []
    for i in range(len(data)):
        l.append(int(data[i].rstrip("\n")))
    return l

class RealTimePlotWindow(tk.Tk):

    def __init__(self, root):
        self.root = root
        self.root.title("Real Time Plot")

        self.continuePlotting = False

        self.savePlotButton = tk.Button(self.root, text='SAVE PLOT', padx=10)
        self.savePlotButton.pack()

        fig = Figure()
        self.ax = fig.add_subplot(111)
        self.ax.set_xlabel("X axis")
        self.ax.set_ylabel("Y axis")
        self.ax.grid(True)

        self.graph = FigureCanvasTkAgg(fig, master=root)
        self.graph.get_tk_widget().pack(side="top", fill='both', expand=True)

        b = tk.Button(root, text="Start/Stop", command=self.gui_handler, bg="red", fg="white")
        b.pack()

    def change_state(self):
        if self.continuePlotting:
            self.continuePlotting = False
        else:
            self.continuePlotting = True

    def plotter(self):
        while self.continuePlotting:
            self.ax.cla()
            self.ax.grid()
            dpts = data_points()
            self.ax.plot(range(10), dpts, marker='o', color='orange')
            # self.graph.draw()
            print(dpts)
            time.sleep(1)

    def gui_handler(self):
        self.change_state()
        threading.Thread(target=self.plotter).start()

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