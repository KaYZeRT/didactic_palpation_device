from PlotMenu import *


class MainWindow:

    def __init__(self, root):
        """Define window for the app"""
        self.root = root
        self.root.title('Didactic Palpation Device GUI')
        self.root.geometry("400x400")

        self.startRecording = tk.Button(self.root, text='START RECORDING', width=30, height=5)
        self.startRecording.pack()

        self.stopRecording = tk.Button(self.root, text='STOP RECORDING', width=30, height=5)
        self.stopRecording.pack()

        self.exportRecording = tk.Button(self.root, text='EXPORT RECORDING', width=30, height=5)
        self.exportRecording.pack()

        self.plotFromFile = tk.Button(self.root, text='DRAW PLOTS FROM .TXT FILE', width=30, height=5,
                                         command=lambda: self.new_window(PlotMenu))
        self.plotFromFile.pack()

    def new_window(self, _class):
        try:
            if self.new.state() == "normal":
                self.new.focus()
        except:
            self.new = tk.Toplevel(self.root)
            _class(self.new)