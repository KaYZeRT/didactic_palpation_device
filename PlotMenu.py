import os

from PlotWindow import *

pd.set_option('display.expand_frame_repr', False)


def time_calculation(df):
    ls = [0]
    time_previous_measurement = df['time_since_previous_measurement(µs)']

    for i in range(1, df.shape[0]):
        ls.append(ls[i - 1] + time_previous_measurement[i])

    df['elapsed_time(µs)'] = ls
    return df


def create_data_frame(file_path):
    data = pd.read_csv(file_path, sep=",", header=None)
    data.columns = ['index', 'command', 'time_since_previous_measurement(µs)', 'time(µs)', 'position', 'speed']

    data = time_calculation(data)

    data = data[['index', 'time(µs)', 'elapsed_time(µs)', 'time_since_previous_measurement(µs)', 'command', 'position',
                 'speed']]

    return data


class PlotMenu:
    def __init__(self, root):
        self.root = root
        self.root.title('Plot Menu')
        self.root.geometry("400x500")

        self.df = None

        self.fileFrame = tk.LabelFrame(self.root, text="FILE BOX", padx=5, pady=5)
        self.fileFrame.pack(padx=10, pady=10)

        self.importRecording = tk.Button(self.fileFrame, text='SELECT FILE', width=30, height=5,
                                         command=lambda: self.import_recording())
        self.importRecording.pack()

        self.selectedFile = tk.StringVar()
        self.selectedFile.set('FILE: no file selected')
        self.isFileSelectedLabel = tk.Label(self.fileFrame, textvariable=self.selectedFile)
        self.isFileSelectedLabel.pack()

        self.generatePlotFrame = tk.LabelFrame(self.root, text="GENERATE PLOTS BOX", padx=5, pady=5)
        self.generatePlotFrame.pack(padx=10, pady=10)

        self.generateCommandPlot = tk.Button(self.generatePlotFrame, text='GENERATE COMMAND PLOT', state=tk.DISABLED,
                                             width=30, height=5, command=lambda: self.new_window(PlotWindow, 'command'))
        self.generateCommandPlot.pack()

        self.generatePositionPlot = tk.Button(self.generatePlotFrame, text='GENERATE POSITION PLOT', state=tk.DISABLED,
                                              width=30, height=5, command=lambda: self.new_window(PlotWindow, 'position'))
        self.generatePositionPlot.pack()

        self.generateSpeedPlot = tk.Button(self.generatePlotFrame, text='GENERATE SPEED PLOT', state=tk.DISABLED,
                                           width=30, height=5, command=lambda: self.new_window(PlotWindow, 'speed'))
        self.generateSpeedPlot.pack()

    def import_recording(self):
        file = filedialog.askopenfilenames(parent=self.root,
                                           initialdir="C:/Thomas_Data/GitHub/didactic_palpation_device/src",
                                           initialfile="tmp",
                                           filetypes=[("All files", "*")]
                                           )
        print(file)
        try:
            file_path = file[0]
            self.selectedFile.set("FILE: " + os.path.basename(file_path))

            self.df = create_data_frame(file_path)
            self.enable_buttons()


            print("SELECTED FILE:", file_path)
            print(self.df.head(10))
            print(self.selectedFile.get())

            # self.plot(self.df, 'command')

        except IndexError:
            print("No file selected")

        return 0

    def enable_buttons(self):
        self.generateCommandPlot.config(state="normal")
        self.generatePositionPlot.config(state="normal")
        self.generateSpeedPlot.config(state="normal")

        return 0

    def new_window(self, _class, plot_type):
        # try:
        #     if self.new.state() == "normal":
        #         self.new.focus()
        # except:
        #     self.new = tk.Toplevel(self.root)
        #     _class(self.new, self.df, plot_type)
        self.new = tk.Toplevel(self.root)
        _class(self.new, self.df, plot_type)

