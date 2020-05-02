import serial

from time import sleep

ser = serial.Serial('COM14', baudrate = 9600, timeout=1)

while True:
    input_value = input('Enter pixel position: ')
    ser.write(input_value.encode())
    
    sleep(0.05)  # in seconds
    
    arduinoData = ser.readline().decode('ascii')
    print(arduinoData)