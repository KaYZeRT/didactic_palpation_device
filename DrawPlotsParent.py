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


class DrawPlotsParent(tk.Frame):

    def __init__(self, parent, controller, real_time):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller

        self.df = None
        self.real_time = real_time

        ################################################################################################################
        # UPPER FRAME (IN SELF)
        ################################################################################################################
        self.upperFrame = tk.LabelFrame(self)
        self.upperFrame.pack()

        self.frameTitleLabel = None
        self.backButton = None

        ################################################################################################################
        # MAIN FRAME (IN SELF)
        ################################################################################################################
        self.mainLabelFrame = tk.LabelFrame(self)
        self.mainLabelFrame.pack()

        # FIGURE FRAME (IN MAIN FRAME)
        self.figureLabelFrame = tk.LabelFrame(self.mainLabelFrame)
        self.figureLabelFrame.grid(row=1, column=0, rowspan=2)

        self.ax = dict()
        self.canvas = None
        self.fill_figure_label_frame()

        ################################################################################################################
        # RIGHT SIDE FRAME (IN MAIN FRAME)
        ################################################################################################################

        self.rightSideLabelFrame = tk.LabelFrame(self.mainLabelFrame, text="RIGHT SIDE FRAME")
        self.rightSideLabelFrame.grid(row=1, column=1, rowspan=2, padx=10, pady=5)

        # CREATE OUTPUT WINDOW BUTTON (IN RIGHT SIDE LABEL FRAME)
        self.data_output_window = None

        self.createOutputWindowButton = tk.Button(self.rightSideLabelFrame, text="GENERATE OUTPUT WINDOW",
                                                  width=30, height=3,
                                                  state=tk.DISABLED,
                                                  command=lambda: self.generate_data_output_window())
        self.createOutputWindowButton.grid(row=2, column=0)

        # PLOTS OPTIONS FRAME (IN MAIN FRAME)
        self.plotsOptionsLabelFrame = tk.LabelFrame(self.rightSideLabelFrame, text="PLOTS OPTIONS FRAME")

        self.optionsLabelFrame = dict()
        self.plotNameLabel = dict()
        self.plotNameEntry = dict()
        self.savePlotButton = dict()
        self.checkButton = dict()
        self.checkButtonValues = dict()
        self.plotsOptionsLabelFrame.grid(row=3, column=0)

        self.fill_plots_options_label_frame()

    def fill_upper_frame(self, frame_name):
        # FRAME TITLE (IN UPPER FRAME)
        self.frameTitleLabel = tk.Label(self.upperFrame, text="DRAW PLOTS " + frame_name, font=LARGE_FONT, bg='red')
        self.frameTitleLabel.grid(row=0, column=0, padx=15, pady=5)

        # BACK TO MAIN WINDOW BUTTON (IN UPPER FRAME)
        self.backButton = tk.Button(self.upperFrame, text="BACK TO MAIN WINDOW",
                                    command=lambda: self.controller.show_frame("MainWindow"))
        self.backButton.grid(row=0, column=1)

    def fill_figure_label_frame(self):
        f = Figure(figsize=(11, 9))

        index = 1
        for plot_type in GlobalConfig.PLOT_TYPES:
            self.ax[plot_type] = f.add_subplot(2, 2, index)
            self.ax[plot_type].set_title(plot_type.upper() + " vs TIME", fontsize=16)
            index += 1

        # DO NOT MODIFY THE LINE BELOW - PREVENTS WHITE SPACES
        f.subplots_adjust(left=0.085, right=0.98, top=0.95, bottom=0.05, wspace=0.3, hspace=0.3)

        self.canvas = FigureCanvasTkAgg(f, master=self.figureLabelFrame)
        self.canvas.get_tk_widget().pack()
        self.canvas.draw()

    def fill_plots_options_label_frame(self):
        row_frame = 0
        column_frame = 0
        for plot_type in GlobalConfig.PLOT_TYPES:
            self.optionsLabelFrame[plot_type] = tk.LabelFrame(self.plotsOptionsLabelFrame, padx=15, pady=5,
                                                              text=plot_type.upper())
            self.optionsLabelFrame[plot_type].grid(row=row_frame, column=column_frame, padx=10, pady=5)

            # FILE NAME LABEL
            self.plotNameLabel[plot_type] = tk.Label(self.optionsLabelFrame[plot_type],
                                                     text="FILENAME:")
            self.plotNameLabel[plot_type].grid(row=0, column=0, padx=10)

            # FILE NAME TEXT FIELD
            self.plotNameEntry[plot_type] = tk.Entry(self.optionsLabelFrame[plot_type], borderwidth=3, width=40)
            self.plotNameEntry[plot_type].grid(row=0, column=1)
            self.plotNameEntry[plot_type].insert(0, plot_type.capitalize())

            # SAVE BUTTON
            self.savePlotButton[plot_type] = tk.Button(self.optionsLabelFrame[plot_type], text='SAVE PLOT',
                                                       width=10, height=1,
                                                       state=tk.DISABLED,
                                                       # partial(function, attribute1 attribute2)
                                                       command=partial(self.save_plot, plot_type)
                                                       )
            self.savePlotButton[plot_type].grid(row=0, column=2, padx=10)

            # MASTER AND SLAVE CHECKBOX
            keys = [plot_type + "_slave", plot_type + "_master"]
            text = ["SLAVE", "MASTER"]
            color = ["blue", "red"]
            row = 1
            for key in keys:
                # MASTER AND SLAVE CHECK BUTTONS (NOT CREATED FOR FORCE_MASTER SUBPLOT)
                if key != 'force_master':
                    self.create_check_button(key=key, init_value=1, plot_type=plot_type, text=text[row - 1],
                                             color=color[row - 1])
                    # No need to return a value as the checkButton[key] is added to a dict()
                    self.checkButton[key].grid(row=row, column=1)
                    row += 1

            # CONVERT COMMAND TO AMPERES CHECKBOX
            if plot_type == 'command':
                key = 'command_in_amps'
                self.create_check_button(key=key, init_value=0, plot_type=plot_type, text="COMMAND IN AMPS",
                                         color='black')
                self.checkButton[key].grid(row=3, column=1)

            # CONVERT POSITION TO DEGREES CHECKBOX
            if plot_type == 'position':
                key = 'pos_in_deg'
                self.create_check_button(key=key, init_value=0, plot_type=plot_type, text="POSITION IN DEGREES",
                                         color='black')
                self.checkButton[key].grid(row=3, column=1)

            row_frame += 1

    def create_check_button(self, key, init_value, plot_type, text, color):
        self.checkButtonValues[key] = tk.IntVar()
        self.checkButtonValues[key].set(init_value)

        if self.real_time == 0:
            self.checkButton[key] = tk.Checkbutton(self.optionsLabelFrame[plot_type], text=text,
                                                   variable=self.checkButtonValues[key],
                                                   command=lambda: self.refresh_all_plots(),
                                                   fg=color
                                                   )
        else:
            # DO NOT MAP A COMMAND FOR THE REAL TIME PLOTTING (BECAUSE REFRESH IS ALREADY HAPPENING)
            self.checkButton[key] = tk.Checkbutton(self.optionsLabelFrame[plot_type], text=text,
                                                   variable=self.checkButtonValues[key],
                                                   fg=color
                                                   )

    def clear_all_plots(self):
        for plot_type in GlobalConfig.PLOT_TYPES:
            self.ax[plot_type].cla()
            self.ax[plot_type].set_title(plot_type.upper() + " vs TIME", fontsize=16)
            self.ax[plot_type].set_ylabel(plot_type, fontsize=14)
            self.ax[plot_type].set_xlabel("elapsed_time(ms)", fontsize=14)
        self.canvas.draw()


    def refresh_all_plots(self):
        if self.df is not None:
            if self.df.empty is False:

                for plot_type in GlobalConfig.PLOT_TYPES:
                    self.ax[plot_type].cla()

                    self.ax[plot_type].set_title(plot_type.upper() + " vs TIME", fontsize=16)
                    self.ax[plot_type].set_ylabel(plot_type, fontsize=14)
                    self.ax[plot_type].set_xlabel("elapsed_time(ms)", fontsize=14)

                    if plot_type == 'force':
                        if self.checkButtonValues[plot_type + "_slave"].get() == 1:
                            x = self.df['elapsed_time(ms)']
                            y = self.df[plot_type]
                            self.ax[plot_type].plot(x, y, marker='x', color='blue')

                    elif plot_type == 'position' and self.checkButtonValues['pos_in_deg'].get() == 1:
                        self.ax[plot_type].set_ylabel("position [deg]", fontsize=14)

                        if self.checkButtonValues[plot_type + "_master"].get() == 1:
                            x = self.df['elapsed_time(ms)']
                            y_master = self.df['position_master_deg']
                            self.ax[plot_type].plot(x, y_master, marker='x', color='red')

                        if self.checkButtonValues[plot_type + "_slave"].get() == 1:
                            x = self.df['elapsed_time(ms)']
                            y_slave = self.df['position_slave_deg']
                            self.ax[plot_type].plot(x, y_slave, marker='x', color='blue')

                    elif plot_type == 'command' and self.checkButtonValues['command_in_amps'].get() == 1:
                        self.ax[plot_type].set_ylabel("command [A]", fontsize=14)

                        if self.checkButtonValues[plot_type + "_master"].get() == 1:
                            x = self.df['elapsed_time(ms)']
                            y_master = self.df['command_master_amps']
                            self.ax[plot_type].plot(x, y_master, marker='x', color='red')

                        if self.checkButtonValues[plot_type + "_slave"].get() == 1:
                            x = self.df['elapsed_time(ms)']
                            y_slave = self.df['command_slave_amps']
                            self.ax[plot_type].plot(x, y_slave, marker='x', color='blue')

                    else:
                        if self.checkButtonValues[plot_type + "_master"].get() == 1:
                            x = self.df['elapsed_time(ms)']
                            y_master = self.df[plot_type + "_master"]
                            self.ax[plot_type].plot(x, y_master, marker='x', color='red')

                        if self.checkButtonValues[plot_type + "_slave"].get() == 1:
                            x = self.df['elapsed_time(ms)']
                            y_slave = self.df[plot_type + "_slave"]
                            self.ax[plot_type].plot(x, y_slave, marker='x', color='blue')

        self.canvas.draw()

        if self.real_time == 1:
            if self.isRecording:
                self.canvas.get_tk_widget().after(GlobalConfig.PLOTTING_FREQUENCY,
                                                  lambda: self.refresh_all_plots())
            else:
                self.activate_save_plot_buttons()

        if self.df is not None and self.real_time != 1:
            self.activate_save_plot_buttons()

    def activate_save_plot_buttons(self):
        for plot_type in GlobalConfig.PLOT_TYPES:
            self.savePlotButton[plot_type].config(state='normal')

    def save_plot(self, plot_type):
        filename = self.plotNameEntry[plot_type].get()

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
                CommonFunctions.save_plot_normal_axis(filename, self.df, plot_type, master, slave)

    def generate_data_output_window(self):
        try:
            if self.data_output_window.state() == "normal":
                self.data_output_window.focus()
        except:
            self.data_output_window = tk.Toplevel(self)
            FileContentWindow(self.data_output_window, self)

