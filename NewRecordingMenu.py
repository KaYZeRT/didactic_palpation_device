import os
import tkinter as tk
import pandas as pd
import threading
import time
import GlobalConfig
import numpy as np

from tkinter import filedialog
from PlotWindowRealTime import *

pd.set_option('display.expand_frame_repr', False)
LARGE_FONT = ("Verdana", 12)


def load_simulation_file():
    res = []
    a_file = open("src/releve_vitesse_2.txt", "r")
    list_of_lists = [(line.strip()).split() for line in a_file]

    # Remove ','
    for list in list_of_lists:
        for element in list:
            if element == ',':
                list.remove(element)

    # Transform strings to float (because the numbers are '1' and not 1)
    for list in list_of_lists:
        to_append = [0 for i in range(len(list))]
        for i in range(len(list)):
            if i == len(list) - 1:
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
        elapsed_time = df.loc[df.index[simulation_step-1], 'elapsed_time(ms)']
        res = elapsed_time + interval
    return res


class NewRecordingMenu(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.df = None
        self.isRecording = False

        self.command_check_button = tk.IntVar()
        self.position_check_button = tk.IntVar()
        self.speed_check_button = tk.IntVar()

        # FRAME TITLE
        label = tk.Label(self, text="NEW RECORDING PAGE", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        # BACK TO MAIN WINDOW BUTTON
        self.backButton = tk.Button(self, text="Back to Start Page",
                                    command=lambda: controller.show_frame("MainWindow"))
        self.backButton.pack()

        # START/STOP RECORDING FRAME
        self.startStopFrame = tk.LabelFrame(self, text="START/STOP RECORDING", padx=5, pady=5)
        self.startStopFrame.pack(padx=10, pady=10)

        self.startRecordingButton = tk.Button(self.startStopFrame, text='START', width=20, height=3,
                                              command=lambda: self.start_recording())
        self.startRecordingButton.grid(row=0, column=0)

        self.stopRecordingButton = tk.Button(self.startStopFrame, text='STOP', width=20, height=3, state=tk.DISABLED,
                                             command=lambda: self.stop_recording())
        self.stopRecordingButton.grid(row=0, column=1)

        # SAVE RECORDING FRAME
        self.saveFrame = tk.LabelFrame(self, text="SAVE RECORDING", pady=10)
        self.saveFrame.pack()

        self.fileNameLabel = tk.Label(self.saveFrame, text="Enter file name : ")
        self.fileNameLabel.grid(row=0, column=0)

        self.fileNameTextField = tk.Entry(self.saveFrame, borderwidth=3)
        self.fileNameTextField.grid(row=0, column=1)
        self.fileNameTextField.insert(0, "data_acquisition")

        self.saveButton = tk.Button(self.saveFrame, text='SAVE', padx=10, state=tk.DISABLED,
                                    command=lambda: self.save_data())
        self.saveButton.grid(row=0, column=2)

        # PLOT RECORDING FRAME
        self.plotRecordingFrame = tk.LabelFrame(self, text="PLOT RECORDING", padx=5, pady=5)
        self.plotRecordingFrame.pack(padx=10, pady=10)

        # PLOT BUTTON (ADDED TO PLOT RECORDING FRAME)
        self.plotCommandButton = tk.Button(self.plotRecordingFrame, text='COMMAND', width=20, height=3,
                                           state=tk.DISABLED,
                                           command=lambda: self.new_window(RealTimePlotWindow, 'command'))
        self.plotCommandButton.grid(row=0, column=0)

        self.plotPositionButton = tk.Button(self.plotRecordingFrame, text='POSITION', width=20, height=3,
                                            state=tk.DISABLED,
                                            command=lambda: self.new_window(RealTimePlotWindow, 'position'))
        self.plotPositionButton.grid(row=1, column=0)

        self.plotSpeedButton = tk.Button(self.plotRecordingFrame, text='SPEED', width=20, height=3,
                                         state=tk.DISABLED,
                                         command=lambda: self.new_window(RealTimePlotWindow, 'speed'))
        self.plotSpeedButton.grid(row=2, column=0)

        # OUTPUT FRAME
        self.outputFrame = tk.LabelFrame(self, text="OUTPUT")
        self.outputFrame.pack(padx=10, pady=10)

        self.outputText = tk.Text(self.outputFrame, width=80, height=20)
        self.outputText.pack(padx=10, pady=10)

        # SIMULATION OF REAL TIME DATA ACQUISITION
        self.simulation_step = 0
        self.simulation_data = load_simulation_file()

    def new_window(self, _class, plot_type):
        self.new = tk.Toplevel(self)
        _class(self.new, plot_type, self)

    def save_data(self):
        filename = self.fileNameTextField.get()
        if filename == "":
            tk.messagebox.showerror("Error !", "Filename not defined !")
            return
        save_dir = filedialog.askdirectory(initialdir=GlobalConfig.DEFAULT_SAVE_DIR)

        try:
            export_csv = self.df.to_csv(save_dir + '/' + filename + '.txt')
        except:
            tk.messagebox.showerror("Error !", "Error while saving file !")

        return

    def start_recording(self):
        self.isRecording = True
        self.startRecordingButton.config(state='disabled')
        self.stopRecordingButton.config(state="normal")
        self.saveButton.config(state='disabled')
        self.plotCommandButton.config(state='normal')
        self.plotPositionButton.config(state='normal')
        self.plotSpeedButton.config(state='normal')

        self.df = pd.DataFrame(columns=['index',
                                        'command',
                                        'interval(ms)',
                                        'time(ms)',
                                        'position',
                                        'speed',
                                        'elapsed_time(ms)'])

        threading.Thread(target=self.simulate_real_time_data_acquisition).start()

        return

    def stop_recording(self):
        self.isRecording = False
        self.startRecordingButton.config(state='normal')
        self.stopRecordingButton.config(state='disabled')
        self.saveButton.config(state='normal')

        # DATA ACQUISITION SIMULATION
        self.simulation_step = 0

        return

    def simulate_real_time_data_acquisition(self):
        while self.isRecording:
            # Only load one line (the one associated with simulation_step)
            row = self.simulation_data[self.simulation_step]
            row[2] = int(round(row[2] / 1000, 0))
            row[3] = int(round(row[3] / 1000, 0))
            row.append(calculate_elapsed_time(self.simulation_step, self.df, row[2]))

            self.df = add_row_to_df(self.df, row)
            self.simulation_step += 1

            # PRINT NEW DATA TO OUTPUT FRAME
            self.outputText.delete(1.0, tk.END)
            string = self.df.to_string(index=False)
            self.outputText.insert(tk.END, string + "\n")
            self.outputText.see("end")

            time.sleep(GlobalConfig.ACQUISITION_FREQUENCY)

        return
