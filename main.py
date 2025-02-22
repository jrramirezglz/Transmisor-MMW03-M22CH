from machine import Timer
from machine import Pin
import time
#esperar 5s a que el medidor Weg arranque
time.sleep(5)

#primer mensaje
#Weg.sync()
#time.sleep(5)
#Weg.envio()

#periodo de envio de informacion
a=Timer.Alarm(lambda y: Weg.envio(),s=900, periodic=True)
