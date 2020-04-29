import matplotlib

import GlobalConfig
import CommonFunctions

from FileContentWindow import *
from DrawPlotsParent import *

from datetime import datetime
from matplotlib import style
from tkinter import filedialog

matplotlib.use("TkAgg")
style.use("ggplot")
LARGE_FONT = ("Verdana", 12)


def create_data_frame(file_path):
    data = pd.read_csv(file_path, sep=",", header=None)
    data.columns = GlobalConfig.DATA_FRAME_COLUMNS

    # CONVERT INTERVAL FROM µs TO ms
    interval_ms = []
    for element in data['interval(ms)']:
        interval_ms.append(CommonFunctions.convert_us_to_ms(element))
    data['interval(ms)'] = interval_ms

    # CONVERT TIME FROM µs TO ms
    time_ms = []
    for element in data['time(ms)']:
        time_ms.append(CommonFunctions.convert_us_to_ms(element))
    data['time(ms)'] = time_ms

    # ADD ELAPSED TIME TO DF
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


class DrawPlotsFromFile(DrawPlotsParent):

    def __init__(self, parent, controller):

        super().__init__(parent, controller, real_time=0)
        self.fill_upper_frame("FROM FILE")

        ################################################################################################################
        # FILE SELECTION FRAME (IN MAIN FRAME)
        ################################################################################################################

        self.fileSelectionLabelFrame = tk.LabelFrame(self.rightSideLabelFrame, text="FILE SELECTION FRAME",
                                                     padx=5, pady=5)
        self.fileSelectionLabelFrame.grid(row=0, column=0)

        self.selectFileButton = None
        self.selectedFileText = None
        self.isFileSelectedLabel = None
        self.fill_file_selection_label_frame()

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
            self.refresh_all_plots()

            # ADD THE DATE AND TIME TO THE NAME TO PREVENT ERASING OLD PLOTS
            self.add_date_to_save_name_entries()

            # ACTIVATE NEW WINDOW BUTTON
            self.createOutputWindowButton.config(state='normal')

        except IndexError:
            print("No file selected")

    def add_date_to_save_name_entries(self):
        date = datetime.today().strftime('%Y-%m-%d_%H-%M')

        for plot_type in GlobalConfig.PLOT_TYPES:
            self.plotNameEntry[plot_type].delete(0, 'end')
            self.plotNameEntry[plot_type].insert(0, date + '__' + plot_type.capitalize())


