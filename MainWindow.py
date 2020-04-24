import tkinter as tk

LARGE_FONT = ("Verdana", 12)


class MainWindow(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # FRAME TITLE
        label = tk.Label(self, text="MAIN WINDOW", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        self.acquireData = tk.Button(self, text='NEW RECORDING', width=30, height=3,
                                     command=lambda: controller.show_frame("NewRecordingMenu"))
        self.acquireData.pack()

        self.plotFromFile = tk.Button(self, text='DRAW PLOTS FROM .txt FILE', width=30, height=3,
                                      command=lambda: controller.show_frame("PlotMenu"))
        self.plotFromFile.pack()

        self.drawPlotsFromFile = tk.Button(self, text='DRAW PLOTS FROM FILE', width=30, height=3,
                                           command=lambda: controller.show_frame("DrawPlotsFromFile"))
        self.drawPlotsFromFile.pack()
