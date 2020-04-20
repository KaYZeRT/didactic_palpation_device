import matplotlib
import matplotlib.pyplot as plt
import tkinter as tk

import GlobalConfig

from matplotlib import style
from tkinter import filedialog

matplotlib.use("TkAgg")
style.use("ggplot")


def save_plot(filename, df, plot_type):
    if filename == "":
        tk.messagebox.showerror("Error !", "Filename not defined !")
        return
    save_dir = filedialog.askdirectory(initialdir=GlobalConfig.DEFAULT_SAVE_DIR)

    try:
        x = df['elapsed_time(ms)']
        y = df[plot_type]

        plt.figure()
        plt.plot(x, y, marker='x', color='blue')
        plt.grid(True)

        plt.title(plot_type.upper() + " vs TIME")
        plt.xlabel("elapsed_time(ms)")
        plt.ylabel(plot_type)
        plt.savefig(save_dir + "/" + filename + ".png")

    except:
        tk.messagebox.showerror("Error !", "Error while saving file !")

    return


def convert_us_to_ms(column):
    res = column / 1000
    res = round(res, 0)

    return res


def add_elapsed_time_to_df(df):
    ls = [0]
    time_previous_measurement = df['time_between_measure(ms)']

    for i in range(1, df.shape[0]):
        ls.append(ls[i - 1] + time_previous_measurement[i])

    df['elapsed_time(ms)'] = ls
    return df
