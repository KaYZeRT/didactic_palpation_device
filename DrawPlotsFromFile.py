########################################################################################################################
# IMPORTS
########################################################################################################################

from DrawPlotsParent import *


########################################################################################################################
# STATIC FUNCTIONS
########################################################################################################################

def add_elapsed_time_to_df(df):
    """Calculates elapsed time since the beginning of the acquisition based on the interval(ms) column of the
    data frame (df)."""
    ls = [0]
    time_previous_measurement = df['interval(ms)']

    for i in range(1, df.shape[0]):
        ls.append(ls[i - 1] + time_previous_measurement[i])

    df['elapsed_time(ms)'] = ls
    return df


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
