########################################################################################################################
# IMPORTS
########################################################################################################################

from DrawPlotsParent import *


########################################################################################################################
# STATIC FUNCTIONS
########################################################################################################################

def create_data_frame(file_path):
    """
    Creates a data frame from the .txt file given by file_path.
    Returns this data frame so it can be used to generate the plots.
    """
    data = pd.read_csv(file_path, sep=",")
    return data


########################################################################################################################
# CLASS: DRAW PLOTS FROM FILE
########################################################################################################################

class DrawPlotsFromFile(DrawPlotsParent):

    def __init__(self, parent, controller):

        super().__init__(parent, controller, real_time=0)

        ################################################################################################################
        # FILE SELECTION FRAME (IN WINDOW SPECIFIC FRAME)
        ################################################################################################################

        self.fileSelectionLabelFrame = tk.LabelFrame(self.windowSpecificLabelFrame, text="FILE SELECTION",
                                                     padx=30, pady=10)
        self.fileSelectionLabelFrame.grid(row=0, column=0)

        self.selectFileButton = None
        self.selectedFileVar = None
        self.isFileSelectedLabel = None
        self.fill_file_selection_label_frame()

        ################################################################################################################
        # END OF __INIT__
        ################################################################################################################

    def fill_file_selection_label_frame(self):
        """Fills the fileSelectionLabelFrame with a button to select a file and the name of the selected file (if a
        file is selected)."""
        self.selectFileButton = tk.Button(self.fileSelectionLabelFrame, text='SELECT FILE', width=30, height=3,
                                          command=lambda: self.import_recording())
        self.selectFileButton.pack()

        self.selectedFileVar = tk.StringVar()
        self.selectedFileVar.set('FILE: no file selected')
        self.isFileSelectedLabel = tk.Label(self.fileSelectionLabelFrame, textvariable=self.selectedFileVar)
        self.isFileSelectedLabel.pack(pady=10)

    def import_recording(self):
        """
        Allow the user to import a recording from a .txt file.
        Prints the filename on the GUI.
        Creates a data frame based on the .txt file.
        Plots the data contained in the file.
        Activates the button which creates the DataOutputWindow.
        """
        file = tk.filedialog.askopenfilenames(initialdir=GlobalConfig.DEFAULT_DIR,
                                              initialfile="tmp",
                                              filetypes=[("All files", "*")]
                                              )
        try:
            self.destroy_data_output_window()

            file_path = file[0]
            self.selectedFileVar.set("FILE: " + os.path.basename(file_path))

            self.df = create_data_frame(file_path)

            # DRAW ALL PLOTS
            self.refresh_all_plots()

            # ADD THE DATE AND TIME TO THE NAME TO PREVENT ERASING OLD PLOTS
            self.add_date_to_save_name_entries()

            # ACTIVATE NEW WINDOW BUTTON
            self.createOutputWindowButton.config(state='normal')

        except IndexError:
            print("No file selected")

    # @ Override
    def refresh_all_plots(self):
        """
        Refreshes all plots and takes into account whether only the master or slave curve must be plotted.
        Also takes into account whether the user wants to display the command in amperes or the position in degrees.
        When all plots are generated, activates the save plot button.
        """
        if self.df is not None:
            if self.df.empty is False:

                for plot_type in GlobalConfig.PLOT_TYPES:
                    self.ax[plot_type].cla()

                    self.ax[plot_type].set_title(plot_type.upper() + " vs TIME", fontsize=16)
                    self.ax[plot_type].set_ylabel(plot_type, fontsize=14)
                    self.ax[plot_type].set_xlabel("elapsed_time(ms)", fontsize=14)

                    if plot_type == 'position' and self.checkButtonValues['pos_in_deg'].get() == 1:
                        self.ax[plot_type].set_ylabel("position [deg]", fontsize=14)

                        if self.checkButtonValues[plot_type + "_master"].get() == 1:
                            x = self.df['elapsed_time(ms)']
                            y_master = self.df['position_master_deg']
                            self.ax[plot_type].plot(x, y_master, marker='x', color='red')

                        if self.checkButtonValues[plot_type + "_slave"].get() == 1:
                            x = self.df['elapsed_time(ms)']
                            y_slave = self.df['position_slave_deg']
                            self.ax[plot_type].plot(x, y_slave, marker='x', color='blue')

                    elif plot_type == 'command' and self.checkButtonValues['command_in_amps'].get() == 1:
                        self.ax[plot_type].set_ylabel("command [A]", fontsize=14)

                        if self.checkButtonValues[plot_type + "_master"].get() == 1:
                            x = self.df['elapsed_time(ms)']
                            y_master = self.df['command_master_amps']
                            self.ax[plot_type].plot(x, y_master, marker='x', color='red')

                        if self.checkButtonValues[plot_type + "_slave"].get() == 1:
                            x = self.df['elapsed_time(ms)']
                            y_slave = self.df['command_slave_amps']
                            self.ax[plot_type].plot(x, y_slave, marker='x', color='blue')

                    else:
                        if plot_type != 'force':
                            if self.checkButtonValues[plot_type + "_master"].get() == 1:
                                x = self.df['elapsed_time(ms)']
                                y_master = self.df[plot_type + "_master"]
                                self.ax[plot_type].plot(x, y_master, marker='x', color='red')

                        if self.checkButtonValues[plot_type + "_slave"].get() == 1:
                            x = self.df['elapsed_time(ms)']
                            y_slave = self.df[plot_type + "_slave"]
                            self.ax[plot_type].plot(x, y_slave, marker='x', color='blue')

                self.activate_or_deactivate_save_plot_buttons('normal')
                self.canvas.draw()
