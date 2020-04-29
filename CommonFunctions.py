import matplotlib
import matplotlib.pyplot as plt
import tkinter as tk

import GlobalConfig

from matplotlib import style
from tkinter import filedialog

from datetime import datetime
from functools import partial
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from FileContentWindow import *

matplotlib.use("TkAgg")
style.use("ggplot")


def save_plot(self, plot_type):
    filename = self.plotNameEntry[plot_type].get()

    if plot_type == 'force':
        save_plot_force(filename, self.df)

    else:
        master = self.checkButtonValues[plot_type + "_master"].get()
        slave = self.checkButtonValues[plot_type + "_slave"].get()

        if plot_type == 'position' and self.checkButtonValues['pos_in_deg'].get() == 1:
            save_plot_special_axis(filename, self.df, plot_type, master, slave, '[deg]')

        elif plot_type == 'command' and self.checkButtonValues['command_in_amps'].get() == 1:
            save_plot_special_axis(filename, self.df, plot_type, master, slave, '[A]')

        else:
            save_plot_normal_axis(filename, self.df, plot_type, master, slave)


def save_plot_force(filename, df):
    if filename == "":
        tk.messagebox.showerror("Error !", "Filename not defined !")
        return
    save_dir = filedialog.askdirectory(initialdir=GlobalConfig.DEFAULT_SAVE_DIR)

    try:
        x = df['elapsed_time(ms)']
        y = df['force']

        plt.figure()
        plt.plot(x, y, label='slave', marker='x', color='blue')
        plt.grid(True)

        plt.title("FORCE vs TIME")
        plt.xlabel("elapsed_time(ms)")
        plt.ylabel('force')
        plt.legend()
        plt.savefig(save_dir + "/" + filename + ".png")

    except:
        tk.messagebox.showerror("Error !", "Error while saving file !")

    return


def save_plot_normal_axis(filename, df, plot_type, master, slave):
    if filename == "":
        tk.messagebox.showerror("Error !", "Filename not defined !")
        return
    save_dir = filedialog.askdirectory(initialdir=GlobalConfig.DEFAULT_SAVE_DIR)

    try:
        x = df['elapsed_time(ms)']

        plt.figure()

        if master == 1:
            y_master = df[plot_type + "_master"]
            plt.plot(x, y_master, label='master', marker='x', color='red')

        if slave == 1:
            y_slave = df[plot_type + "_slave"]
            plt.plot(x, y_slave, label='slave', marker='x', color='blue')

        plt.grid(True)

        plt.title(plot_type.upper() + " vs TIME")
        plt.xlabel("elapsed_time(ms)")
        plt.ylabel(plot_type)
        plt.legend()
        plt.savefig(save_dir + "/" + filename + ".png")

    except:
        tk.messagebox.showerror("Error !", "Error while saving file !")

    return


def save_plot_special_axis(filename, df, plot_type, master, slave, units):
    if filename == "":
        tk.messagebox.showerror("Error !", "Filename not defined !")
        return
    save_dir = filedialog.askdirectory(initialdir=GlobalConfig.DEFAULT_SAVE_DIR)

    try:
        x = df['elapsed_time(ms)']

        plt.figure()

        if master == 1:
            if plot_type == 'command':
                y_master = df[plot_type + "_master_amp"]
            elif plot_type == 'position':
                y_master = df[plot_type + "_master_deg"]

            plt.plot(x, y_master, label='master', marker='x', color='red')

        if slave == 1:
            if plot_type == 'command':
                y_slave = df[plot_type + "_slave_amp"]
            elif plot_type == 'position':
                y_slave = df[plot_type + "_slave_deg"]

            plt.plot(x, y_slave, label='slave', marker='x', color='blue')

        plt.grid(True)

        plt.title(plot_type.upper() + " vs TIME")
        plt.xlabel("elapsed_time(ms)")
        plt.ylabel(plot_type + units)
        plt.legend()
        plt.savefig(save_dir + "/" + filename + ".png")

    except:
        tk.messagebox.showerror("Error !", "Error while saving file !")

    return


