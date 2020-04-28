import tkinter as tk

import GlobalConfig

LARGE_FONT = ("Verdana", 12)


class FileContentWindow(tk.Tk):

    def __init__(self, root, parent):
        self.parent = parent

        self.root = root
        self.root.title("FILE DATA OUTPUT")
        self.root.geometry(GlobalConfig.FILE_CONTENT_WINDOW_GEOMETRY)

        # FRAME TITLE
        tk.Label(self.root, text="FILE DATA OUTPUT", font=LARGE_FONT, bg='red').pack(pady=5)

        # SELECTED FILE NAME
        tk.Label(self.root, text=self.parent.selectedFileText.get()).pack(pady=10)

        # OUTPUT FRAME (LOWER RIGHT)
        self.outputFrame = tk.LabelFrame(self.root, text="OUTPUT")
        self.outputFrame.pack(padx=10, pady=5)

        self.outputText = tk.Text(self.outputFrame,
                                  width=GlobalConfig.OUTPUT_WINDOW_WIDTH,
                                  height=GlobalConfig.OUTPUT_WINDOW_HEIGHT)
        self.outputText.pack(padx=10, pady=10)

        # PRINT FILE DATA TO OUTPUT FRAME
        self.outputText.delete(1.0, tk.END)
        string = self.parent.df.to_string(index=False, columns=GlobalConfig.DATA_FRAME_COLUMNS)
        self.outputText.insert(tk.END, string + "\n")
        # self.outputText.see("end")
