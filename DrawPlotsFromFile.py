import os
import matplotlib
import pandas as pd
import tkinter as tk

from datetime import datetime
from matplotlib import style
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import filedialog

matplotlib.use("TkAgg")
style.use("ggplot")

import GlobalConfig
import CommonFunctions


class DrawPlotsFromFile(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.df = None
        self.date = datetime.today().strftime('%Y-%m-%d_%H-%M')

        self.saveFrame = dict()
        self.fileNameLabel = dict()
        self.fileNameTextField = dict()
        self.savePlotButton = dict()

        self.draw_save_box('command', 0, 1)
        self.draw_save_box('position', 0, 2)
        self.draw_save_box('speed', 0, 3)

    def draw_upper_frame(self):
        pass

    def draw_save_box(self, plot_type, row, column):
        # UPPER FRAME
        self.saveFrame[plot_type] = tk.LabelFrame(self, pady=10)
        self.saveFrame[plot_type].grid(row=row, column=column)

        # FILE NAME LABEL
        self.fileNameLabel[plot_type] = tk.Label(self.saveFrame[plot_type], text="Enter file name : ")
        self.fileNameLabel[plot_type].grid(row=0, column=0)

        # FILE NAME TEXT FIELD
        self.fileNameTextField[plot_type] = tk.Entry(self.saveFrame[plot_type], borderwidth=3, width=40)
        self.fileNameTextField[plot_type].grid(row=0, column=1)
        self.fileNameTextField[plot_type].insert(0, self.date + '_' + plot_type.capitalize())

        # SAVE PLOT BUTTON
        self.savePlotButton[plot_type] = tk.Button(self.saveFrame[plot_type], text='SAVE PLOT', padx=10,
                                                   command=lambda: self.save_plot(plot_type))
        self.savePlotButton[plot_type].grid(row=0, column=2)
