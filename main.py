import time
import pycom
from sensores import Sensores
#esperar 5s a que el medidor Weg arranque
pycom.heartbeat(False)
sensor1 = Sensores("ADC","P20","Presion")
sensor1.configurar_sensor()
sensor2 = Sensores("ADC","P19","Caudal")
sensor2.configurar_sensor()
sensor3 = Sensores("ADC","P16","Hidroestatico")
sensor3.configurar_sensor()
while 1:
    time.sleep(2)
    pycom.rgbled(0xFF0000)
    sensor1.informacionDelSensor()                                                 #ID Modelo Desconocido
    print(sensor1.leer_sensor())
    sensor2.informacionDelSensor()                                                 #ID Modelo Desconocido
    print(sensor2.leer_sensor())
    sensor3.informacionDelSensor()                                                 #ID Modelo Desconocido
    print(sensor3.leer_sensor())
    time.sleep(2)
    pycom.rgbled(0x000000)


#periodo de envio de informacion
#a=Timer.Alarm(lambda y: Weg.envio(),s=900, periodic=True)
