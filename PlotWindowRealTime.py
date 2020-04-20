import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import tkinter as tk

import CommonFunctions

from matplotlib import style
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import filedialog

pd.set_option('display.expand_frame_repr', False)
matplotlib.use("TkAgg")
style.use("ggplot")


class RealTimePlotWindow(tk.Tk):

    def __init__(self, root, plot_type, new_recording_menu):
        self.plot_type = plot_type
        self.parent = new_recording_menu

        self.root = root
        self.root.title("Real Time Plot")

        # UPPER FRAME
        self.upperFrame = tk.LabelFrame(self.root, pady=10)
        # self.upperFrame.grid(row=0, column=0)
        self.upperFrame.pack()

        # FILE NAME LABEL
        self.fileNameLabel = tk.Label(self.upperFrame, text="Enter file name : ")
        self.fileNameLabel.grid(row=0, column=0)

        # FILE NAME TEXT FIELD
        self.fileNameTextField = tk.Entry(self.upperFrame, borderwidth=3)
        self.fileNameTextField.grid(row=0, column=1)
        self.fileNameTextField.insert(0, self.plot_type + "VsTime")

        # SAVE PLOT BUTTON
        self.savePlotButton = tk.Button(self.upperFrame, text='SAVE PLOT', padx=10, state=tk.DISABLED,
                                        command=lambda: self.save_plot())
        self.savePlotButton.grid(row=0, column=2)

        fig = Figure()
        self.ax = fig.add_subplot(111)
        self.ax.set_xlabel("index")
        self.ax.set_ylabel(self.plot_type)
        self.ax.grid(True)

        self.graph = FigureCanvasTkAgg(fig, master=root)
        self.graph.get_tk_widget().pack(side="top", fill='both', expand=True)

        self.draw_plot_real_time()

    def draw_plot_real_time(self):
        self.ax.cla()

        x = self.parent.df['index']
        y = self.parent.df[self.plot_type]

        self.ax.plot(x, y, marker='x', color='blue')
        self.ax.grid(True)

        self.ax.set_title(self.plot_type.upper() + " vs TIME", fontsize=16)
        self.ax.set_xlabel("index")
        self.ax.set_ylabel(self.plot_type)

        self.graph.draw()

        if self.parent.isRecording:
            self.graph.get_tk_widget().after(self.parent.frequency * 1000, self.plot)  # NOT self.plot()
            # if self.parent.simulation_step < 60:
            #     self.graph.get_tk_widget().after(self.parent.frequency*1000, self.plot)   #NOT self.plot()
        else:
            self.savePlotButton.config(state='normal')

    def save_plot(self):
        filename = self.fileNameTextField.get()
        CommonFunctions.save_plot(filename, self.parent.df, self.plot_type)