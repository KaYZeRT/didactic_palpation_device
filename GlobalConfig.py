COMMUNICATION_PORT = 'COM14'
BAUDRATE = 115200

DEFAULT_DIR = "D:/Thomas_Data/GitHub/didactic_palpation_device/src"
DEFAULT_SAVE_DIR = "D:/Thomas_Data/GitHub/didactic_palpation_device/src/temp"

APP_GEOMETRY = "1800x970+10+10"

OUTPUT_WINDOW_GEOMETRY = "1600x900+20+20"
OUTPUT_TEXT_WIDTH = 165
OUTPUT_TEXT_HEIGHT = 45

SIMULATE_DATA_ACQUISITION_FILE = "src/2020-05-03_15-44__Data_From_Arduino.txt"

PLOTTING_FREQUENCY = 100  # in milliseconds

# BE VERY CAREFUL WHEN MODIFYING THE NAME AND ORDER OF THE COLUMNS BELOW ! (WHOLE CODE MUST BE MODIFIED/CHECKED)
DATA_FRAME_COLUMNS = ['index',  # row[0] - int
                      'interval(ms)',  # row[1] - int
                      'time(ms)',  # row[2] - int
                      'command_slave',  # row[3] - int
                      'position_slave',  # row[4] - int
                      'speed_slave',  # row[5] - float
                      'command_master',  # row[6] - int
                      'position_master',  # row[7] - int
                      'speed_master',  # row[8] - float
                      'force_slave',  # row[9] - float
                      'elapsed_time(ms)',  # row[10] - int
                      # END OF DATA SENT BY ARDUINO
                      'command_slave_amps',  # float
                      'position_slave_deg',  # float
                      'command_master_amps',  # float
                      'position_master_deg'  # float
                      ]

PLOT_TYPES = ['command', 'force', 'position', 'speed']
