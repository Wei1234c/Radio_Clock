import time

import adapters
import modulators
from ad9833 import AD9833
from jjy import Encoder



class Display:

    def __init__(self, pin_id_ss = 15, pin_id_sck = 14, pin_id_mosi = 13):
        _spi = adapters.SPI.get_uPy_spi(polarity = 1, pin_id_sck = pin_id_sck, pin_id_mosi = pin_id_mosi)
        _ss = adapters.Pin.get_uPy_pin(pin_id = pin_id_ss, output = True)
        self.display = modulators.OOK(AD9833(_spi, _ss))


    def show_time(self, year, month, day, hour, minute, second):
        jjy_sequence = Encoder.get_symbols_ook_sequence(time.time())
        self.display.send_sequence(jjy_sequence)
