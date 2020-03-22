import pandas as pd
import tkinter as tk
import matplotlib
import matplotlib.pyplot as plt

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import filedialog

pd.set_option('display.expand_frame_repr', False)
matplotlib.use("TkAgg")


class PlotWindow:
    def __init__(self, root, df, plot_type):
        self.root = root
        self.root.title('Plot: ' + plot_type.upper() + " vs TIME")

        self.df = df
        self.plot_type = plot_type

        self.upperFrame = tk.LabelFrame(self.root, pady=10)
        self.upperFrame.pack()

        self.fileNameFrame = tk.LabelFrame(self.upperFrame, borderwidth=0, highlightthickness=0)
        self.fileNameFrame.pack(side=tk.LEFT)

        self.fileNameLabel = tk.Label(self.fileNameFrame, text="Enter file name : ")
        self.fileNameLabel.pack(side=tk.LEFT)

        self.fileNameTextField = tk.Entry(self.fileNameFrame, borderwidth=3)
        self.fileNameTextField.pack(side=tk.RIGHT)
        self.fileNameTextField.insert(0, self.plot_type + "VsTime")

        self.savePlot = tk.Button(self.upperFrame, text='SAVE PLOT', padx=10,
                                  command=lambda: self.save_plot())
        self.savePlot.pack(side=tk.RIGHT)

        self.plot()

    def plot(self):
        x = self.df['elapsed_time(µs)']
        y = self.df[self.plot_type]

        f = Figure(figsize=(8, 8))
        a = f.add_subplot(111)
        a.plot(x, y, marker='x', color='blue')
        a.grid(True)

        a.set_title(self.plot_type.upper() + " vs TIME", fontsize=16)
        a.set_ylabel(self.plot_type, fontsize=14)
        a.set_xlabel("elapsed_time(µs)", fontsize=14)

        canvas = FigureCanvasTkAgg(f, master=self.root)
        canvas.get_tk_widget().pack()
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

        return 0