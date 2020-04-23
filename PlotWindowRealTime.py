import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import tkinter as tk

import CommonFunctions

from matplotlib import style
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import filedialog
from datetime import datetime
import GlobalConfig

pd.set_option('display.expand_frame_repr', False)
matplotlib.use("TkAgg")
style.use("ggplot")


class RealTimePlotWindow(tk.Tk):

    def __init__(self, root, plot_type, new_recording_menu):
        # self.plot_type = plot_type
        # self.parent = new_recording_menu
        #
        # self.root = root
        # self.root.title("Real Time Plot")
        #
        # # UPPER FRAME
        # self.upperFrame = tk.LabelFrame(self.root, pady=10)
        # # self.upperFrame.grid(row=0, column=0)
        # self.upperFrame.pack()
        #
        # # FILE NAME LABEL
        # self.fileNameLabel = tk.Label(self.upperFrame, text="Enter file name : ")
        # self.fileNameLabel.grid(row=0, column=0)
        #
        # # FILE NAME TEXT FIELD
        # self.fileNameTextField = tk.Entry(self.upperFrame, borderwidth=3)
        # self.fileNameTextField.grid(row=0, column=1)
        # self.fileNameTextField.insert(0, self.plot_type + "VsTime")
        #
        # # SAVE PLOT BUTTON
        # self.savePlotButton = tk.Button(self.upperFrame, text='SAVE PLOT', padx=10, state=tk.DISABLED,
        #                                 command=lambda: self.save_plot())
        # self.savePlotButton.grid(row=0, column=2)
        #
        # fig = Figure()
        # self.ax = fig.add_subplot(111)
        # self.ax.set_xlabel("index")
        # self.ax.set_ylabel(self.plot_type)
        # self.ax.grid(True)
        #
        # self.graph = FigureCanvasTkAgg(fig, master=root)
        # self.graph.get_tk_widget().pack(side="top", fill='both', expand=True)
        #
        # self.draw_plot_real_time()

        self.parent = new_recording_menu

        self.root = root
        self.root.title("PLOTS")

        self.date = datetime.today().strftime('%Y-%m-%d_%H-%M')

        self.upperFrame = dict()
        self.fileNameLabel = dict()
        self.fileNameTextField = dict()
        self.savePlotButton = dict()

        self.draw_save_box('command', 0, 1)
        self.draw_save_box('position', 0, 2)
        self.draw_save_box('speed', 0, 3)

        self.draw_plot_real_time('command', 1, 1)
        self.draw_plot_real_time('position', 1, 2)
        self.draw_plot_real_time('speed', 1, 3)

        self.plots = dict()

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

    # def draw_plot_real_time(self):
    #     self.ax.cla()
    #
    #     x = self.parent.df['index']
    #     y = self.parent.df[self.plot_type]
    #
    #     self.ax.plot(x, y, marker='x', color='blue')
    #     self.ax.grid(True)
    #
    #     self.ax.set_title(self.plot_type.upper() + " vs TIME", fontsize=16)
    #     self.ax.set_xlabel("index")
    #     self.ax.set_ylabel(self.plot_type)
    #
    #     self.graph.draw()
    #
    #     if self.parent.isRecording:
    #         self.graph.get_tk_widget().after(self.parent.frequency * 1000, self.plot)  # NOT self.plot()
    #         # if self.parent.simulation_step < 60:
    #         #     self.graph.get_tk_widget().after(self.parent.frequency*1000, self.plot)   #NOT self.plot()
    #     else:
    #         self.savePlotButton.config(state='normal')

    def draw_plot_real_time(self, plot_type, row, column):

        x = self.parent.df['elapsed_time(ms)']
        y = self.parent.df[plot_type]

        f = Figure(figsize=(5, 5))
        ax = f.add_subplot(111)

        ax.cla()
        ax.plot(x, y, marker='x', color='blue')

        ax.grid(True)

        ax.set_title(plot_type.upper() + " vs TIME", fontsize=16)
        ax.set_ylabel(plot_type, fontsize=14)
        ax.set_xlabel("elapsed_time(ms)", fontsize=14)

        canvas = FigureCanvasTkAgg(f, master=self.root)
        canvas.get_tk_widget().grid(row=row, column=column)
        canvas.draw()

        if self.parent.isRecording:
            canvas.get_tk_widget().after(GlobalConfig.PLOTTING_FREQUENCY, lambda: self.draw_plot_real_time(plot_type, row, column))
        else:
            self.savePlotButton[plot_type].config(state='normal')

        return canvas

    def save_plot(self):
        filename = self.fileNameTextField.get()
        CommonFunctions.save_plot(filename, self.parent.df, self.plot_type)
