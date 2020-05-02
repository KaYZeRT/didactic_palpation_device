########################################################################################################################
# IMPORTS
########################################################################################################################

import os
import pandas as pd
import tkinter as tk
from datetime import datetime

import GlobalConfig

from DataOutputWindow import *

import matplotlib
import matplotlib.pyplot as plt
from matplotlib import style
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from tkinter import filedialog
from functools import partial

matplotlib.use("TkAgg")
style.use("ggplot")
LARGE_FONT = ("Verdana", 12)


########################################################################################################################
# STATIC FUNCTIONS
########################################################################################################################

def convert_us_to_ms(element):
    """Converts microseconds to milliseconds"""
    res = element / 1000
    res = round(res, 0)

    return int(res)


def convert_position_to_degrees(element):
    """Converts position to degrees (360°=1024)"""
    return element * 360 / 1024


def convert_command_to_amps(element):
    """
    Converts command to amperes
    Command varies from 0  (=-2A) to 4095 (=2A)
    """
    return (element - 2048) / 1023


########################################################################################################################
# CLASS: DRAW PLOTS PARENT
########################################################################################################################


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
        self.fill_upper_frame()

        ################################################################################################################
        # MAIN FRAME (IN SELF)
        ################################################################################################################
        self.mainLabelFrame = tk.LabelFrame(self)
        self.mainLabelFrame.pack()

        ################################################################################################################
        # FIGURE FRAME (IN MAIN FRAME)
        ################################################################################################################
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

        ################################################################################################################
        # WINDOW SPECIFIC FRAME (IN RIGHT SIDE FRAME)
        ################################################################################################################
        """THIS IS WHERE THE OPTIONS/BUTTONS/ENTRIES WHICH ARE SPECIFIC TO THE WINDOW TYPE (PLOT FROM FILE OR 
        PLOT REAL TIME WILL BE CREATED"""
        self.windowSpecificLabelFrame = tk.LabelFrame(self.rightSideLabelFrame, text="WINDOW SPECIFIC FRAME")
        self.windowSpecificLabelFrame.grid(row=0, column=0)

        ################################################################################################################
        # DATA OUTPUT WINDOW BUTTON (IN RIGHT SIDE FRAME)
        ################################################################################################################
        self.data_output_window = None

        self.createOutputWindowButton = tk.Button(self.rightSideLabelFrame, text="GENERATE OUTPUT WINDOW",
                                                  width=30, height=1,
                                                  state=tk.DISABLED,
                                                  command=lambda: self.generate_data_output_window())
        self.createOutputWindowButton.grid(row=1, column=0, pady=5)

        ################################################################################################################
        # PLOTS OPTIONS FRAME (IN RIGHT SIDE FRAME)
        ################################################################################################################
        self.plotsOptionsLabelFrame = tk.LabelFrame(self.rightSideLabelFrame, text="PLOTS OPTIONS FRAME")

        self.optionsLabelFrame = dict()
        self.plotNameLabel = dict()
        self.plotNameEntry = dict()
        self.savePlotButton = dict()
        self.checkButton = dict()
        self.checkButtonValues = dict()
        self.plotsOptionsLabelFrame.grid(row=2, column=0)

        self.fill_plots_options_label_frame()

        ################################################################################################################
        # END OF __INIT__
        ################################################################################################################

    def fill_upper_frame(self):
        """Fills the upperFrame with the name of the frame and adds a back button to return to the Main Page"""
        # FRAME TITLE (IN UPPER FRAME)
        if self.real_time == 0:
            frame_name = "FROM FILE"
        else:
            frame_name = "REAL TIME"
        self.frameTitleLabel = tk.Label(self.upperFrame, text="DRAW PLOTS " + frame_name, font=LARGE_FONT, bg='red')
        self.frameTitleLabel.grid(row=0, column=0, padx=15, pady=5)

        # BACK TO MAIN WINDOW BUTTON (IN UPPER FRAME)
        self.backButton = tk.Button(self.upperFrame, text="BACK TO MAIN WINDOW",
                                    command=lambda: self.controller.show_frame("MainPage"))
        self.backButton.grid(row=0, column=1)

    def fill_figure_label_frame(self):
        """
        Fills the figureLabelFrame with 1 figure containing 4 subplots (the ones defined in GlobalConfig.PLOT_TYPES)
        Each subplot is added to the self.ax dictionary so it can be easily refreshed using refresh_all_plots(self)
        """
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
        """
        Fills the plotsOptionsLabelFrame with 4 sub-frames: one for each plot (command, force, position and speed).
        Each sub-frame has the options needed by the plot: whether to show only the master or slave curve (if both
        curves are provided - not the case for the force) and whether to show the command in amperes or the position in
        degrees.
        """
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
        """
        Creates a check button.
        If real_time=0: we need to manually refresh the plots with a command to take into account the changes
        If real_time=1: we do not need to refresh the plots with a command as they will be automatically refreshed
        (see the end of the refresh_all_plots method)
        """
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
        """Clears all plots but conserves the title and the name of the X and Y axis"""
        for plot_type in GlobalConfig.PLOT_TYPES:
            self.ax[plot_type].cla()
            self.ax[plot_type].set_title(plot_type.upper() + " vs TIME", fontsize=16)
            self.ax[plot_type].set_ylabel(plot_type, fontsize=14)
            self.ax[plot_type].set_xlabel("elapsed_time(ms)", fontsize=14)
        self.canvas.draw()

    def refresh_all_plots(self):
        """
        Refreshes all plots and takes into account whether only the master or slave curve must be plotted.
        Also takes into account whether the user wants to display the command in amperes or the position in degrees.
        If real time plotting is used, the function will be repeated every GlobalConfig.PLOTTING_FREQUENCY milliseconds.
        When all plots are generated (and the data acquisition is finished), activates the save plot button.
        """
        if self.df is not None:
            if self.df.empty is False:

                for plot_type in GlobalConfig.PLOT_TYPES:
                    self.ax[plot_type].cla()

                    self.ax[plot_type].set_title(plot_type.upper() + " vs TIME", fontsize=16)
                    self.ax[plot_type].set_ylabel(plot_type, fontsize=14)
                    self.ax[plot_type].set_xlabel("elapsed_time(ms)", fontsize=14)

                    if plot_type == 'position' and self.checkButtonValues['pos_in_deg'].get() == 1:
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
                        if plot_type != 'force':
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
                self.activate_or_deactivate_save_plot_buttons('normal')

        if self.df is not None and self.real_time != 1:
            self.activate_or_deactivate_save_plot_buttons('normal')

    def activate_or_deactivate_save_plot_buttons(self, state):
        """Enables all save plot buttons (which are initiated as disabled)"""
        for plot_type in GlobalConfig.PLOT_TYPES:
            self.savePlotButton[plot_type].config(state=state)

    def generate_data_output_window(self):
        """
        Generates a new WINDOW (not frame) of type DataOutputWindow and prevents the creation of multiple windows
        (if it already exists, it will place the window on top).
        """
        try:
            if self.data_output_window.state() == "normal":
                self.data_output_window.focus()
        except:
            self.data_output_window = tk.Toplevel(self)
            DataOutputWindow(self.data_output_window, self)

    def destroy_data_output_window(self):
        """Destroys the DataOutputWindow if it exists"""
        if self.data_output_window is not None:
            self.data_output_window.destroy()
            self.data_output_window = None

    def add_date_to_save_name_entries(self):
        """
        When the recording stops or the plots are generated from a file, it adds the time (YYYY-MM-DD_HH-MM)
        to the Entry boxes in order to prevent erasing a file which is already on disk.
        """
        date = datetime.today().strftime('%Y-%m-%d_%H-%M')

        for plot_type in GlobalConfig.PLOT_TYPES:
            self.plotNameEntry[plot_type].delete(0, 'end')
            self.plotNameEntry[plot_type].insert(0, date + '__' + plot_type.capitalize())

        if self.real_time == 1:
            self.filenameEntry.delete(0, 'end')
            self.filenameEntry.insert(0, date + '__Data')

