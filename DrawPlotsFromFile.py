import os
import matplotlib
import pandas as pd
import tkinter as tk

import GlobalConfig
import CommonFunctions

from FileContentWindow import *

import matplotlib.pyplot as plt

from datetime import datetime
from matplotlib import style
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import filedialog
from functools import partial

matplotlib.use("TkAgg")
style.use("ggplot")
LARGE_FONT = ("Verdana", 12)


def create_data_frame(file_path):
    data = pd.read_csv(file_path, sep=",", header=None)
    data.columns = GlobalConfig.DATA_FRAME_COLUMNS

    data['interval(ms)'] = CommonFunctions.convert_us_to_ms(data['interval(ms)'])
    data['time(ms)'] = CommonFunctions.convert_us_to_ms(data['time(ms)'])

    data = CommonFunctions.add_elapsed_time_to_df(data)

    # CONVERT POSITION TO DEGREES (SLAVE)
    pos_slave_deg = []
    for element in data['position_slave']:
        pos_slave_deg.append(CommonFunctions.convert_position_to_degrees(element))
    data['position_slave_deg'] = pos_slave_deg

    # CONVERT POSITION TO DEGREES (MASTER)
    pos_master_deg = []
    for element in data['position_master']:
        pos_master_deg.append(CommonFunctions.convert_position_to_degrees(element))
    data['position_master_deg'] = pos_master_deg

    # CONVERT COMMAND TO AMPERES (SLAVE)
    command_slave_amp = []
    for element in data['command_slave']:
        command_slave_amp.append(CommonFunctions.convert_command_to_amps(element))
    data['command_slave_amp'] = command_slave_amp

    # CONVERT COMMAND TO AMPERES (MASTER)
    command_master_amp = []
    for element in data['command_master']:
        command_master_amp.append(CommonFunctions.convert_command_to_amps(element))
    data['command_master_amp'] = command_master_amp

    return data


