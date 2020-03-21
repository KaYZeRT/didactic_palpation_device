import os
import pandas as pd
import tkinter as tk

from tkinter import filedialog


class PlotWindow:
    def __init__(self, root):
        self.root = root
        self.root.title('Plot Window')
        self.root.geometry("400x300")

        self.data = None

        self.importRecording = tk.Button(self.root, text='SELECT FILE', padx=50, pady=20,
                                         command=lambda: self.import_recording())
        self.importRecording.grid(row=1, column=0)

        self.selectedFile = tk.StringVar()
        self.selectedFile.set( 'FILE: no file selected' )
        self.isFileSelectedLabel = tk.Label(self.root, textvariable=self.selectedFile)
        self.isFileSelectedLabel.grid(row=2, column=0)

    def import_recording(self):
        file = filedialog.askopenfilenames(parent=self.root,
                                           initialdir="C:/Thomas_Data/GitHub/didactic_palpation_device/src",
                                           initialfile="tmp",
                                           filetypes=[("All files", "*")]
                                           )
        print(file)
        try:
            file_path = file[0]
            print("SELECTED FILE:", file_path)
            data = pd.read_csv(file_path, sep=",", header=None)
            data.columns = ['index', 'command', 'elapsed_time_(µs)', 'time_(µs)', 'position', 'speed']
            print(data.head(10))
            self.data = data

            self.selectedFile.set( "FILE: " + os.path.basename(file_path) )
            print(self.selectedFile.get())

        except IndexError:
            print("No file selected")

        return 0
