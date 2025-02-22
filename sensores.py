from machine import ADC

class Sensores:

    def __init__(self, tipo, puerto , nombre):
        self._tipo = tipo
        self._puerto = puerto
        self._nombre = nombre
        self._medicion = 0
        self._dato = 0
        self._sensor = None
    
    def configurar_sensor(self):
        if self._tipo == "ADC":
            sensor = ADC()
            self._sensor=(sensor.channel(pin=self._puerto, attn=ADC.ATTN_11DB))

    def leer_sensor(self):
        self._medicion = self._sensor.voltage()
        return self._medicion

    def convertir_medicion(self):
        if(self._medicion<400):
            self._medicion=400
        if(self._medicion>2000):
            self._medicion=2000
        self._dato=(self._medicion-400)
        self._dato=int(round(self._dato))
        return self._dato

    def informacionDelSensor(self):
        print(self._tipo)
        print(self._puerto)
        print(self._nombre)