class DrawPlotsFromFile(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.df = None

        # FRAME TITLE
        tk.Label(self, text="DRAW PLOTS FROM FILE", font=LARGE_FONT, bg='red').pack(pady=5)

        # MAIN FRAME
        self.mainLabelFrame = tk.LabelFrame(self)
        self.mainLabelFrame.pack()

        # PLOTS FRAME (IN MAIN FRAME)
        self.ax = dict()
        self.canvas = None

        self.plotsLabelFrame = tk.LabelFrame(self.mainLabelFrame)
        self.plotsLabelFrame.grid(row=1, column=0, rowspan=2)

        self.fill_plots_label_frame()

        # RIGHT SIDE FRAME (IN MAIN FRAME)
        self.rightSideLabelFrame = tk.LabelFrame(self.mainLabelFrame, text="RIGHT SIDE FRAME")
        self.rightSideLabelFrame.grid(row=1, column=1, rowspan=2, padx=10, pady=10)

        # BACK TO MAIN WINDOW BUTTON
        self.backButton = tk.Button(self.rightSideLabelFrame, text="BACK TO MAIN WINDOW",
                                    width=30, height=3,
                                    command=lambda: controller.show_frame("MainWindow"))
        self.backButton.pack(pady=15)

        # FILE SELECTION FRAME (IN MAIN FRAME)
        self.selectFileButton = None
        self.selectedFileText = None
        self.isFileSelectedLabel = None

        self.fileSelectionLabelFrame = tk.LabelFrame(self.rightSideLabelFrame, text="FILE SELECTION FRAME",
                                                     padx=5, pady=5)
        self.fileSelectionLabelFrame.pack()

        self.fill_file_selection_label_frame()

        # GENERATE OUTPUT WINDOW BUTTON (IN RIGHT SIDE LABEL FRAME)
        self.data_output_window = None

        self.showFileContentWindow = tk.Button(self.rightSideLabelFrame, text="GENERATE OUTPUT WINDOW",
                                               width=30, height=3,
                                               state=tk.DISABLED,
                                               command=lambda: self.generate_data_output_window())
        self.showFileContentWindow.pack(pady=15)

        # PLOTS OPTIONS FRAME (IN MAIN FRAME)
        self.optionsLabelFrame = dict()
        self.fileNameLabel = dict()
        self.fileNameEntry = dict()
        self.savePlotButton = dict()
        self.checkButton = dict()
        self.checkButtonValues = dict()

        self.plotsOptionsLabelFrame = tk.LabelFrame(self.rightSideLabelFrame, text="PLOTS OPTIONS FRAME")
        self.plotsOptionsLabelFrame.pack(padx=10, pady=10)

        self.fill_plots_options_label_frame()

    def generate_data_output_window(self):
        try:
            if self.data_output_window.state() == "normal":
                self.data_output_window.focus()
        except:
            self.data_output_window = tk.Toplevel(self)
            FileContentWindow(self.data_output_window, self)

    def fill_plots_label_frame(self):
        f = Figure(figsize=(11, 9))

        index = 1
        for plot_type in GlobalConfig.PLOT_TYPES:
            self.ax[plot_type] = f.add_subplot(2, 2, index)
            self.ax[plot_type].set_title(plot_type.upper() + " vs TIME", fontsize=16)
            index += 1

        # DO NOT MODIFY THE LINE BELOW - PREVENTS WHITE SPACES
        f.subplots_adjust(left=0.085, right=0.98, top=0.95, bottom=0.05, wspace=0.3, hspace=0.3)

        self.canvas = FigureCanvasTkAgg(f, master=self.plotsLabelFrame)
        self.canvas.get_tk_widget().pack()
        self.canvas.draw()

    def fill_file_selection_label_frame(self):
        self.selectFileButton = tk.Button(self.fileSelectionLabelFrame, text='SELECT FILE', width=30, height=3,
                                          command=lambda: self.import_recording())
        self.selectFileButton.pack()

        self.selectedFileText = tk.StringVar()
        self.selectedFileText.set('FILE: no file selected')
        self.isFileSelectedLabel = tk.Label(self.fileSelectionLabelFrame, textvariable=self.selectedFileText,
                                            pady=5)
        self.isFileSelectedLabel.pack()

    def fill_plots_options_label_frame(self):
        row_frame = 0
        column_frame = 0
        for plot_type in GlobalConfig.PLOT_TYPES:
            self.optionsLabelFrame[plot_type] = tk.LabelFrame(self.plotsOptionsLabelFrame, padx=15, pady=15,
                                                              text=plot_type.upper())
            self.optionsLabelFrame[plot_type].grid(row=row_frame, column=column_frame, padx=10, pady=5)

            # FILE NAME LABEL
            self.fileNameLabel[plot_type] = tk.Label(self.optionsLabelFrame[plot_type],
                                                     text="FILE NAME:")
            self.fileNameLabel[plot_type].grid(row=0, column=0, padx=10)

            # FILE NAME TEXT FIELD
            self.fileNameEntry[plot_type] = tk.Entry(self.optionsLabelFrame[plot_type], borderwidth=3, width=40)
            self.fileNameEntry[plot_type].grid(row=0, column=1)
            self.fileNameEntry[plot_type].insert(0, plot_type.capitalize())

            # SAVE BUTTON
            self.savePlotButton[plot_type] = tk.Button(self.optionsLabelFrame[plot_type], text='SAVE PLOT', padx=10,
                                                       state=tk.DISABLED,
                                                       command=partial(self.save_plot, plot_type)
                                                       )
            self.savePlotButton[plot_type].grid(row=0, column=2)

            # MASTER CHECK BUTTON
            key = plot_type + "_master"
            if key != 'force_master':
                # THE FORCE IS ONLY MEASURED FOR THE SLAVE
                self.checkButtonValues[key] = tk.IntVar()
                self.checkButtonValues[key].set(1)

                self.checkButton[key] = tk.Checkbutton(self.optionsLabelFrame[plot_type], text="MASTER",
                                                       variable=self.checkButtonValues[key],
                                                       command=lambda: self.refresh_all_plots(),
                                                       fg='red'
                                                       )
                self.checkButton[key].grid(row=1, column=1)

            # SLAVE CHECK BUTTON
            key = plot_type + "_slave"
            self.checkButtonValues[key] = tk.IntVar()
            self.checkButtonValues[key].set(1)

            self.checkButton[key] = tk.Checkbutton(self.optionsLabelFrame[plot_type], text="SLAVE",
                                                   variable=self.checkButtonValues[key],
                                                   command=lambda: self.refresh_all_plots(),
                                                   fg='blue'
                                                   )
            self.checkButton[key].grid(row=2, column=1)

            # CONVERT COMMAND TO AMPS CHECKBOX
            if plot_type == 'command':
                key = 'command_in_amps'
                self.checkButtonValues[key] = tk.IntVar()
                self.checkButtonValues[key].set(0)

                self.checkButton[key] = tk.Checkbutton(self.optionsLabelFrame[plot_type], text="COMMAND IN AMPS",
                                                       variable=self.checkButtonValues[key],
                                                       command=lambda: self.refresh_all_plots()
                                                       )
                self.checkButton[key].grid(row=3, column=1)

            # CONVERT POSITION TO DEGREES CHECKBOX
            elif plot_type == 'position':
                key = 'pos_in_deg'
                self.checkButtonValues[key] = tk.IntVar()
                self.checkButtonValues[key].set(0)

                self.checkButton[key] = tk.Checkbutton(self.optionsLabelFrame[plot_type], text="POSITION IN DEGREES",
                                                       variable=self.checkButtonValues[key],
                                                       command=lambda: self.refresh_all_plots()
                                                       )
                self.checkButton[key].grid(row=3, column=1)

            row_frame += 1

    def refresh_all_plots(self):
        if self.df is None:
            return

        x = self.df['elapsed_time(ms)']

        for plot_type in GlobalConfig.PLOT_TYPES:
            self.ax[plot_type].cla()

            self.ax[plot_type].set_title(plot_type.upper() + " vs TIME", fontsize=16)
            self.ax[plot_type].set_ylabel(plot_type, fontsize=14)
            self.ax[plot_type].set_xlabel("elapsed_time(ms)", fontsize=14)

            if plot_type == 'force':
                if self.checkButtonValues[plot_type + "_slave"].get() == 1:
                    y = self.df[plot_type]
                    self.ax[plot_type].plot(x, y, marker='x', color='blue')

            elif plot_type == 'position' and self.checkButtonValues['pos_in_deg'].get() == 1:
                self.ax[plot_type].set_ylabel("position [deg]", fontsize=14)

                if self.checkButtonValues[plot_type + "_master"].get() == 1:
                    y_master = self.df['position_master_deg']
                    self.ax[plot_type].plot(x, y_master, marker='x', color='red')

                if self.checkButtonValues[plot_type + "_slave"].get() == 1:
                    y_slave = self.df['position_slave_deg']
                    self.ax[plot_type].plot(x, y_slave, marker='x', color='blue')

            elif plot_type == 'command' and self.checkButtonValues['command_in_amps'].get() == 1:
                self.ax[plot_type].set_ylabel("command [A]", fontsize=14)

                if self.checkButtonValues[plot_type + "_master"].get() == 1:
                    y_master = self.df['command_master_amp']
                    self.ax[plot_type].plot(x, y_master, marker='x', color='red')

                if self.checkButtonValues[plot_type + "_slave"].get() == 1:
                    y_slave = self.df['command_slave_amp']
                    self.ax[plot_type].plot(x, y_slave, marker='x', color='blue')

            else:
                if self.checkButtonValues[plot_type + "_master"].get() == 1:
                    y_master = self.df[plot_type + "_master"]
                    self.ax[plot_type].plot(x, y_master, marker='x', color='red')

                if self.checkButtonValues[plot_type + "_slave"].get() == 1:
                    y_slave = self.df[plot_type + "_slave"]
                    self.ax[plot_type].plot(x, y_slave, marker='x', color='blue')

            self.savePlotButton[plot_type].config(state='normal')

        self.canvas.draw()

    def import_recording(self):
        file = tk.filedialog.askopenfilenames(initialdir=GlobalConfig.DEFAULT_DIR,
                                              initialfile="tmp",
                                              filetypes=[("All files", "*")]
                                              )
        try:
            # DESTROY THE DATA OUTPUT WINDOW IF IT ALREADY EXISTS
            if self.data_output_window is not None:
                self.data_output_window.destroy()
                self.data_output_window = None

            file_path = file[0]
            self.selectedFileText.set("FILE: " + os.path.basename(file_path))

            self.df = create_data_frame(file_path)

            # DRAW ALL PLOTS
            self.refresh_all_plots()
            self.add_time_to_save_name()

            # ACTIVATE NEW WINDOW BUTTON
            self.showFileContentWindow.config(state='normal')

        except IndexError:
            print("No file selected")

    def save_plot(self, plot_type):
        filename = self.fileNameEntry[plot_type].get()

        if plot_type == 'force':
            CommonFunctions.save_plot_force(filename, self.df)

        else:
            master = self.checkButtonValues[plot_type + "_master"].get()
            slave = self.checkButtonValues[plot_type + "_slave"].get()

            if plot_type == 'position' and self.checkButtonValues['pos_in_deg'].get() == 1:
                CommonFunctions.save_plot_special_axis(filename, self.df, plot_type, master, slave, '[deg]')

            elif plot_type == 'command' and self.checkButtonValues['command_in_amps'].get() == 1:
                CommonFunctions.save_plot_special_axis(filename, self.df, plot_type, master, slave, '[A]')

            else:
                CommonFunctions.save_plot(filename, self.df, plot_type, master, slave)

    def add_time_to_save_name(self):
        date = datetime.today().strftime('%Y-%m-%d_%H-%M')

        for plot_type in GlobalConfig.PLOT_TYPES:
            self.fileNameEntry[plot_type].delete(0, 'end')
            self.fileNameEntry[plot_type].insert(0, date + '__' + plot_type.capitalize())
