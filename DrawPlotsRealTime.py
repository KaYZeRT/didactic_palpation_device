# import os
# import matplotlib
# import pandas as pd
# import tkinter as tk
#
# import GlobalConfig
# import CommonFunctions
#
# from FileContentWindow import *
#
# import matplotlib.pyplot as plt
#
# from datetime import datetime
# from matplotlib import style
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# from matplotlib.figure import Figure
# from tkinter import filedialog
# from functools import partial

from DrawPlotsParent import *

import time
import threading

matplotlib.use("TkAgg")
style.use("ggplot")
LARGE_FONT = ("Verdana", 12)




def load_simulation_file():
    res = []
    a_file = open("src/data_slave_and_master.txt", "r")
    list_of_lists = [(line.strip()).split() for line in a_file]

    # Remove ','
    for list in list_of_lists:
        subset = []
        for element in list:
            if ',' in element:
                subset.append(element.replace(',', ''))
            else:
                subset.append(element)
        res.append(subset)

    list_of_lists = res
    res = []

    # Transform strings to float (because the numbers are '1' and not 1)
    for list in list_of_lists:
        to_append = [0 for i in range(len(list))]
        for i in range(len(list)):
            if i == 5 or i == 8 or i == 9:
                to_append[i] = float(list[i])
            else:
                to_append[i] = int(list[i])
        res.append(to_append)

    a_file.close()
    return res


def add_row_to_df(df, to_append):
    """Adds the to_append row to the data frame"""
    to_append_series = pd.Series(to_append, index=df.columns, dtype=object)
    df = df.append(to_append_series, ignore_index=True)

    return df


def calculate_elapsed_time(simulation_step, df, interval):
    if simulation_step == 0:
        res = 0
    else:
        elapsed_time = df.loc[df.index[simulation_step - 1], 'elapsed_time(ms)']
        res = elapsed_time + interval
    return res