################################################################################################################
# SAVE PLOT FUNCTIONS
################################################################################################################

    def save_plot(self, plot_type):
        """
        This function is called when the save plot button is pressed.
        It calls the appropriate function in order to save the plot (normal_axis or special_axis).
        This is due to the fact that the Y axis requires a different column from the data frame (df).
        """

        if plot_type == 'position' and self.checkButtonValues['pos_in_deg'].get() == 1:
            self.save_plot_special_axis(plot_type)

        elif plot_type == 'command' and self.checkButtonValues['command_in_amps'].get() == 1:
            self.save_plot_special_axis(plot_type)

        else:
            self.save_plot_normal_axis(plot_type)

    def save_plot_normal_axis(self, plot_type):
        """
        Saves the plot using the plot name typed in the entry box.
        Takes into account whether only the master or slave curve must be plotted.
        """
        filename = self.plotNameEntry[plot_type].get()
        if filename == "":
            tk.messagebox.showerror("Error !", "Filename not defined !")
            return
        save_dir = filedialog.askdirectory(initialdir=GlobalConfig.DEFAULT_SAVE_DIR)

        try:
            x = self.df['elapsed_time(ms)']
            plt.figure()

            if plot_type != 'force':
                master = self.checkButtonValues[plot_type + "_master"].get()
                if master == 1:
                    y_master = self.df[plot_type + "_master"]
                    plt.plot(x, y_master, label='master', marker='x', color='red')

            slave = self.checkButtonValues[plot_type + "_slave"].get()
            if slave == 1:
                y_slave = self.df[plot_type + "_slave"]
                plt.plot(x, y_slave, label='slave', marker='x', color='blue')

            plt.grid(True)

            plt.title(plot_type.upper() + " vs TIME")
            plt.xlabel("elapsed_time(ms)")
            plt.ylabel(plot_type)
            plt.legend()
            plt.savefig(save_dir + "/" + filename + ".png")

        except:
            tk.messagebox.showerror("Error !", "Error while saving file !")

    def save_plot_special_axis(self, plot_type):
        """
        Only used to save the command or position plots.
        The command will be saved in amperes and the position will be saved in degrees.
        Saves the plot using the plot name typed in the entry box.
        Takes into account whether only the master or slave curve must be plotted.
        """
        filename = self.plotNameEntry[plot_type].get()
        if filename == "":
            tk.messagebox.showerror("Error !", "Filename not defined !")
            return
        save_dir = filedialog.askdirectory(initialdir=GlobalConfig.DEFAULT_SAVE_DIR)

        if plot_type == 'position':
            units = '[deg]'
        else:
            units = '[A]'

        try:
            x = self.df['elapsed_time(ms)']

            plt.figure()

            master = self.checkButtonValues[plot_type + "_master"].get()
            if master == 1:
                if plot_type == 'command':
                    y_master = self.df[plot_type + "_master_amps"]
                elif plot_type == 'position':
                    y_master = self.df[plot_type + "_master_deg"]

                plt.plot(x, y_master, label='master', marker='x', color='red')

            slave = self.checkButtonValues[plot_type + "_slave"].get()
            if slave == 1:
                if plot_type == 'command':
                    y_slave = self.df[plot_type + "_slave_amps"]
                elif plot_type == 'position':
                    y_slave = self.df[plot_type + "_slave_deg"]

                plt.plot(x, y_slave, label='slave', marker='x', color='blue')

            plt.grid(True)

            plt.title(plot_type.upper() + " vs TIME")
            plt.xlabel("elapsed_time(ms)")
            plt.ylabel(plot_type + units)
            plt.legend()
            plt.savefig(save_dir + "/" + filename + ".png")

        except:
            tk.messagebox.showerror("Error !", "Error while saving file !")
