########################################################################################################################
# IMPORTS
########################################################################################################################

import serial
import time
import threading

import GlobalConfig

from DrawPlotsParent import *
from time import sleep


########################################################################################################################
# STATIC FUNCTIONS
########################################################################################################################

def load_simulation_file():
    """
    Loads data to simulate an acquisition without an Arduino.
    This function might need to be adapted as the source file could vary (for example, separation is ";" instead of ",")
    """
    res = []
    a_file = open(GlobalConfig.SIMULATE_DATA_ACQUISITION_FILE, "r")
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
    """Adds the to_append row to the data frame."""
    to_append_series = pd.Series(to_append, index=df.columns, dtype=object)
    df = df.append(to_append_series, ignore_index=True)

    return df


def calculate_elapsed_time(simulation_step, df, interval):
    """Calculates elapsed time since the beginning of the acquisition based on the last elapsed_time(ms) value of the
    data frame (df) and on the interval value of row."""
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
        # CHOICE BOX (IN WINDOW SPECIFIC FRAME)
        # USEFUL TO SIMULATE DATA ACQUISITION WITHOUT AN ARDUINO
        ################################################################################################################

        self.choiceVar = tk.StringVar()
        choices = ["Arduino", "Simulate an Arduino"]
        # self.choiceVar.set(choices[1])
        self.choiceVar.set(choices[0])
        self.choiceMenu = tk.OptionMenu(self.windowSpecificLabelFrame, self.choiceVar, *choices)
        self.choiceMenu.config(width=25)
        self.choiceMenu.grid(row=0, column=0)

        self.simulation_step = 0
        self.simulation_data = None
        self.thread = None

        ################################################################################################################
        # ACQUISITION PARAMETERS (IN WINDOW SPECIFIC FRAME)
        ################################################################################################################

        self.acquisitionParametersLabelFrame = tk.LabelFrame(self.windowSpecificLabelFrame,
                                                             text="ACQUISITION PARAMETERS",
                                                             padx=5, pady=5)
        self.acquisitionParametersLabelFrame.grid(row=1, column=0, pady=10)

        self.acquisitionParametersEntryBox = dict()
        self.interval = tk.IntVar()
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
        self.saveRecordingLabelFrame.grid(row=2, column=0, pady=10)

        self.filenameEntry = None
        self.saveFileButton = None
        self.fill_save_recording_label_frame()

        ################################################################################################################
        # REFRESH PLOTS BUTTON (IN WINDOW SPECIFIC FRAME)
        ################################################################################################################

        self.refreshPlotsButton = tk.Button(self.windowSpecificLabelFrame, text="REFRESH PLOTS",
                                            width=30, height=1,
                                            state=tk.DISABLED,
                                            command=lambda: self.refresh_all_plots()
                                            )
        self.refreshPlotsButton.grid(row=3, column=0, pady=5)

        ################################################################################################################
        # ARDUINO
        ################################################################################################################

        self.ser = serial.Serial(GlobalConfig.COMMUNICATION_PORT, GlobalConfig.BAUDRATE, timeout=1)

        ################################################################################################################
        # END OF __INIT__
        ################################################################################################################

    def fill_acquisition_parameters_label_frame(self):
        """
        Fills the acquisitionParametersLabelFrame with the following elements:
            - interval entry box
            - low_value entry box
            - high_value entry box
            - start acquisition button
            - stop acquisition button
            - reset button
        """
        # ACQUISITION FREQUENCY
        tk.Label(self.acquisitionParametersLabelFrame, padx=15, pady=15,
                 text="ACQUISITION FREQUENCY \n (in milliseconds)").grid(row=0, column=0)
        self.acquisitionParametersEntryBox['interval'] = tk.Entry(self.acquisitionParametersLabelFrame,
                                                                  borderwidth=3, width=10)
        self.acquisitionParametersEntryBox['interval'].grid(row=0, column=1)
        self.acquisitionParametersEntryBox['interval'].insert(0, 10)

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

        # START ACQUISITION BUTTON
        self.startRecordingButton = tk.Button(self.acquisitionParametersLabelFrame, text='START', width=20, height=1,
                                              command=self.start_recording)
        self.startRecordingButton.grid(row=0, column=2, padx=10)

        # STOP ACQUISITION BUTTON
        self.stopRecordingButton = tk.Button(self.acquisitionParametersLabelFrame, text='STOP', width=20, height=1,
                                             command=self.stop_recording,
                                             state=tk.DISABLED)
        self.stopRecordingButton.grid(row=1, column=2, padx=10)

        # RESET BUTTON
        self.resetRecordingButton = tk.Button(self.acquisitionParametersLabelFrame, text='RESET', width=20, height=1,
                                              command=self.reset_recording)
        self.resetRecordingButton.grid(row=2, column=2, padx=10)

    def fill_save_recording_label_frame(self):
        """
        Fills the saveRecordingLabelFrame with the following elements:
            - filename entry box
            - export data to .txt file button
        """
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
        """TO COMMENT AFTER ARDUINO PART IS DONE"""
        self.isRecording = True
        self.df = pd.DataFrame(columns=GlobalConfig.DATA_FRAME_COLUMNS)

        if self.choiceVar.get() == "Simulate an Arduino":
            self.simulation_data = load_simulation_file()
            self.thread = threading.Thread(target=self.simulate_real_time_data_acquisition).start()
        else:
            acquisition_parameters = self.get_acquisition_parameters()
            print(acquisition_parameters)
            if acquisition_parameters == -1:
                return
            self.send_acquisition_parameters_to_arduino(acquisition_parameters)
            self.interval = acquisition_parameters[0]
            self.thread = threading.Thread(target=self.real_time_data_acquisition).start()

        self.startRecordingButton.config(state='disabled')
        self.stopRecordingButton.config(state="normal")
        self.saveFileButton.config(state='disabled')
        self.createOutputWindowButton.config(state='disabled')
        self.refreshPlotsButton.config(state='disabled')

        self.activate_or_deactivate_save_plot_buttons('disabled')

        self.refresh_all_plots()

    def stop_recording(self):
        """
        Stops the recording and allows plot saving, data visualisation in new window.
        It also adds the date to the entry boxes to prevent erasing a file which has already been saved on disk
        """
        self.startRecordingButton.config(state='disabled')  # Keep it disabled unless reset is performed
        self.stopRecordingButton.config(state='disabled')
        self.saveFileButton.config(state='normal')
        self.createOutputWindowButton.config(state='normal')
        self.refreshPlotsButton.config(state='normal')

        # self.activate_or_deactivate_save_plot_buttons('normal')

        if self.thread is not None:
            self.thread.stop()

        if self.choiceVar.get() == "Arduino":
            to_send = str(1)  # TOGGLE
            self.ser.write(to_send.encode())

            sleep(0.05)
            print("STOPPING ARDUINO")
            sending_data = self.ser.readline().decode('ascii')
            print(sending_data)

        self.isRecording = False
        self.add_date_to_save_name_entries()

        # DATA ACQUISITION SIMULATION
        self.simulation_step = 0

    def reset_recording(self):
        """Wipes the recorded data and prepares the program for a new data acquisition."""
        self.startRecordingButton.config(state='normal')
        self.stopRecordingButton.config(state='disabled')
        self.saveFileButton.config(state='disabled')
        self.createOutputWindowButton.config(state='disabled')
        self.refreshPlotsButton.config(state='disabled')

        self.activate_or_deactivate_save_plot_buttons('disabled')

        self.isRecording = False
        self.df = None
        self.clear_all_plots()
        self.destroy_data_output_window()

        # DATA ACQUISITION SIMULATION
        self.simulation_step = 0

    def save_data_as_txt(self):
        """
        Exports the data frame as a .txt file in the chose directory.
        The filename which is given to the .txt file comes from the filename Entry Box
        """
        filename = self.filenameEntry.get()
        if filename == "":
            tk.messagebox.showerror("Error !", "Filename not defined !")
            return
        save_dir = filedialog.askdirectory(initialdir=GlobalConfig.DEFAULT_SAVE_DIR)

        try:
            self.df.to_csv(save_dir + '/' + filename + '.txt', index=False)
        except:
            tk.messagebox.showerror("Error !", "Error while saving file !")

    def get_acquisition_parameters(self):
        """
        Retrieves the data from the low-value, high-value and acquisition frequency entry boxes.
        Checks whether these parameters are valid or not.
        """
        interval = self.acquisitionParametersEntryBox['interval'].get()
        low_value = self.acquisitionParametersEntryBox['low_value'].get()
        high_value = self.acquisitionParametersEntryBox['high_value'].get()

        try:
            interval = int(interval)
            low_value = int(low_value)
            high_value = int(high_value)

            if interval < 1 or low_value < 0 or high_value < 0:
                tk.messagebox.showerror("Error !", "CHECK ACQUISITION PARAMETERS !")
                return -1
            elif high_value < low_value:
                tk.messagebox.showerror("Error !", "CHECK ACQUISITION PARAMETERS !")
                return -1
            elif low_value > 4095 or high_value > 4095:
                tk.messagebox.showerror("Error !", "CHECK ACQUISITION PARAMETERS !")
                return -1
            else:
                return interval, low_value, high_value

        except:
            tk.messagebox.showerror("Error !", "CHECK ACQUISITION PARAMETERS !")
            return -1

    def send_acquisition_parameters_to_arduino(self, acquisition_parameters):
        # THE VALUE "1" STARTS THE ACQUISITION (IT IS THE TOGGLE)
        to_send = str(acquisition_parameters[0]) + '-' + str(acquisition_parameters[1]) + '-' \
                  + str(acquisition_parameters[2]) + '-' + str(1)
        print("TO_SEND: " + to_send)

        self.ser.write(to_send.encode())

        print("SENT: ", to_send.encode())

        sleep(0.05)

        received_string = self.ser.readline().decode('ascii')
        print(received_string)

        interval = self.ser.readline().decode('ascii')
        print(interval)

        low_value = self.ser.readline().decode('ascii')
        print(low_value)

        high_value = self.ser.readline().decode('ascii')
        print(high_value)

        sending_data = self.ser.readline().decode('ascii')
        print(sending_data)

    def simulate_real_time_data_acquisition(self):
        """
        This method is useful to simulate data acquisition without an Arduino.
        It loads a line from the simulation_data and performs the following operations on it: convert interval and time
        to milliseconds, adds command (for master and slave) in amperes and adds position (for master and slave) in
        degrees. Then, it appends the whole line to the data frame.
        This operation is repeated every GlobalConfig.ACQUISITION_FREQUENCY seconds.
        """
        while self.isRecording:
            # Only load one line (the one associated with simulation_step)
            row = self.simulation_data[self.simulation_step].copy()

            row[1] = int(round(row[1] / 1000, 0))  # interval(ms)
            row[2] = int(round(row[2] / 1000, 0))  # time(ms)

            # APPENDS MUST BE DONE IN THE CORRECT ORDER (SEE GlobalConfig.DATA_FRAME_COLUMNS)

            row.append(calculate_elapsed_time(self.simulation_step, self.df, interval=row[1]))  # elapsed_time(ms)

            row.append(convert_command_to_amps(row[3]))  # command_slave_amps
            row.append(convert_position_to_degrees(row[4]))  # position_slave_deg

            row.append(convert_command_to_amps(row[6]))  # command_master_amps
            row.append(convert_position_to_degrees(row[7]))  # position_master_deg

            self.df = add_row_to_df(self.df, row)
            self.simulation_step += 1

            time.sleep(GlobalConfig.ACQUISITION_FREQUENCY)

    def real_time_data_acquisition(self):

        while self.isRecording:
            row = []

            received_data = self.ser.readline().decode('ascii')
            print(received_data)

            time.sleep(self.interval/1000)
