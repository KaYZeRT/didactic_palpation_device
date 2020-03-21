import os
import pandas as pd
import tkinter as tk

from tkinter import filedialog


class Win:
    def __init__(self, root):
        """Define window for the app"""
        self.root = root
        self.root.geometry("400x300")
        self.root["bg"] = "coral"
        self.button_rename = tk.Button(self.root, text="New window",
                                       command=lambda: self.new_window(Win2)).pack()

    def new_window(self, _class):
        try:
            if self.new.state() == "normal":
                self.new.focus()
        except:
            self.new = tk.Toplevel(self.root)
            _class(self.new)


class Win2:
    def __init__(self, root):
        print(app.new.state())
        self.root = root
        self.root.geometry("300x300+200+200")
        self.root["bg"] = "navy"

        self.data = None

        self.selectedFile = 'FILE: no file selected'

        self.importRecording = tk.Button(self.root, text='SELECT FILE', padx=50, pady=20,
                                         command=lambda: self.import_recording())
        self.importRecording.grid(row=1, column=0)

        self.isFileSelectedLabel = tk.Label(self.root, text=self.selectedFile)
        self.isFileSelectedLabel.grid(row=2, column=0)

        self.myString = tk.StringVar()
        self.test = tk.Label(self.root, textvariable=self.myString)
        self.test.grid(row=3, column=0)
        self.myString.set("INITIAL SET")



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

            self.selectedFile = "FILE: " + os.path.basename(file_path)
            print(self.selectedFile)

            self.myString.set("VALUE CHANGED")



        except IndexError:
            print("No file selected")

        return 0


if __name__ == "__main__":
    root = tk.Tk()
    app = Win(root)
    app.root.title("Lezioni")
    root.mainloop()