########################################################################################################################
# IMPORTS
########################################################################################################################

import tkinter as tk
from tkinter import messagebox

from MainPage import *
from DrawPlotsFromFile import *
from DrawPlotsRealTime import *


########################################################################################################################
# CLASS: GUI
########################################################################################################################

class GUI(tk.Tk):

    def __init__(self, *args, **kwargs):
        """
        Creates the main window. It also creates 3 pages (MainPage, DrawPlotsRealTime, DrawPlotsFromFile).
        Only one page is displayed at all time even though 3 exists.
        """
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (MainPage, DrawPlotsRealTime, DrawPlotsFromFile):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MainPage")

    def show_frame(self, page_name):
        """Displays the chosen page and hides the others."""
        frame = self.frames[page_name]
        frame.tkraise()


########################################################################################################################
# LAUNCHING APPLICATION (MAIN FUNCTION)
########################################################################################################################

def on_closing():
    """Warning box to make sure the user wants to exit the application when the red cross is pressed"""
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        app.destroy()


if __name__ == "__main__":
    """MAIN FUNCTION"""
    app = GUI()
    app.geometry(GlobalConfig.APP_GEOMETRY)
    app.title("DIDACTIC PALPATION DEVICE")

    app.protocol("WM_DELETE_WINDOW", on_closing)
    app.mainloop()
