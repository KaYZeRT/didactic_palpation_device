import tkinter as tk

from PlotWindow import *

class MainWindow:

    def __init__(self, root):
        """Define window for the app"""
        self.root = root
        self.root.title('Didactic Palpation Device GUI')
        self.root.geometry("400x300")

        self.startRecording = tk.Button(self.root, text='START RECORDING', padx=50, pady=20)
        self.startRecording.grid(row=0, column=0)

        self.stopRecording = tk.Button(self.root, text='STOP RECORDING', padx=50, pady=20)
        self.stopRecording.grid(row=1, column=0)

        self.exportRecording = tk.Button(self.root, text='EXPORT RECORDING', padx=50, pady=20)
        self.exportRecording.grid(row=2, column=0)

        self.plotFromFile = tk.Button(self.root, text='DRAW PLOTS FROM .TXT FILE', padx=50, pady=20,
                                         command=lambda: self.new_window(PlotWindow))
        self.plotFromFile.grid(row=3, column=0)

    def new_window(self, _class):
        try:
            if self.new.state() == "normal":
                self.new.focus()
        except:
            self.new = tk.Toplevel(self.root)
            _class(self.new)