#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as matdate
import random
from datetime import timedelta, datetime

class Fila(object):
    """Clase base de fila"""

    def __init__(self):
        """constructor de la clase Fila"""
        self.apertura = False
        self.enfila=0
        self.fila = []

    def abrircaja(self):
        """Metodo que abre una fila/caja"""
        if self.apertura == False:
            self.apertura = True

    def cerrarcaja(self):
        """Metodo que cierra una fila/caja"""
        if self.apertura == True:
            self.enfila = 0
            self.fila = []
            self.apertura = False

    def get_clientes_enfila(self):
        """Metodo que devuelve el numero de cliente por fila"""
        return self.enfila

    def estado_caja(self):
        """Metodo que devuelve si la caja esta cerrada o abierta"""
        return self.apertura

    def get_DNI_cliente_en_fila(self, posicion):
        """Metodo que duelve el DNI de algun cliente dado en alguna posicion (parametro)"""
        DNI = self.fila[posicion].get_DNI()
        return DNI


class FilaPreferencial(Fila):
    """Clase de la fila de los clientes preferenciales"""

    def insertar(self, cliente):
        """Inserta un nuevo cliente en la fila preferencial"""
        if (cliente.categoria == "Preferencial"):
            #print("Cliente agregado a la fila preferencial")
            self.enfila+=1
            self.fila.append(cliente)
        #else:
            #print("Cliente no preferencial, debe agregarse a fila no preferncial o cambiar de categoria")

    def atender(self):
        """Atiende al proximo cliente preferencial"""
        self.enfila-=1
        self.fila.pop(0)

    def abrircajanueva(self,maxenfila,filanueva):
        """Si maxenfila es menor que la cantidad de clientes actualmente en espera, abro nueva caja"""
        if (maxenfila < self.enfila):
            if (filanueva.apertura == False) : #Chequeamos que la caja filanueva ya esta abierta o no, si no lo esta, la abre
                print("Abriendo caja nueva")
                filanueva.abrircaja()
                mitadFila = self.enfila // 2 #Dividimos en dos a la fila
                filanueva.enfila = self.enfila - mitadFila
                self.enfila = mitadFila
                filanueva.fila = self.fila[0:filanueva.enfila]  #Y guardamos los clientes en cada fila en mitades
                self.fila = self.fila[filanueva.enfila:]

class FilaGeneral(Fila):
    """Clase que mantiene una fila de clientes no preferenciales"""

    def insertar(self, cliente):
        """Inserta un nuevo cliente en la fila no preferencial"""
        if (cliente.categoria != "Preferencial"):
            #print("Cliente agregado a la fila general")
            self.enfila+=1
            self.fila.append(cliente)

    def atender(self):
        """Atiende al proximo cliente no prederencial"""
        self.enfila-=1
        self.fila.pop(0)


class cliente(object):
    """clase cliente """
    def __init__(self,dni):
        """ constructor de la clase cliente """
        self.dni=dni
        self.categoria=None

    def modificarcategoria(self, categoria):
        """modifica el atributo categoria del cliente """
        self.categoria = categoria

    def get_categoria(self):
        """Metodo que devuelve a que categoria pertenece el cliente"""
        return self.categoria

    def get_DNI(self):
        """Metodo que devuelve el DNI del cliente"""
        return self.dni

#Funcion que devuelve horas y minutos
def convert_from_minutes(minutes):
    td = timedelta(minutes=minutes)
    dt = datetime(2018,1,1,8,0)
    result = dt + td
    return result

