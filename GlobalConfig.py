DEFAULT_DIR = "D:/Thomas_Data/GitHub/didactic_palpation_device/src"
DEFAULT_SAVE_DIR = "D:/Thomas_Data/GitHub/didactic_palpation_device/src/temp"

APP_GEOMETRY = "1800x970+10+10"


ACQUISITION_FREQUENCY = 0.3  # in seconds
PLOTTING_FREQUENCY = 300  # in milliseconds

# BE VERY CAREFUL WHEN MODIFYING THE NAME AND ORDER OF THE COLUMNS BELOW ! (WHOLE CODE MUST BE MODIFIED)
DATA_FRAME_COLUMNS = ['index',
                      'interval(ms)',
                      'time(ms)',
                      'command_slave',
                      'position_slave',
                      'speed_slave',
                      'command_master',
                      'position_master',
                      'speed_master',
                      'force',
                      'position_slave_deg',
                      'position_master_deg',
                      'command_slave_amps',
                      'command_master_amps',
                      'elapsed_time(ms)'
                      ]

PLOT_TYPES = ['command', 'force', 'position', 'speed']

OUTPUT_WINDOW_GEOMETRY = "1600x900+20+20"
OUTPUT_TEXT_WIDTH = 165
OUTPUT_TEXT_HEIGHT = 45
