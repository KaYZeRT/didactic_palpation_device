DEFAULT_DIR = "D:/Thomas_Data/GitHub/didactic_palpation_device/src"
DEFAULT_SAVE_DIR = "D:/Thomas_Data/GitHub/didactic_palpation_device/src/temp"

APP_GEOMETRY = "1800x950+10+10"
ACQUISITION_FREQUENCY = 0.3  # in seconds
PLOTTING_FREQUENCY = 300  # in milliseconds

DATA_FRAME_COLUMNS = ['index',
                      'interval(ms)',
                      'time(ms)',
                      'command_slave',
                      'position_slave',
                      'speed_slave',
                      'command_master',
                      'position_master',
                      'speed_master',
                      'force']

PLOT_TYPES = ['command', 'force', 'position', 'speed']
