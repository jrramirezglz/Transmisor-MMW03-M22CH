from network import Sigfox
from machine import ADC
import pycom
import socket
#Se apaga la funcion que tiene por defecto de parpadeo
pycom.heartbeat(False)

#Configuracion de los pines analogicos de entrada
adc=ADC()
adc2=ADC()
adc3=ADC()
presion=(adc.channel(pin="P20", attn=ADC.ATTN_11DB))
caudal=(adc2.channel(pin="P19", attn=ADC.ATTN_11DB))
hidro=(adc3.channel(pin="P16", attn=ADC.ATTN_11DB))

Q=0                     #Int Caudal
P=0                     #Int Presion
H=0                     #Int Nivel H
#Configuracion inicial del modem de Sigfox
sigfox = Sigfox(mode=Sigfox.SIGFOX, rcz=Sigfox.RCZ2)
#sigfox = Sigfox(mode=Sigfox.FSK, frequency=868000000)
# create a Sigfox socket
s = socket.socket(socket.AF_SIGFOX, socket.SOCK_RAW)
# make the socket blocking
s.setblocking(True)
# configure it as uplink only
s.setsockopt(socket.SOL_SIGFOX, socket.SO_RX, False)
#s.send('0')

# Primer mensaje de ID Modelo 
def sync():
    #Se enciende el color rojo
    pycom.rgbled(0xFF0000)                                                 #ID Modelo Desconocido
    #envio 
    #se apaga el led 
    pycom.rgbled(0x00)

# Funcion de escaneo de medidores
def scan():

#Led se prende de color azul
    pycom.rgbled(0xFF)
    global Q #Caudal
    global P #Presion
    global H #Carga dinamica
    #CAUDAL
    caudal_mil=caudal.voltage()
    if(caudal_mil<400):
        caudal_mil=400
    if(caudal_mil>2000):
        caudal_mil=2000
    Q=(caudal_mil-400)
    Q=int(round(Q))
    
    #NIVEL HIDRO DINAMICO
    hidro_mil=hidro.voltage()
    if(hidro_mil<400):
        hidro_mil=400
    if(hidro_mil>2000):
        hidro_mil=2000
    H=(hidro_mil-400)*0.0625
    H=int(round(H))
    #PRESION
    presion_mil=presion.voltage()
    if(presion_mil<400):
        presion_mil=400
    if(presion_mil>2000):
        presion_mil=2000
    P=(presion_mil-400)/3.125
    P=int(round(P))
# se apaga el led una vez que termina de ejecutar la lectura de lso sensores
    pycom.rgbled(0x00)
#Funcion de escaneo y envio de informacion
def envio():
    
    scan()
    #Se enciende el color verde
    pycom.rgbled(0xFF00)
    s.send('0')
    #print(hex(Comps.BtoN(payload)))
    #se apaga el led 
    pycom.rgbled(0x00)
    



   

