DEFAULT_DIR = "D:/Thomas_Data/GitHub/didactic_palpation_device/src"
DEFAULT_SAVE_DIR = "D:/Thomas_Data/GitHub/didactic_palpation_device/src/temp"

SIMULATE_DATA_ACQUISITION_FILE = "src/data_slave_and_master.txt"

APP_GEOMETRY = "1800x970+10+10"

OUTPUT_WINDOW_GEOMETRY = "1600x900+20+20"
OUTPUT_TEXT_WIDTH = 165
OUTPUT_TEXT_HEIGHT = 45

ACQUISITION_FREQUENCY = 0.3  # in seconds
PLOTTING_FREQUENCY = 100  # in milliseconds

# BE VERY CAREFUL WHEN MODIFYING THE NAME AND ORDER OF THE COLUMNS BELOW ! (WHOLE CODE MUST BE MODIFIED/CHECKED)
DATA_FRAME_COLUMNS = ['index',  # row[0]
                      'interval(ms)',  # row[1]
                      'time(ms)',  # row[2]
                      'command_slave',  # row[3]
                      'position_slave',  # row[4]
                      'speed_slave',  # row[5]
                      'command_master',  # row[6]
                      'position_master',  # row[7]
                      'speed_master',  # row[8]
                      'force_slave',  # row[9]
                      'elapsed_time(ms)',  # row[10]
                      # END OF DATA SENT BY ARDUINO
                      'command_slave_amps',
                      'position_slave_deg',
                      'command_master_amps',
                      'position_master_deg'
                      ]

PLOT_TYPES = ['command', 'force', 'position', 'speed']

COMMUNICATION_PORT = 'COM14'
BAUDRATE = 115200