def convert_us_to_ms(column):
    res = column / 1000
    res = round(res, 0)
    res = [int(i) for i in res]

    return res


def convert_position_to_degrees(element):
    return element * 360 / 1024


def convert_command_to_amps(element):
    return (element - 2048) / 1023


def add_elapsed_time_to_df(df):
    ls = [0]
    time_previous_measurement = df['interval(ms)']

    for i in range(1, df.shape[0]):
        ls.append(ls[i - 1] + time_previous_measurement[i])

    df['elapsed_time(ms)'] = ls
    return df


########################################################################################################################

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


def fill_plots_options_label_frame(self, real_time):
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
                                                   command=partial(save_plot, self, plot_type)
                                                   )
        self.savePlotButton[plot_type].grid(row=0, column=2, padx=10)

        # MASTER CHECK BUTTON
        key = plot_type + "_master"
        if key != 'force_master':
            # THE FORCE IS ONLY MEASURED FOR THE SLAVE
            self.checkButtonValues[key] = tk.IntVar()
            self.checkButtonValues[key].set(1)

            self.checkButton[key] = tk.Checkbutton(self.optionsLabelFrame[plot_type], text="MASTER",
                                                   variable=self.checkButtonValues[key],
                                                   command=lambda: refresh_all_plots(self, real_time),
                                                   fg='red'
                                                   )
            self.checkButton[key].grid(row=1, column=1)

        # SLAVE CHECK BUTTON
        key = plot_type + "_slave"
        self.checkButtonValues[key] = tk.IntVar()
        self.checkButtonValues[key].set(1)

        self.checkButton[key] = tk.Checkbutton(self.optionsLabelFrame[plot_type], text="SLAVE",
                                               variable=self.checkButtonValues[key],
                                               command=lambda: refresh_all_plots(self, real_time),
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
                                                   command=lambda: refresh_all_plots(self, real_time)
                                                   )
            self.checkButton[key].grid(row=3, column=1)

        # CONVERT POSITION TO DEGREES CHECKBOX
        elif plot_type == 'position':
            key = 'pos_in_deg'
            self.checkButtonValues[key] = tk.IntVar()
            self.checkButtonValues[key].set(0)

            self.checkButton[key] = tk.Checkbutton(self.optionsLabelFrame[plot_type], text="POSITION IN DEGREES",
                                                   variable=self.checkButtonValues[key],
                                                   command=lambda: refresh_all_plots(self, real_time)
                                                   )
            self.checkButton[key].grid(row=3, column=1)

        row_frame += 1


def add_time_to_save_name(self):
    date = datetime.today().strftime('%Y-%m-%d_%H-%M')

    for plot_type in GlobalConfig.PLOT_TYPES:
        self.plotNameEntry[plot_type].delete(0, 'end')
        self.plotNameEntry[plot_type].insert(0, date + '__' + plot_type.capitalize())


def generate_data_output_window(self):
    try:
        if self.data_output_window.state() == "normal":
            self.data_output_window.focus()
    except:
        self.data_output_window = tk.Toplevel(self)
        FileContentWindow(self.data_output_window, self)


def refresh_all_plots(self, real_time):
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
                        y_master = self.df['command_master_amp']
                        self.ax[plot_type].plot(x, y_master, marker='x', color='red')

                    if self.checkButtonValues[plot_type + "_slave"].get() == 1:
                        x = self.df['elapsed_time(ms)']
                        y_slave = self.df['command_slave_amp']
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

    if real_time == 1:
        if self.isRecording:
            self.canvas.get_tk_widget().after(GlobalConfig.PLOTTING_FREQUENCY,
                                              lambda: refresh_all_plots(self, real_time))
        else:
            activate_save_plot_buttons(self)

    if self.df is not None and real_time != 1:
        activate_save_plot_buttons(self)


def activate_save_plot_buttons(self):
    for plot_type in GlobalConfig.PLOT_TYPES:
        self.savePlotButton[plot_type].config(state='normal')
