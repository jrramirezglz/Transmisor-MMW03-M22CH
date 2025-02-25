from machine import Timer, Pin, ADC
import pycom
from network import Sigfox
import socket
import time

class Conectividad:

    def __init__(self):
        self._frecuencia = Sigfox.RCZ2
        self._local_message_mode = False
        self._downlink = False
        self._test_message = "1"
        self._sigfox_mode = Sigfox.SIGFOX
        #Configuracion inicial del modem de Sigfox
        if self._local_message_mode == False: 
            sigfox = Sigfox(self._sigfox_mode, rcz=self._frecuencia)
        else:
            sigfox = Sigfox(mode=Sigfox.FSK, frequency=868000000)
        # create a Sigfox socket
        self.sigfox_module = socket.socket(socket.AF_SIGFOX, socket.SOCK_RAW)
        # make the socket blocking
        self.sigfox_module.setblocking(True)
        if self._downlink == False:
            # configure it as uplink only
            self.sigfox_module.setsockopt(socket.SOL_SIGFOX, socket.SO_RX, False)
        else:
            self.sigfox_module.setsockopt(socket.SOL_SIGFOX, socket.SO_RX, True)

    def send_message(self,mensaje1):
        self.sigfox_module.send(mensaje1)
        print("Mensaje enviado")

    def read_sensor(self):
        #print(self._sensor.vref())
        #self._sensor.vref(1250)    
        #print(self._sensor.vref())
        time.sleep(1)
        self._sensor_read()
        lectura = self._sensor_read.voltage()
        if(lectura<400):
            lectura=400
        if(lectura>2000):
            lectura=2000
        altura=round(((((lectura - 400)*10.2)/1600)*10))

        return lectura ,altura
