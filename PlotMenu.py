import os
import tkinter as tk
import pandas as pd

from PlotWindow import *

pd.set_option('display.expand_frame_repr', False)
LARGE_FONT = ("Verdana", 12)


def create_data_frame(file_path):
    data = pd.read_csv(file_path, sep=",", header=None)
    data.columns = ['index', 'command', 'time_between_measure(µs)', 'time(µs)', 'position', 'speed']

    data = time_calculation(data)

    data = data[['index', 'time(µs)', 'elapsed_time(µs)', 'time_between_measure(µs)', 'command', 'position',
                 'speed']]

    return data


def time_calculation(df):
    ls = [0]
    time_previous_measurement = df['time_between_measure(µs)']

    for i in range(1, df.shape[0]):
        ls.append(ls[i - 1] + time_previous_measurement[i])

    df['elapsed_time(µs)'] = ls
    return df


class PlotMenu(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # FRAME TITLE
        label = tk.Label(self, text="PLOT PAGE", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        # DATA FRAME
        self.df = None

        # Back to Main Window
        self.backButton = tk.Button(self, text="Back to Start Page",
                                    command=lambda: controller.show_frame("MainWindow"))
        self.backButton.pack()

        # FILE FRAME
        self.fileFrame = tk.LabelFrame(self, text="FILE SELECTION BOX", padx=5, pady=5)
        self.fileFrame.pack(padx=10, pady=10)

        self.importRecordingButton = tk.Button(self.fileFrame, text='SELECT FILE', width=30, height=3,
                                               command=lambda: self.import_recording())
        self.importRecordingButton.pack()

        self.selectedFile = tk.StringVar()
        self.selectedFile.set('FILE: no file selected')
        self.isFileSelectedLabel = tk.Label(self.fileFrame, textvariable=self.selectedFile, pady=5)
        self.isFileSelectedLabel.pack()

        # GENERATE PLOT FRAME
        self.generatePlotFrame = tk.LabelFrame(self, text="PLOT BOX", padx=5, pady=5)
        self.generatePlotFrame.pack(padx=10, pady=10)

        # GENERATE COMMAND PLOT BUTTON
        self.generateCommandPlotButton = tk.Button(self.generatePlotFrame, text='GENERATE COMMAND PLOT',
                                                   state=tk.DISABLED,
                                                   width=30, height=3,
                                                   command=lambda: self.new_plot_window(PlotWindow, 'command'))
        self.generateCommandPlotButton.pack()

        # GENERATE POSITION PLOT BUTTON
        self.generatePositionPlotButton = tk.Button(self.generatePlotFrame, text='GENERATE POSITION PLOT',
                                                    state=tk.DISABLED,
                                                    width=30, height=3,
                                                    command=lambda: self.new_plot_window(PlotWindow, 'position'))
        self.generatePositionPlotButton.pack()

        # GENERATE SPEED PLOT BUTTON
        self.generateSpeedPlotButton = tk.Button(self.generatePlotFrame, text='GENERATE SPEED PLOT', state=tk.DISABLED,
                                                 width=30, height=3,
                                                 command=lambda: self.new_plot_window(PlotWindow, 'speed'))
        self.generateSpeedPlotButton.pack()

        # OUTPUT FRAME
        self.outputFrame = tk.LabelFrame(self, text="OUTPUT")
        self.outputFrame.pack(padx=10, pady=10)

        self.outputText = tk.Text(self.outputFrame, width=80, height=20)
        self.outputText.pack(padx=10, pady=10)

    def import_recording(self):
        file = tk.filedialog.askopenfilenames(initialdir="C:/Thomas_Data/GitHub/didactic_palpation_device/src",
                                              initialfile="tmp",
                                              filetypes=[("All files", "*")]
                                              )
        try:
            file_path = file[0]
            self.selectedFile.set("FILE: " + os.path.basename(file_path))

            self.df = create_data_frame(file_path)
            self.enable_buttons()

            # PRINT NEW DATA TO OUTPUT FRAME
            self.outputText.delete(1.0, tk.END)
            string = self.df.to_string(index=False)
            self.outputText.insert(tk.END, string + "\n")
            self.outputText.see("end")

        except IndexError:
            print("No file selected")

        return

    def enable_buttons(self):
        self.generateCommandPlotButton.config(state="normal")
        self.generatePositionPlotButton.config(state="normal")
        self.generateSpeedPlotButton.config(state="normal")

        return

    def new_plot_window(self, _class, plot_type):
        self.new = tk.Toplevel(self)
        _class(self.new, self.df, plot_type)

        return
