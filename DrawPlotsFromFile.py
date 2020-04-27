import os
import matplotlib
import pandas as pd
import tkinter as tk

import GlobalConfig
import CommonFunctions

import matplotlib.pyplot as plt

from datetime import datetime
from matplotlib import style
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import filedialog

matplotlib.use("TkAgg")
style.use("ggplot")
LARGE_FONT = ("Verdana", 12)


def create_data_frame(file_path):
    data = pd.read_csv(file_path, sep=",", header=None)
    # data.columns = ['index', 'command', 'interval(ms)', 'time(ms)', 'position', 'speed']
    data.columns = GlobalConfig.DATA_FRAME_COLUMNS

    data['interval(ms)'] = CommonFunctions.convert_us_to_ms(data['interval(ms)'])
    data['time(ms)'] = CommonFunctions.convert_us_to_ms(data['time(ms)'])

    data = CommonFunctions.add_elapsed_time_to_df(data)

    return data


class DrawPlotsFromFile(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # PLOTS FRAME
        self.ax = dict()
        self.canvas = None

        self.plotsLabelFrame = tk.LabelFrame(self)
        self.plotsLabelFrame.grid(row=1, column=0, rowspan=2)

        self.fill_plots_label_frame()

        # FILE SELECTION FRAME (IN LOWER LEFT FRAME)
        self.selectFileButton = None
        self.selectedFileText = None
        self.isFileSelectedLabel = None

        self.fileSelectionLabelFrame = tk.LabelFrame(self, text="FILE SELECTION BOX", padx=5, pady=15)
        self.fileSelectionLabelFrame.grid(row=1, column=2)

        self.fill_file_selection_label_frame()

        # PLOTS OPTIONS FRAME
        self.optionsLabelFrame = dict()
        self.fileNameLabel = dict()
        self.fileNameEntry = dict()
        self.savePlotButton = dict()
        self.checkButton = dict()
        self.checkButtonValues = dict()

        self.plotsOptionsLabelFrame = tk.LabelFrame(self)
        self.plotsOptionsLabelFrame.grid(row=2, column=2)

        self.fill_plots_options_label_frame()

        # # UPPER FRAME
        # self.upperFrame = tk.LabelFrame(self, highlightthickness=0, borderwidth=0)
        # self.upperFrame.pack()
        #
        # # BACK TO MAIN WINDOW BUTTON
        # self.backButton = tk.Button(self.upperFrame, text="BACK TO MAIN WINDOW",
        #                             pady=10,
        #                             command=lambda: controller.show_frame("MainWindow"))
        # self.backButton.grid(row=0, column=0)
        #
        # # PAGE NAME
        # label = tk.Label(self.upperFrame, text="DRAW PLOTS FROM FILE", font=LARGE_FONT, fg="red")
        # label.grid(row=0, column=1, padx=50)
        #
        # self.draw_command_slave = tk.IntVar()
        # # tk.Checkbutton(self.upperFrame, text="command slave", variable=self.draw_command_slave).grid(row=0, column=2)
        # tk.Checkbutton(self.upperFrame, text="command slave", variable=self.draw_command_slave, command=self.test).grid(row=0, column=2)
        #
        # # MAIN FRAME
        # self.mainFrame = tk.LabelFrame(self, padx=10, pady=10)
        # self.mainFrame.pack()
        #
        # self.df = None
        # self.plot_list = ['command_slave', 'position_slave', 'speed_slave']
        #
        # # SAVE BOXES AND EMPTY PLOTS CREATION
        # self.saveFrame = dict()
        # self.fileNameLabel = dict()
        # self.fileNameEntry = dict()
        # self.savePlotButton = dict()
        #
        # self.ax = dict()
        #
        # self.create_all_plots(1, 0)
        #
        # # LOWER LEFT FRAME
        # self.lowerLeftFrame = tk.LabelFrame(self.mainFrame, pady=10)
        # self.lowerLeftFrame.grid(row=2, column=0)
        #
        # # self.backButton = tk.Button(self.lowerLeftFrame, text="Back to Start Page",
        # #                             pady=15,
        # #                             command=lambda: controller.show_frame("MainWindow"))
        # # # self.backButton.pack()
        # # self.backButton.grid(row=0, column=0)
        #
        # # FILE SELECTION FRAME (IN LOWER LEFT FRAME)
        # self.fileFrame = tk.LabelFrame(self.lowerLeftFrame, text="FILE SELECTION BOX", padx=5, pady=15)
        # # self.fileFrame.pack(padx=10, pady=10)
        # self.fileFrame.grid(row=0, column=1)
        #
        # self.selectFileButton = tk.Button(self.fileFrame, text='SELECT FILE', width=30, height=3,
        #                                   command=lambda: self.import_recording())
        # self.selectFileButton.pack()
        #
        # self.selectedFileText = tk.StringVar()
        # self.selectedFileText.set('FILE: no file selected')
        # self.isFileSelectedLabel = tk.Label(self.fileFrame, textvariable=self.selectedFileText, pady=5)
        # self.isFileSelectedLabel.pack()

        # # SAVE PLOTS (IN LOWER LEFT FRAME)
        # row = 1
        # for plot_type in self.plot_list:
        #     self.draw_save_box(plot_type, row, 0)
        #     # self.create_plot(plot_type, 1, 0)
        #     row += 1

        # # OUTPUT FRAME (LOWER RIGHT)
        # self.outputFrame = tk.LabelFrame(self.mainFrame, text="OUTPUT")
        # self.outputFrame.grid(row=2, column=1, columnspan=2, pady=10)
        #
        # self.outputText = tk.Text(self.outputFrame, width=110, height=20)
        # self.outputText.pack(padx=5, pady=5)

    def test(self):
        print(self.draw_command_slave.get())
        self.draw_command_slave.set(1)
        print(self.draw_command_slave.get())

    def fill_plots_label_frame(self):
        f = Figure(figsize=(11, 9))

        index = 1
        for plot_type in GlobalConfig.PLOT_TYPES:
            self.ax[plot_type] = f.add_subplot(2, 2, index)
            self.ax[plot_type].set_title(plot_type.upper() + " vs TIME", fontsize=16)
            index += 1

        # DO NOT MODIFY THE LINE BELOW - PREVENTS WHITE SPACE
        f.subplots_adjust(left=0.07, right=0.98, top=0.95, bottom=0.05, wspace=0.3)

        self.canvas = FigureCanvasTkAgg(f, master=self.plotsLabelFrame)
        self.canvas.get_tk_widget().pack()
        self.canvas.draw()

    def fill_file_selection_label_frame(self):
        self.selectFileButton = tk.Button(self.fileSelectionLabelFrame, text='SELECT FILE', width=30, height=3,
                                          command=lambda: self.import_recording())
        self.selectFileButton.pack()

        self.selectedFileText = tk.StringVar()
        self.selectedFileText.set('FILE: no file selected')
        self.isFileSelectedLabel = tk.Label(self.fileSelectionLabelFrame, textvariable=self.selectedFileText,
                                            pady=5)
        self.isFileSelectedLabel.pack()

    def fill_plots_options_label_frame(self):
        row_frame = 0
        column_frame = 0
        for plot_type in GlobalConfig.PLOT_TYPES:
            self.optionsLabelFrame[plot_type] = tk.LabelFrame(self.plotsOptionsLabelFrame, padx=15, pady=15,
                                                              text=plot_type.upper())
            self.optionsLabelFrame[plot_type].grid(row=row_frame, column=column_frame)

            # FILE NAME LABEL
            self.fileNameLabel[plot_type] = tk.Label(self.optionsLabelFrame[plot_type],
                                                     text="FILE NAME:")
            self.fileNameLabel[plot_type].grid(row=0, column=0, padx=10)

            # FILE NAME TEXT FIELD
            self.fileNameEntry[plot_type] = tk.Entry(self.optionsLabelFrame[plot_type], borderwidth=3, width=40)
            self.fileNameEntry[plot_type].grid(row=0, column=1)
            self.fileNameEntry[plot_type].insert(0, plot_type.capitalize())

            # SAVE BUTTON
            self.savePlotButton[plot_type] = tk.Button(self.optionsLabelFrame[plot_type], text='SAVE PLOT', padx=10,
                                                       state=tk.DISABLED,
                                                       command=lambda: self.save_plot(plot_type))
            self.savePlotButton[plot_type].grid(row=0, column=2)

            # MASTER CHECK BUTTON
            key = plot_type + "_master"
            if key != 'force_master':
                # THE FORCE IS ONLY MEASURED FOR THE SLAVE
                self.checkButtonValues[key] = tk.IntVar()
                self.checkButtonValues[key].set(1)

                self.checkButton[key] = tk.Checkbutton(self.optionsLabelFrame[plot_type], text="MASTER",
                                                       variable=self.checkButtonValues[key])
                self.checkButton[key].grid(row=1, column=1)

            # SLAVE CHECK BUTTON
            key = plot_type + "_slave"
            self.checkButtonValues[key] = tk.IntVar()
            self.checkButtonValues[key].set(1)

            self.checkButton[key] = tk.Checkbutton(self.optionsLabelFrame[plot_type], text="SLAVE",
                                                   variable=self.checkButtonValues[key])
            self.checkButton[key].grid(row=2, column=1)

            row_frame += 1

    def refresh_all_plots(self):
        x = self.df['elapsed_time(ms)']

        for plot_type in self.plot_list:
            # y = self.df[plot_type]
            self.ax[plot_type].cla()

            self.ax[plot_type].set_title(plot_type.upper() + " vs TIME", fontsize=16)
            self.ax[plot_type].set_ylabel(plot_type, fontsize=14)
            self.ax[plot_type].set_xlabel("elapsed_time(ms)", fontsize=14)

            if plot_type == 'force':
                y = self.df[plot_type]
                self.ax[plot_type].plot(x, y, marker='x', color='blue')

            else:
                if self.checkButtonValues[plot_type + "_master"] == 1:
                    y_master = self.df[plot_type + "_master"]
                    self.ax[plot_type].plot(x, y_master, marker='x', color='red')

                if self.checkButtonValues[plot_type + "_slave"] == 1:
                    y_slave = self.df[plot_type + "_slave"]
                    self.ax[plot_type].plot(x, y_slave, marker='x', color='blue')

            self.savePlotButton[plot_type].config(state='normal')

        self.canvas.draw()

    def import_recording(self):
        file = tk.filedialog.askopenfilenames(initialdir=GlobalConfig.DEFAULT_DIR,
                                              initialfile="tmp",
                                              filetypes=[("All files", "*")]
                                              )
        try:
            file_path = file[0]
            self.selectedFileText.set("FILE: " + os.path.basename(file_path))

            self.df = create_data_frame(file_path)

            # PRINT NEW DATA TO OUTPUT FRAME
            self.outputText.delete(1.0, tk.END)
            string = self.df.to_string(index=False)
            self.outputText.insert(tk.END, string + "\n")
            self.outputText.see("end")

            # DRAW ALL PLOTS
            self.refresh_all_plots()
            self.add_time_to_save_name()

        except IndexError:
            print("No file selected")

    def save_plot(self, plot_type):
        filename = self.fileNameEntry[plot_type].get()
        CommonFunctions.save_plot(filename, self.df, plot_type)

    def add_time_to_save_name(self):
        date = datetime.today().strftime('%Y-%m-%d_%H-%M')

        for plot_type in self.plot_list:
            self.fileNameEntry[plot_type].delete(0, 'end')
            self.fileNameEntry[plot_type].insert(0, date + '__' + plot_type.capitalize())
