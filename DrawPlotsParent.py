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

class DrawPlotsParent:

    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller

        self.df = None

        self.upperFrame = tk.LabelFrame(self)
        self.upperFrame.pack()

        self.frameTitleLabel = None
        self.backButton = None

    def fill_upper_frame(self, frame_name):
        # FRAME TITLE (IN UPPER FRAME)
        self.frameTitleLabel = tk.Label(self.upperFrame, text="DRAW PLOTS REAL TIME", font=LARGE_FONT, bg='red')
        self.frameTitleLabel.grid(row=0, column=0, padx=15, pady=5)

        # BACK TO MAIN WINDOW BUTTON (IN UPPER FRAME)
        self.backButton = tk.Button(self.upperFrame, text="BACK TO MAIN WINDOW",
                                    command=lambda: self.controller.show_frame("MainWindow"))
        self.backButton.grid(row=0, column=1)
