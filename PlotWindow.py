import matplotlib
import tkinter as tk

import CommonFunctions

from matplotlib import style
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import filedialog
from datetime import datetime


matplotlib.use("TkAgg")
style.use("ggplot")


class PlotWindow:

    def __init__(self, root, df):
        self.root = root
        self.root.title("PLOTS")

        self.df = df
        self.date = datetime.today().strftime('%Y-%m-%d_%H-%M')

        self.upperFrame = dict()
        self.fileNameLabel = dict()
        self.fileNameTextField = dict()
        self.savePlotButton = dict()

        self.draw_save_box('command', 0, 1)
        self.draw_save_box('position', 0, 2)
        self.draw_save_box('speed', 0, 3)

        self.draw_plot('command', 1, 1)
        self.draw_plot('position', 1, 2)
        self.draw_plot('speed', 1, 3)

    def draw_save_box(self, plot_type, row, column):
        # UPPER FRAME
        self.upperFrame[plot_type] = tk.LabelFrame(self.root, pady=10)
        self.upperFrame[plot_type].grid(row=row, column=column)

        # FILE NAME LABEL
        self.fileNameLabel[plot_type] = tk.Label(self.upperFrame[plot_type], text="Enter file name : ")
        self.fileNameLabel[plot_type].grid(row=0, column=0)

        # FILE NAME TEXT FIELD
        self.fileNameTextField[plot_type] = tk.Entry(self.upperFrame[plot_type], borderwidth=3, width=40)
        self.fileNameTextField[plot_type].grid(row=0, column=1)
        self.fileNameTextField[plot_type].insert(0, self.date + '_' + plot_type.capitalize())

        # SAVE PLOT BUTTON
        self.savePlotButton[plot_type] = tk.Button(self.upperFrame[plot_type], text='SAVE PLOT', padx=10,
                                                   command=lambda: self.save_plot(plot_type))
        self.savePlotButton[plot_type].grid(row=0, column=2)

    def draw_plot(self, plot_type, row, column):
        x = self.df['elapsed_time(ms)']
        y = self.df[plot_type]

        f = Figure(figsize=(5, 5))
        ax = f.add_subplot(111)
        ax.plot(x, y, marker='x', color='blue')
        ax.grid(True)

        ax.set_title(plot_type.upper() + " vs TIME", fontsize=16)
        ax.set_ylabel(plot_type, fontsize=14)
        ax.set_xlabel("elapsed_time(ms)", fontsize=14)

        canvas = FigureCanvasTkAgg(f, master=self.root)
        canvas.get_tk_widget().grid(row=row, column=column)
        canvas.draw()

        return canvas

    def save_plot(self, plot_type):
        filename = self.fileNameTextField[plot_type].get()
        CommonFunctions.save_plot(filename, self.df, plot_type)
