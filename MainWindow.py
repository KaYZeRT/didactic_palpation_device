import tkinter as tk

LARGE_FONT = ("Verdana", 12)


class MainWindow(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="START PAGE", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        # self.startRecording = tk.Button(self, text='START RECORDING', width=30, height=3)
        # self.startRecording.pack()
        #
        # self.stopRecording = tk.Button(self, text='STOP RECORDING', width=30, height=3)
        # self.stopRecording.pack()
        #
        # self.exportRecording = tk.Button(self, text='EXPORT RECORDING', width=30, height=3)
        # self.exportRecording.pack()

        self.acquireData = tk.Button(self, text='ACQUIRE DATA', width=30, height=3,
                                     command=lambda: controller.show_frame("NewRecording"))
        self.acquireData.pack()

        self.plotFromFile = tk.Button(self, text='DRAW PLOTS FROM .TXT FILE', width=30, height=3,
                                      command=lambda: controller.show_frame("PlotMenu"))
        self.plotFromFile.pack()
