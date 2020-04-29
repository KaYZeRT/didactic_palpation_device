# import os
# import matplotlib
# import pandas as pd
# import tkinter as tk
#
# import GlobalConfig
# import CommonFunctions
#
# from FileContentWindow import *
#
# import matplotlib.pyplot as plt
#
# from datetime import datetime
# from matplotlib import style
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# from matplotlib.figure import Figure
# from tkinter import filedialog
# from functools import partial

matplotlib.use("TkAgg")
style.use("ggplot")
LARGE_FONT = ("Verdana", 12)


def create_data_frame(file_path):
    data = pd.read_csv(file_path, sep=",", header=None)
    data.columns = GlobalConfig.DATA_FRAME_COLUMNS

    data['interval(ms)'] = CommonFunctions.convert_us_to_ms(data['interval(ms)'])
    data['time(ms)'] = CommonFunctions.convert_us_to_ms(data['time(ms)'])

    data = CommonFunctions.add_elapsed_time_to_df(data)

    # CONVERT POSITION TO DEGREES (SLAVE)
    pos_slave_deg = []
    for element in data['position_slave']:
        pos_slave_deg.append(CommonFunctions.convert_position_to_degrees(element))
    data['position_slave_deg'] = pos_slave_deg

    # CONVERT POSITION TO DEGREES (MASTER)
    pos_master_deg = []
    for element in data['position_master']:
        pos_master_deg.append(CommonFunctions.convert_position_to_degrees(element))
    data['position_master_deg'] = pos_master_deg

    # CONVERT COMMAND TO AMPERES (SLAVE)
    command_slave_amp = []
    for element in data['command_slave']:
        command_slave_amp.append(CommonFunctions.convert_command_to_amps(element))
    data['command_slave_amp'] = command_slave_amp

    # CONVERT COMMAND TO AMPERES (MASTER)
    command_master_amp = []
    for element in data['command_master']:
        command_master_amp.append(CommonFunctions.convert_command_to_amps(element))
    data['command_master_amp'] = command_master_amp

    return data


class DrawPlotsFromFile(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.df = None

        # UPPER FRAME
        self.upperFrame = tk.LabelFrame(self)
        self.upperFrame.pack()

        # FRAME TITLE (IN UPPER FRAME)
        self.frameTitleLabel = tk.Label(self.upperFrame, text="DRAW PLOTS FROM FILE", font=LARGE_FONT, bg='red')
        self.frameTitleLabel.grid(row=0, column=0, padx=15, pady=5)

        # BACK TO MAIN WINDOW BUTTON (IN UPPER FRAME)
        self.backButton = tk.Button(self.upperFrame, text="BACK TO MAIN WINDOW",
                                    command=lambda: controller.show_frame("MainWindow"))
        self.backButton.grid(row=0, column=1)

        # MAIN FRAME
        self.mainLabelFrame = tk.LabelFrame(self)
        self.mainLabelFrame.pack()

        # PLOTS FRAME (IN MAIN FRAME)
        self.ax = dict()
        self.canvas = None

        self.plotsLabelFrame = tk.LabelFrame(self.mainLabelFrame)
        self.plotsLabelFrame.grid(row=1, column=0, rowspan=2)

        CommonFunctions.fill_plots_label_frame(self)

        # RIGHT SIDE FRAME (IN MAIN FRAME)
        self.rightSideLabelFrame = tk.LabelFrame(self.mainLabelFrame, text="RIGHT SIDE FRAME")
        self.rightSideLabelFrame.grid(row=1, column=1, rowspan=2, padx=10, pady=10)

        # FILE SELECTION FRAME (IN MAIN FRAME)
        self.selectFileButton = None
        self.selectedFileText = None
        self.isFileSelectedLabel = None

        self.fileSelectionLabelFrame = tk.LabelFrame(self.rightSideLabelFrame, text="FILE SELECTION FRAME",
                                                     padx=5, pady=5)
        self.fileSelectionLabelFrame.pack()

        self.fill_file_selection_label_frame()

        # GENERATE OUTPUT WINDOW BUTTON (IN RIGHT SIDE LABEL FRAME)
        self.data_output_window = None

        self.showFileContentWindow = tk.Button(self.rightSideLabelFrame, text="GENERATE OUTPUT WINDOW",
                                               width=30, height=3,
                                               state=tk.DISABLED,
                                               command=lambda: self.generate_data_output_window())
        self.showFileContentWindow.pack(pady=15)

        # PLOTS OPTIONS FRAME (IN MAIN FRAME)
        self.optionsLabelFrame = dict()
        self.plotNameLabel = dict()
        self.plotNameEntry = dict()
        self.savePlotButton = dict()
        self.checkButton = dict()
        self.checkButtonValues = dict()

        self.plotsOptionsLabelFrame = tk.LabelFrame(self.rightSideLabelFrame, text="PLOTS OPTIONS FRAME")
        self.plotsOptionsLabelFrame.pack(padx=10, pady=10)

        CommonFunctions.fill_plots_options_label_frame(self, real_time=0)

    def generate_data_output_window(self):
        try:
            if self.data_output_window.state() == "normal":
                self.data_output_window.focus()
        except:
            self.data_output_window = tk.Toplevel(self)
            FileContentWindow(self.data_output_window, self)

    def fill_file_selection_label_frame(self):
        self.selectFileButton = tk.Button(self.fileSelectionLabelFrame, text='SELECT FILE', width=30, height=3,
                                          command=lambda: self.import_recording())
        self.selectFileButton.pack()

        self.selectedFileText = tk.StringVar()
        self.selectedFileText.set('FILE: no file selected')
        self.isFileSelectedLabel = tk.Label(self.fileSelectionLabelFrame, textvariable=self.selectedFileText,
                                            pady=5)
        self.isFileSelectedLabel.pack()

    def import_recording(self):
        file = tk.filedialog.askopenfilenames(initialdir=GlobalConfig.DEFAULT_DIR,
                                              initialfile="tmp",
                                              filetypes=[("All files", "*")]
                                              )
        try:
            # DESTROY THE DATA OUTPUT WINDOW IF IT ALREADY EXISTS (WHEN CHANGING FILE)
            if self.data_output_window is not None:
                self.data_output_window.destroy()
                self.data_output_window = None

            file_path = file[0]
            self.selectedFileText.set("FILE: " + os.path.basename(file_path))

            self.df = create_data_frame(file_path)

            # DRAW ALL PLOTS
            CommonFunctions.refresh_all_plots(self, real_time=0)
            self.add_time_to_save_name()

            # ACTIVATE NEW WINDOW BUTTON
            self.showFileContentWindow.config(state='normal')

        except IndexError:
            print("No file selected")

    def add_time_to_save_name(self):
        date = datetime.today().strftime('%Y-%m-%d_%H-%M')

        for plot_type in GlobalConfig.PLOT_TYPES:
            self.plotNameEntry[plot_type].delete(0, 'end')
            self.plotNameEntry[plot_type].insert(0, date + '__' + plot_type.capitalize())
