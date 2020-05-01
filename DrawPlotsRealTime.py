########################################################################################################################
# IMPORTS
########################################################################################################################

import time
import threading

from DrawPlotsParent import *


########################################################################################################################
# STATIC FUNCTIONS
########################################################################################################################

def load_simulation_file():
    res = []
    a_file = open("src/data_slave_and_master.txt", "r")
    list_of_lists = [(line.strip()).split() for line in a_file]

    # Remove ','
    for list in list_of_lists:
        subset = []
        for element in list:
            if ',' in element:
                subset.append(element.replace(',', ''))
            else:
                subset.append(element)
        res.append(subset)

    list_of_lists = res
    res = []

    # Transform strings to float (because the numbers are '1' and not 1)
    for list in list_of_lists:
        to_append = [0 for i in range(len(list))]
        for i in range(len(list)):
            if i == 5 or i == 8 or i == 9:
                to_append[i] = float(list[i])
            else:
                to_append[i] = int(list[i])
        res.append(to_append)

    a_file.close()
    return res


def add_row_to_df(df, to_append):
    """Adds the to_append row to the data frame"""
    to_append_series = pd.Series(to_append, index=df.columns, dtype=object)
    df = df.append(to_append_series, ignore_index=True)

    return df


def calculate_elapsed_time(simulation_step, df, interval):
    if simulation_step == 0:
        res = 0
    else:
        elapsed_time = df.loc[df.index[simulation_step - 1], 'elapsed_time(ms)']
        res = elapsed_time + interval
    return res


########################################################################################################################
# CLASS: DRAW PLOTS REAL TIME
########################################################################################################################