if __name__ == "__main__":
    """ simular una fila en una entidad bancaria"""

    #El banco cuenta con 3 cajas generales generales y 5 cajas preferenciales.
    #Las 3 cajas generales estan abiertas todo el tiempo. Las cajas preferenciales se abren cuando llega una cantidad de
    #clientes que obliga a abrir una caja si es que hay disponibles. Si una caja preferencial esta vacia un cierto tiempo, se cierra.

    # El horario bancario es de 8 a 14 horas en los que los clientes pueden ingresar al banco con una probabilidad de probabilidadLLegadaCliente,
    # luego una vez cerrado se atienden a todos los clientes que hayan entrado. En minutos va a significar 360 minutos.
    # En un dia promedio ingresan entre 1 cliente cada minuto. Por otro lado, la proporcion de clientes preferenciales es de un 25%.

    #Cada loop va a simular 1 minuto. Durante ese minuto, puede llegar un cliente con un probabilidad del "probabilidadLLegadaCliente"
    #Durante esos 1 minutos, un cliente prefencial tiene un "probabilidadAtencionClientePreferencial" de ser atendido
    #Durante esos 1 minutos, un cliente general tiene un "probabilidadAtencionClienteGeneral" de ser atendido
    #Si una caja prerencial pasa 5 minutos (5 loops) sin clientes, se cierra siempre quedando al menos una abierta
    #La fila maxima preferencial por caja es de 2.

    #Configuraciones
    minutosBancoAbierto = 360
    proporcionPreferencial = 0.25       # Hay aproximadamnete 25% de clientes preferenciales en el banco
    probabilidadLLegadaCliente = 0.75   # Cada 1 minuto puede llegar un cliente con una probabilidad de 0.75
    probabilidadAtencionClienteGeneral = 0.3   # Cada 1 minuto puede llegar un cliente general ser atendido con un 0.3 de probablidad
    probabilidadAtencionClientePreferencial = 0.25   # Cada 1 minuto puede llegar un cliente preferencial ser atendido con un 0.25 de probablidad
    maximoClientePreferencialPorCaja = 2           # Numero de clientes preferencial maximo en la fila por caja, antes que se habra una nueva
    numeroCajasGenerales = 2
    numeroCajasPreferenciales = 3
    cajasPreferencialesAbiertas = 1

    madness = False
    #Habilitame si queres que se descontrole todo
    #madness = True

    if madness == True:
        proporcionPreferencial = 0.5       # Hay aproximadamnete 50% de clientes preferenciales en el banco
        probabilidadLLegadaCliente = 1     # Cada 1 minuto puede llegar un cliente con una probabilidad 100%
        probabilidadAtencionClienteGeneral = 0.1   # Cada 1 minuto puede llegar un cliente general ser atendido con un 0.3 de probablidad
        probabilidadAtencionClientePreferencial = 0.15   # Cada 1 minuto puede llegar un cliente preferencial ser atendido con un 0.25 de probablidad
        maximoClientePreferencialPorCaja = 20           # Numero de clientes preferencial maximo en la fila por caja, antes que se habra una nueva
        numeroCajasGenerales = 2
        numeroCajasPreferenciales = 2
        cajasPreferencialesAbiertas = 1

    # Creamos las cajas del banco
    cajasGenerales = []
    cajasGeneralesAbiertas = numeroCajasGenerales
    for index in range(0, numeroCajasGenerales):
        cajasGenerales.append(FilaGeneral())
        cajasGenerales[index].abrircaja()

    # Lista que van a guardar el estado de las filas de caja cada 1 minutos
    estadoFilaGenerales = []
    for index in range(0, numeroCajasGenerales):
        estadoFilaGenerales.append([0])

    cajasPreferenciales = []
    for index in range(0, numeroCajasPreferenciales):
        cajasPreferenciales.append(FilaPreferencial())
    for index in range(0, cajasPreferencialesAbiertas):
        cajasPreferenciales[index].abrircaja()

    estadoFilaPreferenciales = []
    for index in range(0, numeroCajasPreferenciales):
        estadoFilaPreferenciales.append([0])

    tiempoCajaPreferenciaAbiertaVacia = [0] * numeroCajasPreferenciales #Lista que mide el tiempo de cada caja que esta vacia

    #Vamos a medir, tiempo de espera promedio por cliente preferencial y general
    tiempoAtencionporCliente = []
    tiempoAtencionporClienteGeneral = []
    tiempoAtencionporClientePreferencial = []

    minutosPasados = 0
    DNICliente = 0
    clientesLlegaron = 0
    clientesAtendidos = 0
    contadorCiclos = 0

    while minutosPasados < minutosBancoAbierto or clientesAtendidos < clientesLlegaron:

        if minutosPasados == 0:
            print("------------------------------------")
            print("Banco abierto")
            print("------------------------------------")
        elif minutosPasados == minutosBancoAbierto:
            totalclientes = clientesLlegaron - clientesAtendidos
            print("------------------------------------")
            print("Banco cerró la puertas y quedan " + str(totalclientes) + " clientes por atender")

        #Si el banco está abierto, va llegando clientes
        if minutosPasados < minutosBancoAbierto:
            #Vemos si llega un cliente
            llegoCliente = random.random()

            if llegoCliente < probabilidadLLegadaCliente:

                clienteTemp = cliente(DNICliente)

                #La relacion de clientes preferenciales de generales se va a asignar de forma aleatoria.
                tipocliente = random.random()

                if tipocliente <= proporcionPreferencial:
                    clienteTemp.modificarcategoria("Preferencial")
                else:
                    clienteTemp.modificarcategoria("General")

                #Lo metemos en alguna cola
                if clienteTemp.get_categoria() == "Preferencial": #Si el cliente es preferencial

                    #Le asignamos unas de las cajas preferneciales, se le asigna la fila con menos clientes en fila
                    numeroClienteLastCaja = 99999
                    indexCajaMenosClientes = -1

                    for index, caja in enumerate(cajasPreferenciales):

                        if caja.estado_caja() == True:
                            if caja.get_clientes_enfila() < numeroClienteLastCaja:
                                indexCajaMenosClientes = index
                                numeroClienteLastCaja = caja.get_clientes_enfila()

                    cajasPreferenciales[indexCajaMenosClientes].insertar(clienteTemp)

                else:
                    #Le asignamos unas de las cajas generles, se le asigna la fila con menos clientes en fila
                    numeroClienteLastCaja = 99999
                    indexCajaMenosClientes = -1

                    for index, caja in enumerate(cajasGenerales):

                        if caja.get_clientes_enfila() < numeroClienteLastCaja:
                            indexCajaMenosClientes = index
                            numeroClienteLastCaja = caja.get_clientes_enfila()

                    cajasGenerales[indexCajaMenosClientes].insertar(clienteTemp)

                #Medimos en que ciclo entro el cliente al banco
                tiempoAtencionporCliente.append(contadorCiclos)

                DNICliente += 1
                clientesLlegaron = DNICliente

        # Vemos las cajas generales
        for index,caja in enumerate(cajasGenerales):
            #Hay clientes?
            if caja.get_clientes_enfila() != 0:
                atiendeN = random.random() #Tiramos el dado
                if atiendeN < probabilidadAtencionClienteGeneral: #Si sale que si, atiende a un cliente

                    #Medimos el tiempo de atencion del clientes
                    DNI = caja.get_DNI_cliente_en_fila(0)
                    tiempoAtencionporCliente[DNI] =  contadorCiclos - tiempoAtencionporCliente[DNI]
                    tiempoAtencionporClienteGeneral.append(tiempoAtencionporCliente[DNI])

                    caja.atender()
                    clientesAtendidos+=1

        # Vemos las cajas preferenciales
        for index,caja in enumerate(cajasPreferenciales):
            #Esta abierta la caja?
            if caja.estado_caja() == True:
                #Hay clientes?
                if caja.get_clientes_enfila() != 0:
                    atiendeN = random.random() #Tiramos el dado
                    if atiendeN < probabilidadAtencionClientePreferencial: #Si sale que si, atiende a un cliente

                        #Medimos el tiempo de atencion del clientes
                        #Use DNI como contador, otra forma de resolverlo era usar rango de DNI validos y usar un diccionario
                        DNI = caja.get_DNI_cliente_en_fila(0)
                        tiempoAtencionporCliente[DNI] =  contadorCiclos - tiempoAtencionporCliente[DNI]
                        tiempoAtencionporClientePreferencial.append(tiempoAtencionporCliente[DNI])
                        caja.atender()
                        clientesAtendidos+=1

        # Vemos si es necesario abrir alguna nueva caja preferencial
        for index, caja in enumerate(cajasPreferenciales):
            #Esta abierta la caja?
            if caja.estado_caja() == True:
                #Vemos si esta vacia, la primera caja preferencial nunca la cierra
                if index > 0:
                    if caja.get_clientes_enfila() == 0:
                        tiempoCajaPreferenciaAbiertaVacia[index]+= 1
                    else:
                        tiempoCajaPreferenciaAbiertaVacia[index] = 0

                    #Si pasaron 5 minutos sin clientes, la caja se cierra
                    if tiempoCajaPreferenciaAbiertaVacia[index] == 5:
                        print("Se cierra la caja " + str(index) + " preferencial")
                        caja.cerrarcaja()

                #Vemos si es necesario abrir, para ello vamos probando si queda alguna de las cajas abiertas
                for cajanueva in cajasPreferenciales:
                    caja.abrircajanueva(maximoClientePreferencialPorCaja, cajanueva)


        contadorCiclos += 1
        minutosPasados += 1

        #Sacamos una foto a todas las filas
        for index, caja in enumerate(cajasGenerales):
            estadoFilaGenerales[index].append(caja.get_clientes_enfila())

        for index, caja in enumerate(cajasPreferenciales):
            estadoFilaPreferenciales[index].append(caja.get_clientes_enfila())

