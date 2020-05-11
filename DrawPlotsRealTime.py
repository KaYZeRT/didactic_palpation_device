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
    data = pd.read_csv(GlobalConfig.SIMULATE_DATA_ACQUISITION_FILE, sep=",", dtype=object)
    list_of_lists = data.values.tolist()

    res = []

    for list in list_of_lists:
        sub_list = []
        for i in range(len(list)):
            if i == 0 or i == 1 or i == 2 or i == 3 or i == 4 or i == 6 or i == 7 or i == 10:
                # Cannot convert '1.0' to 1 so we do '1.0' --> 1.0 --> 1
                temp = float(list[i])
                sub_list.append(int(temp))
            else:
                sub_list.append(float(list[i]))
        res.append(sub_list)

    return res


def add_row_to_df(df, to_append):
    """Adds the to_append row to the data frame."""
    to_append_series = pd.Series(to_append, index=df.columns, dtype=object)
    df = df.append(to_append_series, ignore_index=True)

    return df


########################################################################################################################
# CLASS: DRAW PLOTS REAL TIME
########################################################################################################################

class DrawPlotsRealTime(DrawPlotsParent):

    def __init__(self, parent, controller):

        super().__init__(parent, controller, real_time=1)

        self.isRecording = False

        self.data = {'index': [],
                     'interval(ms)': [],
                     'time(ms)': [],
                     'command_slave': [],
                     'position_slave': [],
                     'speed_slave': [],
                     'command_master': [],
                     'position_master': [],
                     'speed_master': [],
                     'force_slave': [],
                     'elapsed_time(ms)': [],
                     'command_slave_amps': [],
                     'position_slave_deg': [],
                     'command_master_amps': [],
                     'position_master_deg': []
                     }

        ################################################################################################################
        # ARDUINO + CHOICE BOX
        # USEFUL TO SIMULATE DATA ACQUISITION WITHOUT AN ARDUINO
        ################################################################################################################

        self.choiceVar = tk.StringVar()
        try:
            self.ser = serial.Serial(GlobalConfig.COMMUNICATION_PORT, GlobalConfig.BAUDRATE, timeout=1)
            choices = ["Arduino", "Simulate an Arduino"]
        except:
            self.ser = None
            choices = ["Simulate an Arduino"]

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
        self.acquisitionParametersLabelFrame.grid(row=1, column=0, pady=5)

        self.acquisitionParametersEntryBox = dict()
        # self.interval = tk.IntVar()
        # self.lowValue = tk.IntVar()
        # self.highValue = tk.IntVar()
        self.startRecordingButton = None
        self.stopRecordingButton = None
        self.resetRecordingButton = None
        self.fill_acquisition_parameters_label_frame()

        ################################################################################################################
        # SAVE RECORDING FRAME (IN WINDOW SPECIFIC FRAME)
        ################################################################################################################

        self.saveRecordingLabelFrame = tk.LabelFrame(self.windowSpecificLabelFrame, text="SAVE RECORDING", pady=10)
        self.saveRecordingLabelFrame.grid(row=2, column=0, pady=0)

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
        self.startRecordingButton = tk.Button(self.acquisitionParametersLabelFrame, text='START', width=10, height=1,
                                              command=self.start_recording)
        self.startRecordingButton.grid(row=0, column=2, padx=10)

        # STOP ACQUISITION BUTTON
        self.stopRecordingButton = tk.Button(self.acquisitionParametersLabelFrame, text='STOP', width=10, height=1,
                                             command=self.stop_recording,
                                             state=tk.DISABLED)
        self.stopRecordingButton.grid(row=1, column=2, padx=10)

        # RESET BUTTON
        self.resetRecordingButton = tk.Button(self.acquisitionParametersLabelFrame, text='RESET', width=10, height=1,
                                              command=self.reset_recording)
        self.resetRecordingButton.grid(row=2, column=2, padx=10)

    def fill_save_recording_label_frame(self):
        """
        Fills the saveRecordingLabelFrame with the following elements:
            - filename entry box
            - export data to .txt file button
        """
        tk.Label(self.saveRecordingLabelFrame, text="NAME:").grid(row=0, column=0, padx=10)

        self.filenameEntry = tk.Entry(self.saveRecordingLabelFrame, borderwidth=3, width=30)
        self.filenameEntry.grid(row=0, column=1)
        self.filenameEntry.insert(0, "Data")

        self.saveFileButton = tk.Button(self.saveRecordingLabelFrame, text='SAVE FILE',
                                        width=10, height=1,
                                        state=tk.DISABLED,
                                        command=lambda: self.save_data_as_txt())
        self.saveFileButton.grid(row=0, column=2, padx=10)

    def start_recording(self):
        """
        Retrieves the acquisition parameters from the entry boxes.
        Starts the simulation (if an Arduino is not used) or starts the acquisition from the Arduino.
        Enables/disables multiple buttons.
        Starts to refresh all plots.
        """
        acquisition_parameters = self.get_acquisition_parameters()
        # print(acquisition_parameters)
        if acquisition_parameters == -1:
            return

        self.isRecording = True

        if self.choiceVar.get() == "Simulate an Arduino":
            # SIMULATE REAL TIME ACQUISITION
            self.df = pd.DataFrame(columns=GlobalConfig.DATA_FRAME_COLUMNS)
            self.simulation_data = load_simulation_file()
            self.thread = threading.Thread(target=self.simulate_real_time_data_acquisition).start()
        else:
            # USING ARDUINO
            self.send_acquisition_parameters_to_arduino(acquisition_parameters)

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
        Stops the recording and allows plot saving, data saving and data visualisation in new window.
        It also adds the date to the entry boxes to prevent erasing a file which has already been saved on disk.
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
            # THE VALUE "0" STOPS THE ACQUISITION
            to_send = 'c' + str(0)
            self.ser.write(to_send.encode())

            while self.ser.in_waiting:
                # EMPTIES THE BUFFER
                self.ser.readline()

            self.create_data_frame()

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

        for key in self.data:
            self.data[key] = []

        self.clear_all_plots()
        self.destroy_data_output_window()

        # DATA ACQUISITION SIMULATION
        self.simulation_step = 0

    def save_data_as_txt(self):
        """
        Exports the data frame as a .txt file in the chose directory.
        The filename which is given to the .txt file comes from the filename Entry Box.
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
        """
        Sends the acquisition parameters to the Arduino
        A commend would look like this: c10-1000-3000-1
        10: acquisition frequency (milliseconds)
        1000: low value (command)
        3000: high value (command)
        1: starts the acquisition
        """
        # THE VALUE "1" STARTS THE ACQUISITION
        to_send = 'c' + str(acquisition_parameters[0]) + '-' + str(acquisition_parameters[1]) + '-' \
                  + str(acquisition_parameters[2]) + '-' + str(1)
        self.ser.write(to_send.encode())

        # # CHECK THAT CORRECT DATA WAS SENT - Serial.prints() must be written in the Arduino code
        # print("TO_SEND: " + to_send)
        # print("SENT: ", to_send.encode())
        # sleep(0.05)
        # received_string = self.ser.readline().decode('ascii')
        # print(received_string)
        # interval = self.ser.readline().decode('ascii')
        # print(interval)
        # low_value = self.ser.readline().decode('ascii')
        # print(low_value)
        # high_value = self.ser.readline().decode('ascii')
        # print(high_value)
        # acquiring_data = self.ser.readline().decode('ascii')
        # print(acquiring_data)

    def simulate_real_time_data_acquisition(self):
        """
        This method is useful to simulate data acquisition without an Arduino.
        It loads a line from the simulation_data and adds it to the data frame.
        This operation is repeated every 100 milliseconds.
        NOTE: as add_row_to_df() is NOT an efficient method, it is not recommended to try and go
        faster than 100 milliseconds.
        """
        while self.isRecording:
            # Only load one line (the one associated with simulation_step)
            if self.simulation_step < len(self.simulation_data):
                row = self.simulation_data[self.simulation_step].copy()

                self.df = add_row_to_df(self.df, row)

            self.simulation_step += 1

            time.sleep(100)

    def real_time_data_acquisition(self):

        while self.isRecording:
            received_data = self.ser.readline().decode('ascii')

            if received_data.startswith('b') and received_data.endswith('e\r\n'):
                received_data = received_data.replace('b', '')
                received_data = received_data.replace('e\r\n', '')
                received_data = received_data.split(';')

                if len(received_data) == 11:

                    try:
                        self.data['index'].append(int(received_data[0]))
                        self.data['interval(ms)'].append(int(received_data[1]))
                        self.data['time(ms)'].append(int(received_data[2]))
                        self.data['command_slave'].append(int(received_data[3]))
                        self.data['position_slave'].append(int(received_data[4]))
                        self.data['speed_slave'].append(float(received_data[5]))
                        self.data['command_master'].append(int(received_data[6]))
                        self.data['position_master'].append(int(received_data[7]))
                        self.data['speed_master'].append(float(received_data[8]))
                        self.data['force_slave'].append(float(received_data[9]))
                        self.data['elapsed_time(ms)'].append(int(received_data[10]))

                        self.data['command_slave_amps'].append(convert_command_to_amps(int(received_data[3])))
                        self.data['position_slave_deg'].append(convert_position_to_degrees(int(received_data[4])))
                        self.data['command_master_amps'].append(convert_command_to_amps(int(received_data[6])))
                        self.data['position_master_deg'].append(convert_position_to_degrees(int(received_data[7])))

                    except:
                        pass

    def create_data_frame(self):
        """
        Creates a data frame from the dictionary which contains all the acquired data.
        Having a data frame makes it easier to save the plots and to save the data on disk.
        """
        self.df = pd.DataFrame()

        self.df['index'] = self.data['index']
        self.df['interval(ms)'] = self.data['interval(ms)']
        self.df['time(ms)'] = self.data['time(ms)']
        self.df['command_slave'] = self.data['command_slave']
        self.df['position_slave'] = self.data['position_slave']
        self.df['speed_slave'] = self.data['speed_slave']
        self.df['command_master'] = self.data['command_master']
        self.df['position_master'] = self.data['position_master']
        self.df['speed_master'] = self.data['speed_master']
        self.df['force_slave'] = self.data['force_slave']
        self.df['elapsed_time(ms)'] = self.data['elapsed_time(ms)']
        self.df['command_slave_amps'] = self.data['command_slave_amps']
        self.df['position_slave_deg'] = self.data['position_slave_deg']
        self.df['command_master_amps'] = self.data['command_master_amps']
        self.df['position_master_deg'] = self.data['position_master_deg']

    # @ Override
    def refresh_all_plots(self):
        """
        Refreshes all plots and takes into account whether only the master or slave curve must be plotted.
        Also takes into account whether the user wants to display the command in amperes or the position in degrees.
        If real time plotting is used, the function will be repeated every GlobalConfig.PLOTTING_FREQUENCY milliseconds.
        When all plots are generated (and the data acquisition is finished), activates the save plot button.
        """

        for plot_type in GlobalConfig.PLOT_TYPES:
            self.ax[plot_type].cla()

            self.ax[plot_type].set_title(plot_type.upper() + " vs TIME", fontsize=16)
            self.ax[plot_type].set_ylabel(plot_type, fontsize=14)
            self.ax[plot_type].set_xlabel("elapsed_time(ms)", fontsize=14)

            if plot_type == 'position' and self.checkButtonValues['pos_in_deg'].get() == 1:
                self.ax[plot_type].set_ylabel("position [deg]", fontsize=14)

                if self.checkButtonValues[plot_type + "_master"].get() == 1:
                    x = self.data['elapsed_time(ms)']
                    y_master = self.data['position_master_deg']
                    self.ax[plot_type].plot(x, y_master, marker='x', color='red')

                if self.checkButtonValues[plot_type + "_slave"].get() == 1:
                    x = self.data['elapsed_time(ms)']
                    y_slave = self.data['position_slave_deg']
                    self.ax[plot_type].plot(x, y_slave, marker='x', color='blue')

            elif plot_type == 'command' and self.checkButtonValues['command_in_amps'].get() == 1:
                self.ax[plot_type].set_ylabel("command [A]", fontsize=14)

                if self.checkButtonValues[plot_type + "_master"].get() == 1:
                    x = self.data['elapsed_time(ms)']
                    y_master = self.data['command_master_amps']
                    self.ax[plot_type].plot(x, y_master, marker='x', color='red')

                if self.checkButtonValues[plot_type + "_slave"].get() == 1:
                    x = self.df['elapsed_time(ms)']
                    y_slave = self.df['command_slave_amps']
                    self.ax[plot_type].plot(x, y_slave, marker='x', color='blue')

            else:
                if plot_type != 'force':
                    if self.checkButtonValues[plot_type + "_master"].get() == 1:
                        x = self.data['elapsed_time(ms)']
                        y_master = self.data[plot_type + "_master"]
                        self.ax[plot_type].plot(x, y_master, marker='x', color='red')

                if self.checkButtonValues[plot_type + "_slave"].get() == 1:
                    x = self.data['elapsed_time(ms)']
                    y_slave = self.data[plot_type + "_slave"]
                    self.ax[plot_type].plot(x, y_slave, marker='x', color='blue')

        self.canvas.draw()

        if self.isRecording:
            self.canvas.get_tk_widget().after(GlobalConfig.PLOTTING_FREQUENCY,
                                              lambda: self.refresh_all_plots())
        else:
            self.activate_or_deactivate_save_plot_buttons('normal')

        if self.df is not None and self.real_time != 1:
            self.activate_or_deactivate_save_plot_buttons('normal')

