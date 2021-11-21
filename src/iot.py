import bmp280

try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus

class BMP280Monitor:
    def __init__(self):
        
        # Inicializa o driver do sensor de temperatura e pressão BMP280
        bus = SMBus(1)
        self._bmp280 = bmp280.BMP280(i2c_dev=bus)

    def get_temperature(self):

        # Obtém a temperatura no sensor
        return self._bmp280.get_temperature()

    def get_pressure(self):

        #Obtém a pressão no sensor
        return self._bmp280.get_pressure()