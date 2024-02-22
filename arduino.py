import serial

#establish serial connection between the computer and the port
arduino = serial.Serial(port='COM4', baudrate=9600)


# Send a list of values to the Arduino board
def send_list_to_arduino(values):
    values_str = ','.join(map(str, values))
    arduino.write(bytes(values_str, 'utf-8'))

def close_serial_port():
    if arduino.is_open:
        arduino.close()