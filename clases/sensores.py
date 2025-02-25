from machine import ADC

class Sensores:

    def __init__(self, tipo, puerto , nombre):
        self._tipo = tipo
        self._puerto = puerto
        self._nombre = nombre
        self._medicion = 0
        self._sensor = None
    
    def configurar_sensor(self):
        if self._tipo == "ADC":
            sensor = ADC()
            self._sensor=(sensor.channel(pin=self._puerto, attn=ADC.ATTN_11DB))

    def leer_sensor(self):
        self._medicion = self._sensor.voltage()
        if(self._medicion<400):
            self._medicion=400
        if(self._medicion>2000):
            self._medicion=2000
        dato = self._medicion
        if self._nombre == "Presion":
            P=(self._medicion-400)/3.125
        elif self._nombre == "Hidroestatico":
            P=((((self._medicion - 400)*10.2)/1600)*10)
        elif self._nombre == "Caudal":
            P=(self._medicion - 400)      
        else :
            P = 0
        dato=int(round(P))
        return  self._medicion, dato

    def informacionDelSensor(self):
        print(self._tipo)
        print(self._puerto)
        print(self._nombre)
