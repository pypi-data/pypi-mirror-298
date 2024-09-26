import serial
import serial.tools.list_ports as list_ports
from time import *

PID_CALLIOPE_1_or_3 = 516
VID_CALLIOPE_1_or_3 = 3368

PID_CALLIOPE_2 = 4133
VID_CALLIOPE_2 = 4966

# PID_CALLIOPE_3 = 516
# VID_CALLIOPE_3 = 3368

TIMEOUT = 0.2

BAUD = 115200

def find_comport():
    ser_port = serial.Serial(timeout=TIMEOUT)
    ser_port.baudrate = BAUD
    ports = list(list_ports.comports())
    for p in ports:
        try:
            if (p.pid == PID_CALLIOPE_1_or_3) and (p.vid == VID_CALLIOPE_1_or_3):
                # Calliope 1 oder Calliope 3 gefunden
                ser_port.port = str(p.device)
                return ser_port
            
            if (p.pid == PID_CALLIOPE_2) and (p.vid == VID_CALLIOPE_2):
                # Calliope 2 gefunden
                ser_port.port = str(p.device)
                return ser_port

        except AttributeError:
            continue

    return None

def readline(s):
    char = s.read()
    val = char
    while char != b'9':
        char = s.read()
        val = val + char
    return val
        
class Interface:
    def __init__(self, comport=False):
        self._lastReadValue = 0

        if comport:
            self.s = serial.Serial(comport, baudrate=BAUD, timeout=TIMEOUT)
        else:
            self.s = find_comport()
            if not self.s:
                raise Exception("Calliope not found")
            self.s.open()
        


    def write(self, value):
        if (value):
            self.s.write(b'1\n')
        else:
            self.s.write(b'0\n')
            
    def read(self):
        # Der Calliope sendet dauerhaft
        # Input-Buffer leeren, damit der aktuelle Wert (und kein alter Wert aus dem Buffer) gelesen wird
        self.s.reset_input_buffer()

        response = self.s.read(1)
        if len(response) == 0:
            print('Timeout beim Lesen')
            return self._lastReadValue
        else:
            if response[0] == 0x30:
                self._lastReadValue = 0
                return 0
            else:
                self._lastReadValue = 1
                return 1


    def close(self):
        self.s.close()