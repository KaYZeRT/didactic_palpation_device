import os
import tkinter as tk
import pandas as pd
import threading
import time

from tkinter import filedialog
from RealTimePlotWindow import *

LARGE_FONT = ("Verdana", 12)
FREQUENCY = 1  # in SECONDS


class NewRecordingMenu(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # FRAME TITLE
        label = tk.Label(self, text="NEW RECORDING PAGE", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        self.df = None
        self.isRecording = False

        self.command_check_button = tk.IntVar()
        self.position_check_button = tk.IntVar()
        self.speed_check_button = tk.IntVar()

        # BACK TO MAIN WINDOW BUTTON
        self.backButton = tk.Button(self, text="Back to Start Page",
                                    command=lambda: controller.show_frame("MainWindow"))
        self.backButton.pack()

        # START/STOP RECORDING FRAME
        self.startStopFrame = tk.LabelFrame(self, text="START/STOP RECORDING", padx=5, pady=5)
        self.startStopFrame.pack(padx=10, pady=10)

        self.startRecordingButton = tk.Button(self.startStopFrame, text='START', width=30, height=3,
                                              command=lambda: self.start_recording())
        self.startRecordingButton.pack(side=tk.LEFT)

        self.stopRecordingButton = tk.Button(self.startStopFrame, text='STOP', width=30, height=3, state=tk.DISABLED,
                                             command=lambda: self.stop_recording())
        self.stopRecordingButton.pack(side=tk.RIGHT)

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
        self.plotRecordingFrame = tk.LabelFrame(self, text="PLOT", padx=5, pady=5)
        self.plotRecordingFrame.pack(padx=10, pady=10)

        # CHECK BOX FRAME
        self.checkBoxFrame = tk.LabelFrame(self.plotRecordingFrame, padx=5, pady=5, borderwidth=0, highlightthickness=0)
        self.checkBoxFrame.pack(side=tk.LEFT)

        self.c = tk.Checkbutton(self.checkBoxFrame, text="Command", variable=self.command_check_button, anchor='w',
                                width=10)
        self.c.grid(row=0, column=0)

        self.p = tk.Checkbutton(self.checkBoxFrame, text="Position", variable=self.position_check_button, anchor='w',
                                width=10)
        self.p.grid(row=1, column=0)
        self.s = tk.Checkbutton(self.checkBoxFrame, text="Speed", variable=self.speed_check_button, anchor='w',
                                width=10)
        self.s.grid(row=2, column=0)

        # PLOT BUTTON (ADDED TO PLOT RECORDING FRAME)
        self.plotButton = tk.Button(self.plotRecordingFrame, text='PLOT', width=20, height=3, state=tk.DISABLED,
                                    command=lambda: self.new_window(RealTimePlotWindow))
        self.plotButton.pack(side=tk.RIGHT)

        # SIMULATION OF REAL TIME DATA ACQUISITION
        self.simulation_step = 1
        self.simulation_df = pd.read_csv("src/releve_vitesse_2.txt", sep=",", header=None)
        self.simulation_df.columns = ['index', 'command', 'time_since_previous_measurement(µs)', 'time(µs)', 'position',
                                      'speed']

    def new_window(self, _class):
        try:
            if self.new.state() == "normal":
                self.new.focus()
        except:
            self.new = tk.Toplevel(self)
            _class(self.new)

    def save_data(self):
        # NOT COMPLETE
        filename = self.fileNameTextField.get()
        if filename == "":
            tk.messagebox.showerror("Error !", "Filename not defined !")
            return
        save_dir = filedialog.askdirectory(initialdir="C:/Thomas_Data/GitHub/didactic_palpation_device")

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
        self.plotButton.config(state='normal')

        self.df = None
        df = pd.DataFrame(columns=['index',
                                   'command',
                                   'time_since_previous_measurement(µs)',
                                   'time(µs)',
                                   'position',
                                   'speed'])

        threading.Thread(target=self.simulate_real_time_data_acquisition).start()

        return

    def stop_recording(self):
        self.isRecording = False
        self.startRecordingButton.config(state='normal')
        self.stopRecordingButton.config(state='disabled')
        self.saveButton.config(state='normal')
        self.plotButton.config(state='disabled')

        # DATA ACQUISITION SIMULATION
        self.simulation_step = 1

        return

    def simulate_real_time_data_acquisition(self):
        while self.isRecording:
            # print(self.simulation_df.head())
            df = self.simulation_df.iloc[:self.simulation_step, :]
            self.df = df
            # print(self.df.head())
            time.sleep(FREQUENCY)
            self.simulation_step += 1
            print(self.df.tail(1))

        return
