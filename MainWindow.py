########################################################################################################################
# IMPORTS
########################################################################################################################

import tkinter as tk

LARGE_FONT = ("Verdana", 12)


########################################################################################################################
# CLASS: MAIN WINDOW
########################################################################################################################

class MainWindow(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # FRAME TITLE
        label = tk.Label(self, text="MAIN WINDOW", font=LARGE_FONT, bg='red')
        label.pack(pady=10, padx=10)

        self.drawPlotsRealTime = tk.Button(self, text='DRAW PLOTS REAL TIME', width=30, height=3,
                                           command=lambda: controller.show_frame("DrawPlotsRealTime"))
        self.drawPlotsRealTime.pack()

        self.drawPlotsFromFile = tk.Button(self, text='DRAW PLOTS FROM FILE', width=30, height=3,
                                           command=lambda: controller.show_frame("DrawPlotsFromFile"))
        self.drawPlotsFromFile.pack()

