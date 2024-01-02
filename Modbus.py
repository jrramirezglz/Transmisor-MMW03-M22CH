#Autor: Jesus Miguel Camarillo
#Proyecto: Aguas 2.0
#Fecha: Julio 2022
#Descripcion: Funciones de Modbus, comunicacion con analizador.

from machine import Pin
from machine import UART


#Reg Register 16 bits 2bytes
#
#Pin 8 configurado como puerto UART
serial_mode=Pin('P8',Pin.OUT)
serial_mode.value(0)
#serial_mode2=Pin('P23',Pin.OUT)
#serial_mode2.value(1)
modbus=UART(1, baudrate=38400,timeout_chars=100)
    
#Poner chip de RS485 en modo transmision
def Tx():
    serial_mode.value(1)
    #serial_mode2.value(1)
    
#Poner chip de RS485 en modo recepcion
def Rx():
    serial_mode.value(0)
    #serial_mode2.value(0)

#comprobacion de errores
def CRC(buf, leng):
    crc = 0xFFFF
    
    for i in range(0, leng):
        crc^=buf[i]
        
        for j in range(0,8):
            if (crc & 0x0001)==1:
                crc>>=1
                crc^=0xA001
            else:
                crc>>=1
    return [(crc & 0xFF),(crc>>8)]

#Funcion lectura de registros
def readReg(slave,S_add,Q_reg):
    
    bufer=[slave]
    bufer.append(0x03)
    bufer.append(S_add>>8)
    bufer.append(S_add & 0xFF)
    bufer.append(Q_reg>>8)
    bufer.append(Q_reg & 0xFF)
    
    bufer+=CRC(bufer,6)
    
    Tx()
    modbus.write(bytes(bufer))
    
    modbus.wait_tx_done(10)
    
    Rx()
    bufer=modbus.read()

    if bufer == None:
        res=False
    else:
        res=bufer[3:(3+(2*Q_reg))]
    
    return res
    
#Funcion Escritura de registros
def writeReg(slave,S_add,Q_reg,data):
    
    bufer=[slave]#Id esclavo
    bufer.append(0x10)
    bufer.append(S_add>>8)
    bufer.append(S_add & 0xFF)
    bufer.append(Q_reg>>8)
    bufer.append(Q_reg & 0xFF)
    bufer.append(Q_reg*2)
    for i in range (bufer[6]-1,-1,-1):
        bufer.append((data>>(8*i)) & 0xFF)
    
    bufer+=CRC(bufer,(7+Q_reg*2))
    
    Tx()
    modbus.write(bytes(bufer))
    
    modbus.wait_tx_done(10)
    
    Rx()
    bufer=modbus.read()

    if bufer == None:
        res=False
    else:
        res=bufer

    return res

