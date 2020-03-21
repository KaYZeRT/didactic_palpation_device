##############################################################################
#IMPORTS
##############################################################################


from tkinter import *


##############################################################################
#PARAMETERS
##############################################################################


SRC_DIR = 'data/'


##############################################################################
#FUNCTIONS
##############################################################################



##############################################################################

##############################################################################


root = Tk()

startRecording = Button(root, text='START RECORDING', padx=50, pady=20)
startRecording.grid(row=0, column=0)

stopRecording = Button(root, text='STOP RECORDING', padx=50, pady=20)
stopRecording.grid(row=1, column=0)

exportRecording = Button(root, text='EXPORT RECORDING', padx=50, pady=20)
exportRecording.grid(row=2, column=0)

importRecording = Button(root, text='IMPORT RECORDING', padx=50, pady=20)
importRecording.grid(row=3, column=0)


root.mainloop()