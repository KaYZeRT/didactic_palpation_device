import serial

ser = serial.Serial('COM14', baudrate = 112500, timeout=1)

while 1:
    arduinoData = ser.readline().decode('ascii')
    print(arduinoData)