class DrawPlotsRealTime(tk.Frame, DrawPlotsParent):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.df = None
        self.isRecording = False

        # UPPER FRAME
        self.upperFrame = tk.LabelFrame(self)
        self.upperFrame.pack()

        # FRAME TITLE (IN UPPER FRAME)
        self.frameTitleLabel = tk.Label(self.upperFrame, text="DRAW PLOTS REAL TIME", font=LARGE_FONT, bg='red')
        self.frameTitleLabel.grid(row=0, column=0, padx=15, pady=5)

        # BACK TO MAIN WINDOW BUTTON (IN UPPER FRAME)
        self.backButton = tk.Button(self.upperFrame, text="BACK TO MAIN WINDOW",
                                    command=lambda: controller.show_frame("MainWindow"))
        self.backButton.grid(row=0, column=1)

        # MAIN FRAME
        self.mainLabelFrame = tk.LabelFrame(self)
        self.mainLabelFrame.pack()

        # PLOTS FRAME (IN MAIN FRAME)
        self.ax = dict()
        self.canvas = None

        self.plotsLabelFrame = tk.LabelFrame(self.mainLabelFrame)
        self.plotsLabelFrame.grid(row=1, column=0, rowspan=2)

        CommonFunctions.fill_plots_label_frame(self)

        # RIGHT SIDE FRAME (IN MAIN FRAME)
        self.rightSideLabelFrame = tk.LabelFrame(self.mainLabelFrame, text="RIGHT SIDE FRAME")
        self.rightSideLabelFrame.grid(row=1, column=1, rowspan=2, padx=10, pady=10)

        # ACQUISITION PARAMETERS (IN MAIN FRAME)
        self.acquisitionParametersEntryBox = dict()
        self.acquisitionFrequency = tk.IntVar()
        self.lowValue = tk.IntVar()
        self.highValue = tk.IntVar()
        self.startRecordingButton = None
        self.stopRecordingButton = None
        self.resetRecordingButton = None

        self.acquisitionParametersLabelFrame = tk.LabelFrame(self.rightSideLabelFrame,
                                                             text="ACQUISITION PARAMETERS FRAME",
                                                             padx=5, pady=5)
        self.acquisitionParametersLabelFrame.pack()

        self.fill_acquisition_parameters_label_frame()

        # SAVE RECORDING FRAME
        self.filenameEntry = None
        self.saveFileButton = None

        self.saveRecordingLabelFrame = tk.LabelFrame(self.rightSideLabelFrame, text="SAVE RECORDING", pady=10)
        self.saveRecordingLabelFrame.pack()

        self.fill_save_recording_label_frame()

        # GENERATE OUTPUT WINDOW BUTTON (IN RIGHT SIDE LABEL FRAME)
        self.data_output_window = None

        self.showFileContentWindow = tk.Button(self.rightSideLabelFrame, text="GENERATE OUTPUT WINDOW",
                                               width=30, height=3,
                                               state=tk.DISABLED,
                                               command=lambda: self.generate_data_output_window())
        self.showFileContentWindow.pack(pady=15)

        # PLOTS OPTIONS FRAME (IN MAIN FRAME)
        self.optionsLabelFrame = dict()
        self.plotNameLabel = dict()
        self.plotNameEntry = dict()
        self.savePlotButton = dict()
        self.checkButton = dict()
        self.checkButtonValues = dict()

        self.plotsOptionsLabelFrame = tk.LabelFrame(self.rightSideLabelFrame, text="PLOTS OPTIONS FRAME")
        self.plotsOptionsLabelFrame.pack(padx=10, pady=10)

        CommonFunctions.fill_plots_options_label_frame(self, real_time=1)

        # SIMULATION OF REAL TIME DATA ACQUISITION
        self.simulation_step = 0
        self.simulation_data = load_simulation_file()

    def fill_acquisition_parameters_label_frame(self):
        # ACQUISITION FREQUENCY
        tk.Label(self.acquisitionParametersLabelFrame, padx=15, pady=15,
                 text="ACQUISITION FREQUENCY").grid(row=0, column=0)
        self.acquisitionParametersEntryBox['acquisition_frequency'] = tk.Entry(self.acquisitionParametersLabelFrame,
                                                                               borderwidth=3, width=10)
        self.acquisitionParametersEntryBox['acquisition_frequency'].grid(row=0, column=1)
        self.acquisitionParametersEntryBox['acquisition_frequency'].insert(0, 0)

        # LOW VALUE
        tk.Label(self.acquisitionParametersLabelFrame, padx=15, pady=15,
                 text="LOW VALUE").grid(row=1, column=0)
        self.acquisitionParametersEntryBox['low_value'] = tk.Entry(self.acquisitionParametersLabelFrame,
                                                                   borderwidth=3, width=10)
        self.acquisitionParametersEntryBox['low_value'].grid(row=1, column=1)
        self.acquisitionParametersEntryBox['low_value'].insert(0, 0)

        # HIGH VALUE
        tk.Label(self.acquisitionParametersLabelFrame, padx=15, pady=15,
                 text="HIGH VALUE").grid(row=2, column=0)
        self.acquisitionParametersEntryBox['high_value'] = tk.Entry(self.acquisitionParametersLabelFrame,
                                                                    borderwidth=3, width=10)
        self.acquisitionParametersEntryBox['high_value'].grid(row=2, column=1)
        self.acquisitionParametersEntryBox['high_value'].insert(0, 0)

        self.startRecordingButton = tk.Button(self.acquisitionParametersLabelFrame, text='START', width=20, height=1,
                                              command=self.start_recording)
        self.startRecordingButton.grid(row=0, column=2, padx=10)

        self.stopRecordingButton = tk.Button(self.acquisitionParametersLabelFrame, text='STOP', width=20, height=1,
                                             command=self.stop_recording,
                                             state=tk.DISABLED)
        self.stopRecordingButton.grid(row=1, column=2, padx=10)

        self.resetRecordingButton = tk.Button(self.acquisitionParametersLabelFrame, text='RESET', width=20, height=1,
                                              command=self.reset_recording)
        self.resetRecordingButton.grid(row=2, column=2, padx=10)

    def fill_save_recording_label_frame(self):
        tk.Label(self.saveRecordingLabelFrame, text="FILENAME: ").grid(row=0, column=0)

        self.filenameEntry = tk.Entry(self.saveRecordingLabelFrame, borderwidth=3)
        self.filenameEntry.grid(row=0, column=1)
        self.filenameEntry.insert(0, "data_acquisition")

        self.saveFileButton = tk.Button(self.saveRecordingLabelFrame, text='SAVE',
                                        width=10, height=1,
                                        state=tk.DISABLED)
        self.saveFileButton.grid(row=0, column=2, padx=10)

    def start_recording(self):
        self.isRecording = True
        self.startRecordingButton.config(state='disabled')
        self.stopRecordingButton.config(state="normal")
        self.saveFileButton.config(state='disabled')

        self.df = pd.DataFrame(columns=GlobalConfig.DATA_FRAME_COLUMNS + ['elapsed_time(ms)'])

        threading.Thread(target=self.simulate_real_time_data_acquisition).start()

        CommonFunctions.refresh_all_plots(self, real_time=1)
        # self.refresh_all_plots(1)

        return

    def stop_recording(self):
        self.isRecording = False
        self.stopRecordingButton.config(state='disabled')
        self.saveFileButton.config(state='normal')

        # DATA ACQUISITION SIMULATION
        self.simulation_step = 0

    def reset_recording(self):
        self.isRecording = False
        # self.outputText.delete(1.0, tk.END)
        self.df = None

        self.startRecordingButton.config(state='normal')
        self.stopRecordingButton.config(state='disabled')

        self.simulation_step = 0

    def simulate_real_time_data_acquisition(self):
        while self.isRecording:
            # Only load one line (the one associated with simulation_step)
            row = self.simulation_data[self.simulation_step].copy()
            row[1] = int(round(row[1] / 1000, 0))  # interval
            row[2] = int(round(row[2] / 1000, 0))  # time
            row.append(calculate_elapsed_time(self.simulation_step, self.df, row[1]))

            self.df = add_row_to_df(self.df, row)
            self.simulation_step += 1

            time.sleep(GlobalConfig.ACQUISITION_FREQUENCY)

        return
