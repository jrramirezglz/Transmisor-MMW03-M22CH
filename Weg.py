#Autor: Jesus Miguel Camarillo
#Proyecto: Aguas 2.0
#Fecha: Junio 2023
#Descripcion: Integracion de medidores WEG 
##Pendientes:::
##Conocer bytes de numero de orden y numero de modelo de 2 dispositivos Weg
##Programar y conocer el parametro de tuberia vacia
##Programar falla de energia, falla de resplado

from machine import RTC
from network import Sigfox
from machine import ADC
import pycom
import socket
import medidor_modbus.Modbus as Modbus
import time
import casting_variables.Comps as Comps

#Se apaga la funcion que tiene por defecto de parpadeo
pycom.heartbeat(False)

#Configuracion de los pines analogicos de entrada
rtc=RTC()
adc=ADC()
adc2=ADC()
adc3=ADC()
presion=(adc.channel(pin="P20", attn=ADC.ATTN_11DB))
caudal=(adc2.channel(pin="P19", attn=ADC.ATTN_11DB))
hidro=(adc3.channel(pin="P16", attn=ADC.ATTN_11DB))
#Se delcaran variables globales
m22chb=0                #bit indicador de modelo M22CHB (mas avanzado y unico que cambia de registros)
falla_modbus=0          #bit falla de comunicacion modbus

tem=0                   #32 float Temperatura
Pa=0                    #32 float Potencia Activa Total Instantanea
En=0                    #32 float Energia 
Fp=0                    #32 float Factor de Potencia
Te=0                    #32 float Tension Media de las 3 Fases
Ic=0                    #32 float Corriente Total de las 3 Fases
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

def fallas():
    global falla_modbus
    f=0
    if falla_modbus==1:
        f=0b0100|f
    return f

# Primer mensaje de ID Modelo 
def sync():
    #Se enciende el color rojo
    pycom.rgbled(0xFF0000)
    global falla_modbus, m22chb

    i=Modbus.readReg(1,650,2)
    if i== False:                                           #ID Modelo =0 y marca fallo de modbus
        falla_modbus=1
        i=0
    elif i==b'\x00\xdb\x87\x17':                            #ID Modelo MMW03 CH
        i=0b0011
    elif i==b'\x00\xdb\x87K':                               #ID Modelo MMW03 M22CH
        i=0b0010
    elif Modbus.readReg(1, 2264, 2)==b'\x00\xdb\x87Q':      #ID Modelo MMW03 M22CHB
        i==0b0001
    else:
        i=0                                                 #ID Modelo Desconocido
    #envio 
    i=(fallas()<<4)|i
    i=Comps.NtoB(i,1)
    s.send(i)

    #se apaga el led 
    pycom.rgbled(0x00)

# Funcion de escaneo de medidores
def scan():

#Led se prende de color azul
    pycom.rgbled(0xFF)

#Se accesa a las variables globales 
    global falla_modbus
    global tem #temperatura
    global Pa #potencia activa total
    global En #Energia KWh
    global Fp #factor de potencia media 3 fases
    global Te #tension media 3 fases
    global Ic #corriente total 3 fases
    global Q #Caudal
    global P #Presion
    global H #Carga dinamica

#pedir lectura de regstros en el analizador de energia

    #POTENCIA ACTIVA
    i=Modbus.readReg(1,68,2)
    if i== False:
        falla_modbus=1
        Pa=b'\x00\x00\x00\x00'
    else:
        Pa=i

    Pa=Comps.BtoF(Pa)
    Pa=int(round(float(Pa)/5))
    #ENERGIA ACTIVA
    i=Modbus.readReg(1,470,2)
    if i== False:
        falla_modbus=1
        En=0
    else:
        En=Comps.BtoN(i)     
    if En >= 0xFFFF:
        Modbus.writeReg(1, 5000, 2, 2222)
        Modbus.writeReg(1, 470, 2, En-0xFFFF)
        Modbus.writeReg(1, 2000, 2, 1)
        time.sleep(5)
    
    #FACTOR DE POTENCIA
    i=Modbus.readReg(1,66,2)
    if i== False:
        falla_modbus=1
        Fp=b'\x00\x00\x00\x00'
    else:
        Fp=i
    Fp=Comps.BtoF(Fp)
    Fp=int(round(Fp*100))
    

    #TENSION
    i=Modbus.readReg(1,62,2)
    if i== False:
        falla_modbus=1
        Te=b'\x00\x00\x00\x00'
    else:
        Te=i
    

    #CORRIENTE
    i=Modbus.readReg(1,64,2)
    if i== False:
        falla_modbus=1
        Ic=b'\x00\x00\x00\x00'
    else:
        Ic=i


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
    
    payload=Comps.mesg(fallas(),Pa,Fp,Te,Ic,Q,P,En,H)
    #print(hex(Comps.BtoN(payload)))
    #se apaga el led 
    pycom.rgbled(0x00)
    



   

