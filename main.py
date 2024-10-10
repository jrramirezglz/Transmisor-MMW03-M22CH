#Autor: Jesus Miguel Camarillo
#Proyecto: Aguas 2.0
#Fecha: Abril 2023
#Descripcion: Programacion Principal

from machine import Timer
from machine import Pin
import Weg
from Weg import rtc
from Weg import time

#esperar 5s a que el medidor Weg arranque
time.sleep(5)

#primer mensaje
Weg.sync()
time.sleep(5)
Weg.envio()

#boton manual de mensaje
def pin_handler(arg):
    Weg.envio()

p_in = Pin('P10', mode=Pin.IN, pull=Pin.PULL_UP)
p_in.callback(Pin.IRQ_FALLING, pin_handler)


#periodo de envio de informacion
a=Timer.Alarm(lambda y: Weg.envio(),s=90, periodic=True)
