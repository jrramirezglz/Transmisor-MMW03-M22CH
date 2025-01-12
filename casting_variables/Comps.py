#Autor: Jesus Miguel Camarillo
#Proyecto: Aguas 2.0
#Fecha: Julio 2022
#Descripcion: Todas las funciones que hacen casting de varibles y la que arma el payload
import struct

#Decimal a Flotante
def DtoF(valor,exp):
    mult=1
    d=0
    for i in range(exp):
        mult = mult/2
        if ((valor>>(exp-1-i)) & 0x01)==1 :
            d=d+mult

    return d

#Byte a floatante
def BtoF(byte):
    return struct.unpack('>f', byte)[0]

#Floatante a Byte
def FtoB(valor):
    return struct.pack('>f', valor)

#Entero a bytes
def NtoB(valor,n_bytes):
    B=[(valor>>((n_bytes-1)*8))&0xFF]
    for i in range (1, n_bytes):
        B.append((valor>>((n_bytes-1-i)*8))&0xFF)
    return bytes(B)

#Bytes a entero
def BtoN(valor):
    return int.from_bytes(valor, "big")
# Componer un flotante
def F32com(valor,bufer,signo,bit_en,bit_dec):
    exp=((valor>>23)&(0xFF))-127
    expn=23-exp
    mantissa=valor & 0x7FFFFF
    ent=((mantissa+(1<<23))>>expn) & ((2**bit_en)-1)
    dec=(mantissa & ((2**expn)-1)) >> (expn-bit_dec)
    if signo==1:
        bufer=(bufer<<1)+(valor>>31)
    
    bufer=(bufer<<bit_en)+ent
    bufer=(bufer<<bit_dec)+dec
    return bufer

#Componer Entero 
def Icom(valor,bufer,bit):
    ent= valor & ((2**bit)-1)
    
    bufer=(bufer<<bit)+ent
    #print(ent)
    
    return bufer

#Floatante a Bytes
def te(valor):
    
    return BtoN(FtoB(valor))
# Creador de payload
def mesg(falla,v1,v2,v3,v4,v5,v6,v7,v8):
    
    bufer=falla
    
    #POTENCIA ACTIVA
    bufer=Icom(v1,bufer,16)
    #FACTOR DE POTENCIA
    bufer=Icom(v2,bufer,7)
    #TENSION MEDIA
    bufer=F32com(BtoN(v3),bufer,0,10,0)
    #CORRIENTE TOTAL
    bufer=F32com(BtoN(v4),bufer,0,11,0)
    #CAUDAL
    bufer=Icom(v5,bufer,7)
    #PRESION
    bufer=Icom(v6,bufer,9)
    #ENERGIA
    bufer=Icom(v7,bufer,16)
    #NIVEL HIDRODINAMICO
    bufer=Icom(v8,bufer,8)
    

    return NtoB(bufer,11)
    
    
    