print("------------------------------------")
print("Se atendió al ultimo cliente pasados " + str(minutosPasados - minutosBancoAbierto) + " minutos de cerrado el banco.")
print("------------------------------------")
print("Clientes Preferenciales:")
print("    Tiempo de atencion promedio: " + str(np.mean(np.array(tiempoAtencionporClientePreferencial))) + " minutos")
print("    Desvio estandar: " + str(np.std(np.array(tiempoAtencionporClientePreferencial))) + " minutos")
print("    Q1: " + str(np.percentile(np.array(tiempoAtencionporClientePreferencial), 25)) + " minutos")
print("    Q3: " + str(np.percentile(np.array(tiempoAtencionporClientePreferencial), 75)) + " minutos")
print("    Peor caso: " + str(np.max(np.array(tiempoAtencionporClientePreferencial))) + " minutos")
print("    Mejor caso: " + str(np.min(np.array(tiempoAtencionporClientePreferencial))) + " minutos")
print("------------------------------------")
print("Clientes Generales:")
print("    Tiempo de atencion promedio: " + str(np.mean(np.array(tiempoAtencionporClienteGeneral))) + " minutos")
print("    Desvio estandar: " + str(np.std(np.array(tiempoAtencionporClienteGeneral))) + " minutos")
print("    Q1: " + str(np.percentile(np.array(tiempoAtencionporClienteGeneral), 25)) + " minutos")
print("    Q3: " + str(np.percentile(np.array(tiempoAtencionporClienteGeneral), 75)) + " minutos")
print("    Peor caso: " + str(np.max(np.array(tiempoAtencionporClienteGeneral))) + " minutos")
print("    Mejor caso: " + str(np.min(np.array(tiempoAtencionporClienteGeneral))) + " minutos")
print("------------------------------------")

#Graficamos como fue evolucionando por minuto.
timeAxis = []
for index in range(0, len(estadoFilaGenerales[0])):
    timeAxis.append(convert_from_minutes(index))

dates = matdate.date2num(timeAxis)

fig, ax = plt.subplots()

for index in range(0, numeroCajasGenerales):
    ax.plot_date(dates, estadoFilaGenerales[index], linestyle='-', marker=None, label="Caja general " + str(index))

for index in range(0, numeroCajasPreferenciales):
    ax.plot_date(dates, estadoFilaPreferenciales[index], linestyle='-', marker=None, label="Caja preferencial " + str(index))

ax.xaxis.set_major_formatter(matdate.DateFormatter('%H:%M'))
ax.legend()
plt.title("Clientes por caja")
plt.xlabel("Horario")
plt.ylabel("Clientes en fila")

plt.show()
