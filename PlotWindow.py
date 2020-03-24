import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import tkinter as tk

from matplotlib import style
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import filedialog

pd.set_option('display.expand_frame_repr', False)
matplotlib.use("TkAgg")
style.use("ggplot")


class PlotWindow:

    def __init__(self, root, df, plot_type):
        self.root = root
        self.root.title('Plot: ' + plot_type.upper() + " vs TIME")

        self.df = df
        self.plot_type = plot_type

        # UPPER FRAME
        self.upperFrame = tk.LabelFrame(self.root, pady=10)
        self.upperFrame.grid(row=0, column=0)

        # FILE NAME LABEL
        self.fileNameLabel = tk.Label(self.upperFrame, text="Enter file name : ")
        self.fileNameLabel.grid(row=0, column=0)

        # FILE NAME TEXT FIELD
        self.fileNameTextField = tk.Entry(self.upperFrame, borderwidth=3)
        self.fileNameTextField.grid(row=0, column=1)
        self.fileNameTextField.insert(0, self.plot_type + "VsTime")

        # SAVE PLOT BUTTON
        self.savePlotButton = tk.Button(self.upperFrame, text='SAVE PLOT', padx=10,
                                        command=lambda: self.save_plot())
        self.savePlotButton.grid(row=0, column=2)

        self.plot()

    def plot(self):
        x = self.df['elapsed_time(µs)']
        y = self.df[self.plot_type]

        f = Figure(figsize=(8, 8))
        ax = f.add_subplot(111)
        ax.plot(x, y, marker='x', color='blue')
        ax.grid(True)

        ax.set_title(self.plot_type.upper() + " vs TIME", fontsize=16)
        ax.set_ylabel(self.plot_type, fontsize=14)
        ax.set_xlabel("elapsed_time(µs)", fontsize=14)

        canvas = FigureCanvasTkAgg(f, master=self.root)
        canvas.get_tk_widget().grid(row=1, column=0)
        canvas.draw()

        return canvas

    def save_plot(self):
        filename = self.fileNameTextField.get()
        if filename == "":
            tk.messagebox.showerror("Error !", "Filename not defined !")
            return
        save_dir = filedialog.askdirectory(initialdir="C:/Thomas_Data/GitHub/didactic_palpation_device")

        try:
            x = self.df['elapsed_time(µs)']
            y = self.df[self.plot_type]

            plt.figure()
            plt.plot(x, y, marker='x', color='blue')
            plt.grid(True)

            plt.title(self.plot_type.upper() + " vs TIME")
            plt.xlabel("elapsed_time(µs)")
            plt.ylabel(self.plot_type)
            plt.savefig(save_dir + "/" + filename + ".png")

        except:
            tk.messagebox.showerror("Error !", "Error while saving file !")

        return
