import os
import matplotlib
import pandas as pd
import tkinter as tk

import GlobalConfig
import CommonFunctions

from datetime import datetime
from matplotlib import style
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import filedialog

matplotlib.use("TkAgg")
style.use("ggplot")


def create_data_frame(file_path):
    data = pd.read_csv(file_path, sep=",", header=None)
    data.columns = ['index', 'command', 'interval(ms)', 'time(ms)', 'position', 'speed']

    data['interval(ms)'] = CommonFunctions.convert_us_to_ms(data['interval(ms)'])
    data['time(ms)'] = CommonFunctions.convert_us_to_ms(data['time(ms)'])

    data = CommonFunctions.add_elapsed_time_to_df(data)

    return data


class DrawPlotsFromFile(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.df = None
        self.date = datetime.today().strftime('%Y-%m-%d_%H-%M')

        # SAVE BOXES CREATION
        self.saveFrame = dict()
        self.fileNameLabel = dict()
        self.fileNameTextField = dict()
        self.savePlotButton = dict()

        self.draw_save_box('command', 0, 0)
        self.draw_save_box('position', 0, 1)
        self.draw_save_box('speed', 0, 2)

        # PLOTS CREATION
        self.plots = dict()
        self.ax = dict()
        self.canvas = dict()

        self.create_plot('command', 1, 0)
        self.create_plot('position', 1, 1)
        self.create_plot('speed', 1, 2)

        # LOWER LEFT FRAME
        self.lowerLeftFrame = tk.LabelFrame(self, pady=10)
        self.lowerLeftFrame.grid(row=2, column=0)

        self.backButton = tk.Button(self.lowerLeftFrame, text="Back to Start Page",
                                    command=lambda: controller.show_frame("MainWindow"))
        self.backButton.pack()

        # FILE SELECTION FRAME (IN LOWER LEFT FRAME)
        self.fileFrame = tk.LabelFrame(self.lowerLeftFrame, text="FILE SELECTION BOX", padx=5, pady=5)
        self.fileFrame.pack(padx=10, pady=10)

        self.selectFileButton = tk.Button(self.fileFrame, text='SELECT FILE', width=30, height=3,
                                          command=lambda: self.import_recording())
        self.selectFileButton.pack()

        self.selectedFileText = tk.StringVar()
        self.selectedFileText.set('FILE: no file selected')
        self.isFileSelectedLabel = tk.Label(self.fileFrame, textvariable=self.selectedFileText, pady=5)
        self.isFileSelectedLabel.pack()

        # OUTPUT FRAME (LOWER RIGHT)
        self.outputFrame = tk.LabelFrame(self, text="OUTPUT")
        self.outputFrame.grid(row=2, column=1, columnspan=2)

        self.outputText = tk.Text(self.outputFrame, width=110, height=20)
        self.outputText.pack(padx=5, pady=5)

    def draw_save_box(self, plot_type, row, column):
        # SAVE FRAME
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
                                                   state=tk.DISABLED,
                                                   command=lambda: self.save_plot(plot_type))
        self.savePlotButton[plot_type].grid(row=0, column=2)

    def create_plot(self, plot_type, row, column):
        f = Figure(figsize=(5, 5))
        ax = f.add_subplot(111)

        ax.grid(True)

        ax.set_title(plot_type.upper() + " vs TIME", fontsize=16)
        ax.set_ylabel(plot_type, fontsize=14)
        ax.set_xlabel("elapsed_time(ms)", fontsize=14)

        canvas = FigureCanvasTkAgg(f, master=self)
        canvas.get_tk_widget().grid(row=row, column=column)
        canvas.draw()

        self.ax[plot_type] = ax
        self.canvas[plot_type] = canvas

    def import_recording(self):
        file = tk.filedialog.askopenfilenames(initialdir=GlobalConfig.DEFAULT_DIR,
                                              initialfile="tmp",
                                              filetypes=[("All files", "*")]
                                              )
        try:
            file_path = file[0]
            self.selectedFileText.set("FILE: " + os.path.basename(file_path))

            self.df = create_data_frame(file_path)

            # PRINT NEW DATA TO OUTPUT FRAME
            self.outputText.delete(1.0, tk.END)
            string = self.df.to_string(index=False)
            self.outputText.insert(tk.END, string + "\n")
            self.outputText.see("end")

            # DRAW ALL PLOTS
            self.refresh_all_plots()

        except IndexError:
            print("No file selected")

    def save_plot(self, plot_type):
        filename = self.fileNameTextField[plot_type].get()
        CommonFunctions.save_plot(filename, self.df, plot_type)

    def refresh_plot(self, plot_type):
        x = self.df['elapsed_time(ms)']
        y = self.df[plot_type]

        self.ax[plot_type].cla()
        self.ax[plot_type].plot(x, y, marker='x', color='blue')

        self.canvas[plot_type].draw()

        self.savePlotButton[plot_type].config(state='normal')

    def refresh_all_plots(self):
        self.refresh_plot('command')
        self.refresh_plot('position')
        self.refresh_plot('speed')
