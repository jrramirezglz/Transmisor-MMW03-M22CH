import time
from clases.sensores import Sensores
from clases.leds import Led
from clases.sigfox import Conectividad
from machine import Timer

def inicializarSensores(tipo,puerto,nombre):
    sensor = Sensores(tipo,puerto,nombre)
    sensor.configurar_sensor()
    return sensor

def inicializarComunicacion():
    com = Conectividad()
    return com