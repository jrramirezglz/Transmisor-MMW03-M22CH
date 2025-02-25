import pycom
import time

class Led():
    def __init__(self):
        pycom.heartbeat(False)
        self._led_red = 0xFF0000
        self._led_blue = 0xFF
        self._led_green = 0xFF00
        
    def led_status(self, color):
        if color == "RED":
            pycom.rgbled(self._led_red)
        elif color == "BLUE":
            pycom.rgbled(self._led_blue)
        elif color == "GREEN":
            pycom.rgbled(self._led_green)
        elif color == "OFF":
            pycom.rgbled(0x00)
        else:
            print("color_invalido")
            pycom.rgbled(0x00)
        
    def led_toggle(self,color,tiempo):
        if color == "RED":
            pycom.rgbled(self._led_red)
            time.sleep(tiempo)
        elif color == "BLUE":
            pycom.rgbled(self._led_blue)
            time.sleep(tiempo)
        elif color == "GREEN":
            pycom.rgbled(self._led_green)
            time.sleep(tiempo)
        pycom.rgbled(0x00)
