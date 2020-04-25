import os
import tkinter as tk
import pandas as pd

import GlobalConfig
import CommonFunctions

from PlotWindow import *

pd.set_option('display.expand_frame_repr', False)
LARGE_FONT = ("Verdana", 12)


def create_data_frame(file_path):
    data = pd.read_csv(file_path, sep=",", header=None)
    data.columns = ['index', 'command', 'interval(ms)', 'time(ms)', 'position', 'speed']

    data['interval(ms)'] = CommonFunctions.convert_us_to_ms(data['interval(ms)'])
    data['time(ms)'] = CommonFunctions.convert_us_to_ms(data['time(ms)'])

    data = CommonFunctions.add_elapsed_time_to_df(data)

    return data


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

        # FILE SELECTION FRAME
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

        self.generatePlotsButton = tk.Button(self.generatePlotFrame, text='GENERATE ALL PLOTS',
                                             state=tk.DISABLED,
                                             width=30, height=3,
                                             command=lambda: self.new_plot_window(PlotWindow))
        self.generatePlotsButton.pack()

        # OUTPUT FRAME
        self.outputFrame = tk.LabelFrame(self, text="OUTPUT")
        self.outputFrame.pack(padx=10, pady=10)

        self.outputText = tk.Text(self.outputFrame, width=80, height=30)
        self.outputText.pack(padx=10, pady=10)

    def import_recording(self):
        file = tk.filedialog.askopenfilenames(initialdir=GlobalConfig.DEFAULT_DIR,
                                              initialfile="tmp",
                                              filetypes=[("All files", "*")]
                                              )
        try:
            file_path = file[0]
            self.selectedFile.set("FILE: " + os.path.basename(file_path))

            self.df = create_data_frame(file_path)
            self.enable_button()

            # PRINT NEW DATA TO OUTPUT FRAME
            self.outputText.delete(1.0, tk.END)
            string = self.df.to_string(index=False)
            self.outputText.insert(tk.END, string + "\n")
            self.outputText.see("end")

        except IndexError:
            print("No file selected")

    def enable_button(self):
        self.generatePlotsButton.config(state='normal')

    def new_plot_window(self, _class):
        self.new = tk.Toplevel(self)
        _class(self.new, self.df)