class DrawPlotsRealTime(DrawPlotsParent):

    def __init__(self, parent, controller):

        super().__init__(parent, controller, real_time=1)
        # self.fill_upper_frame("REAL TIME")

        self.isRecording = False

        ################################################################################################################
        # ACQUISITION PARAMETERS (IN WINDOW SPECIFIC FRAME)
        ################################################################################################################

        self.acquisitionParametersLabelFrame = tk.LabelFrame(self.windowSpecificLabelFrame,
                                                             text="ACQUISITION PARAMETERS FRAME",
                                                             padx=5, pady=5)
        self.acquisitionParametersLabelFrame.grid(row=0, column=0)

        self.acquisitionParametersEntryBox = dict()
        self.acquisitionFrequency = tk.IntVar()
        self.lowValue = tk.IntVar()
        self.highValue = tk.IntVar()
        self.startRecordingButton = None
        self.stopRecordingButton = None
        self.resetRecordingButton = None
        self.fill_acquisition_parameters_label_frame()

        ################################################################################################################
        # SAVE RECORDING FRAME (IN WINDOW SPECIFIC FRAME)
        ################################################################################################################

        self.saveRecordingLabelFrame = tk.LabelFrame(self.windowSpecificLabelFrame, text="SAVE RECORDING", pady=10)
        self.saveRecordingLabelFrame.grid(row=1, column=0)

        self.filenameEntry = None
        self.saveFileButton = None
        self.fill_save_recording_label_frame()

        ################################################################################################################
        # REFRESH PLOTS BUTTON (IN WINDOW SPECIFIC FRAME)
        ################################################################################################################

        self.refreshPlotsButton = tk.Button(self.windowSpecificLabelFrame, text="REFRESH PLOTS",
                                            width=30, height=3,
                                            state=tk.DISABLED,
                                            command=lambda: self.refresh_all_plots()
                                            )
        self.refreshPlotsButton.grid(row=2, column=0)

        ################################################################################################################
        # SIMULATION OF REAL DATA ACQUISITION - TO DELETE
        ################################################################################################################
        self.simulation_step = 0
        self.simulation_data = load_simulation_file()

        ################################################################################################################
        # END OF __INIT__
        ################################################################################################################

    def fill_acquisition_parameters_label_frame(self):
        # ACQUISITION FREQUENCY
        tk.Label(self.acquisitionParametersLabelFrame, padx=15, pady=15,
                 text="ACQUISITION FREQUENCY \n (in milliseconds)").grid(row=0, column=0)
        self.acquisitionParametersEntryBox['acquisition_frequency'] = tk.Entry(self.acquisitionParametersLabelFrame,
                                                                               borderwidth=3, width=10)
        self.acquisitionParametersEntryBox['acquisition_frequency'].grid(row=0, column=1)
        self.acquisitionParametersEntryBox['acquisition_frequency'].insert(0, 1)

        # LOW VALUE
        tk.Label(self.acquisitionParametersLabelFrame, padx=15, pady=15,
                 text="LOW VALUE").grid(row=1, column=0)
        self.acquisitionParametersEntryBox['low_value'] = tk.Entry(self.acquisitionParametersLabelFrame,
                                                                   borderwidth=3, width=10)
        self.acquisitionParametersEntryBox['low_value'].grid(row=1, column=1)
        self.acquisitionParametersEntryBox['low_value'].insert(0, 0)

        # HIGH VALUE
        tk.Label(self.acquisitionParametersLabelFrame, padx=15, pady=15,
                 text="HIGH VALUE").grid(row=2, column=0)
        self.acquisitionParametersEntryBox['high_value'] = tk.Entry(self.acquisitionParametersLabelFrame,
                                                                    borderwidth=3, width=10)
        self.acquisitionParametersEntryBox['high_value'].grid(row=2, column=1)
        self.acquisitionParametersEntryBox['high_value'].insert(0, 0)

        self.startRecordingButton = tk.Button(self.acquisitionParametersLabelFrame, text='START', width=20, height=1,
                                              command=self.start_recording)
        self.startRecordingButton.grid(row=0, column=2, padx=10)

        self.stopRecordingButton = tk.Button(self.acquisitionParametersLabelFrame, text='STOP', width=20, height=1,
                                             command=self.stop_recording,
                                             state=tk.DISABLED)
        self.stopRecordingButton.grid(row=1, column=2, padx=10)

        self.resetRecordingButton = tk.Button(self.acquisitionParametersLabelFrame, text='RESET', width=20, height=1,
                                              command=self.reset_recording)
        self.resetRecordingButton.grid(row=2, column=2, padx=10)

    def fill_save_recording_label_frame(self):
        tk.Label(self.saveRecordingLabelFrame, text="FILENAME:").grid(row=0, column=0, padx=10)

        self.filenameEntry = tk.Entry(self.saveRecordingLabelFrame, borderwidth=3, width=40)
        self.filenameEntry.grid(row=0, column=1)
        self.filenameEntry.insert(0, "Data")

        self.saveFileButton = tk.Button(self.saveRecordingLabelFrame, text='SAVE FILE',
                                        width=10, height=1,
                                        state=tk.DISABLED,
                                        command=lambda: self.save_data_as_txt())
        self.saveFileButton.grid(row=0, column=2, padx=10)

    def start_recording(self):
        acquisition_parameters = self.get_data_acquisition_parameters()
        if acquisition_parameters == -1:
            return

        self.startRecordingButton.config(state='disabled')
        self.stopRecordingButton.config(state="normal")
        self.saveFileButton.config(state='disabled')
        self.createOutputWindowButton.config(state='disabled')
        self.refreshPlotsButton.config(state='disabled')

        for plot_type in GlobalConfig.PLOT_TYPES:
            self.savePlotButton[plot_type].config(state='disabled')

        self.isRecording = True
        self.df = pd.DataFrame(columns=GlobalConfig.DATA_FRAME_COLUMNS)

        # DATA ACQUISITION SIMULATION
        threading.Thread(target=self.simulate_real_time_data_acquisition).start()

        self.refresh_all_plots()

    def stop_recording(self):
        self.startRecordingButton.config(state='disabled')  # Keep it disabled unless reset is performed
        self.stopRecordingButton.config(state='disabled')
        self.saveFileButton.config(state='normal')
        self.createOutputWindowButton.config(state='normal')
        self.refreshPlotsButton.config(state='normal')

        for plot_type in GlobalConfig.PLOT_TYPES:
            self.savePlotButton[plot_type].config(state='normal')

        self.isRecording = False
        self.add_date_to_save_name_entries()

        # DATA ACQUISITION SIMULATION
        self.simulation_step = 0

    def reset_recording(self):
        self.startRecordingButton.config(state='normal')
        self.stopRecordingButton.config(state='disabled')
        self.saveFileButton.config(state='disabled')
        self.createOutputWindowButton.config(state='disabled')
        self.refreshPlotsButton.config(state='disabled')

        for plot_type in GlobalConfig.PLOT_TYPES:
            self.savePlotButton[plot_type].config(state='disabled')

        self.isRecording = False
        self.df = None
        self.clear_all_plots()
        self.destroy_data_output_window()

        # DATA ACQUISITION SIMULATION
        self.simulation_step = 0

    def simulate_real_time_data_acquisition(self):
        while self.isRecording:
            # Only load one line (the one associated with simulation_step)
            row = self.simulation_data[self.simulation_step].copy()

            row[1] = int(round(row[1] / 1000, 0))  # interval(ms)
            row[2] = int(round(row[2] / 1000, 0))  # time(ms)

            # APPENDS MUST BE DONE IN THE CORRECT ORDER (SEE GlobalConfig.DATA_FRAME_COLUMNS)

            row.append(convert_command_to_amps(row[3]))  # command_slave_amps
            row.append(convert_position_to_degrees(row[4]))  # position_slave_deg

            row.append(convert_command_to_amps(row[6]))  # command_master_amps
            row.append(convert_position_to_degrees(row[7]))  # position_master_deg

            row.append(calculate_elapsed_time(self.simulation_step, self.df, row[1]))  # elapsed_time(ms)

            self.df = add_row_to_df(self.df, row)
            self.simulation_step += 1

            time.sleep(GlobalConfig.ACQUISITION_FREQUENCY)

    def save_data_as_txt(self):
        filename = self.filenameEntry.get()
        if filename == "":
            tk.messagebox.showerror("Error !", "Filename not defined !")
            return
        save_dir = filedialog.askdirectory(initialdir=GlobalConfig.DEFAULT_SAVE_DIR)

        try:
            self.df.to_csv(save_dir + '/' + filename + '.txt', index=False)
        except:
            tk.messagebox.showerror("Error !", "Error while saving file !")

    def get_data_acquisition_parameters(self):
        """
        Retrieves the data from the low-value, high-value and acquisition frequency entry boxes.
        Checks whether these parameters are valid.
        """
        acquisition_frequency = self.acquisitionParametersEntryBox['acquisition_frequency'].get()
        low_value = self.acquisitionParametersEntryBox['low_value'].get()
        high_value = self.acquisitionParametersEntryBox['high_value'].get()

        try:
            acquisition_frequency = int(acquisition_frequency)
            low_value = int(low_value)
            high_value = int(high_value)

            if acquisition_frequency < 1 or low_value < 0 or high_value < 0:
                tk.messagebox.showerror("Error !", "CHECK ACQUISITION PARAMETERS !")
                return -1
            elif high_value < low_value:
                tk.messagebox.showerror("Error !", "CHECK ACQUISITION PARAMETERS !")
                return -1
            elif low_value > 4095 or high_value > 4095:
                tk.messagebox.showerror("Error !", "CHECK ACQUISITION PARAMETERS !")
                return -1
            else:
                return acquisition_frequency, low_value, high_value

        except:
            tk.messagebox.showerror("Error !", "CHECK ACQUISITION PARAMETERS !")
            return -1

    def send_acquisition_parameters_to_arduino(self):
        pass
