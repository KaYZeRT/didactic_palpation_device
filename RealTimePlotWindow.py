import pandas as pd
import tkinter as tk
import matplotlib

from matplotlib import style
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import filedialog

LARGE_FONT = ("Verdana", 12)
style.use("ggplot")

pd.set_option('display.expand_frame_repr', False)
matplotlib.use("TkAgg")


class RealTimePlotWindow(tk.Tk):

    def __init__(self, root):
        self.root = root
        self.root.title("Real Time Plot")

        # SIMULATION OF REAL TIME DATA ACQUISITION
        self.simulation_df = pd.read_csv("src/releve_vitesse_2.txt", sep=",", header=None)
        self.simulation_df.columns = ['index', 'command', 'time_since_previous_measurement(µs)', 'time(µs)', 'position',
                                      'speed']
        self.simulation_step = 1

        self.df = None
        self.continuePlotting = False

        self.savePlotButton = tk.Button(self.root, text='SAVE PLOT', padx=10)
        self.savePlotButton.pack()

        fig = Figure()
        self.ax = fig.add_subplot(111)
        self.ax.set_xlabel("X axis")
        self.ax.set_ylabel("Y axis")
        self.ax.grid(True)

        self.graph = FigureCanvasTkAgg(fig, master=root)
        self.graph.get_tk_widget().pack(side="top", fill='both', expand=True)

        b = tk.Button(root, text="Start/Stop", command=self.gui_handler, bg="red", fg="white")
        b.pack()

    def gui_handler(self):
        self.change_state()
        self.plot()

    def change_state(self):
        if self.continuePlotting:
            self.continuePlotting = False
        else:
            self.continuePlotting = True

    def plot(self):
        if self.continuePlotting:
            self.ax.cla()
            self.ax.grid()

            self.simulate_real_time_data_acquisition()
            x = self.df['index']
            y = self.df['speed']

            self.ax.plot(x, y, marker='o', color='orange')
            self.graph.draw()
            self.simulation_step += 1

            if self.simulation_step < 60:
                self.graph.get_tk_widget().after(1000, self.plot)   #NOT self.plot()

    def simulate_real_time_data_acquisition(self):
        df = self.simulation_df.iloc[:self.simulation_step, :]
        self.df = df
        return
