import matplotlib
import matplotlib.pyplot as plt
import tkinter as tk

import GlobalConfig

from matplotlib import style
from tkinter import filedialog

matplotlib.use("TkAgg")
style.use("ggplot")


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


def save_plot(filename, df, plot_type, master, slave):
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
