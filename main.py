import time
from clases.sensores import Sensores
from clases.leds import Led
from clases.sigfox import Conectividad
from machine import Timer
import inicializar as init

def inicializacion():
    sensor1 = init.inicializarSensores("ADC","P20","Presion") 
    sensor2 = init.inicializarSensores("ADC","P19","Caudal") 
    sensor3 = init.inicializarSensores("ADC","P16","Hidroestatico")
    comunicacion = init.inicializarComunicacion()
    ledIndicador = init.inicializarLeds()
    return sensor1,sensor2,sensor3,comunicacion,ledIndicador

def lecturaSensores():
    lecturaPresion, datoPresion  = presion.leer_sensor()
    lecturaCaudal, datoCaudal = caudal.leer_sensor()
    lecturaHidro, datoHidro = hidro.leer_sensor()
    volt1 = lecturaPresion.to_bytes(2, 'big')
    lPresion = datoPresion.to_bytes(1,'big')
    volt2 = lecturaCaudal.to_bytes(2, 'big')
    lCaudal = datoCaudal.to_bytes(1,'big')
    volt3 = lecturaHidro.to_bytes(2, 'big')
    lHidro = datoHidro.to_bytes(1,'big')
    payload =(volt1+ lPresion + volt2	+ lCaudal + volt3 + lHidro)
    print(payload)
    return payload

def analisisDatos():
    lecturaSensores()
    wireless.send_message(lecturaSensores())

presion, caudal, hidro, wireless, led= inicializacion()
i = 0
for  i in range(3):
    led.led_toggle("GREEN",5)
    analisisDatos()
    time.sleep(30)
#periodo de envio de informacion
a=Timer.Alarm(lambda y: analisisDatos(),s=600, periodic=True)
