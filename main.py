#!/usr/bin/env python
import random

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
            print("Abriendo caja")
            self.apertura = True
        else:
            print("Caja ya abierta")

    def cerrarcaja(self):
        """Metodo que cierra una fila/caja"""
        if self.apertura == True:
            print("Cerrando caja")
            self.enfila = 0
            self.fila = []
            self.apertura = False
        else:
            print("Caja ya cerrada")

class FilaPreferencial(Fila):
    """Clase de la fila de los clientes preferenciales"""

    def insertar(self, cliente):
        """Inserta un nuevo cliente en la fila preferencial"""
        if (cliente.categoria == "Preferencial"):
            print("Cliente agregado a la fila preferencial")
            self.enfila+=1
            self.fila.append(cliente)
        else:
            print("Cliente no preferencial, debe agregarse a fila no preferncial o cambiar de categoria")

    def atender(self):
        """Atiende al proximo cliente prederencial"""
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
            else:
                print("Caja ya abierta, abra otra caja o si no hay mas cajas, no se puede hacer nada") #Si la caja esta abierta, avisa que la caja esta abierta
        else:
            print("No hay suficiente clientes como para abrir una nueva fila")

class FilaGeneral(Fila):
    """Clase que mantiene una fila de clientes no preferenciales"""

    def insertar(self, cliente):
        """Inserta un nuevo cliente en la fila no preferencial"""
        if (cliente.categoria != "Preferencial"):
            print("Cliente agregado a la fila general")
            self.enfila+=1
            self.fila.append(cliente)
        else:
            print("Cliente preferencial, debe agregarse a fila preferencial")

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


if __name__ == "__main__":
    """ simular una fila en una entidad bancaria"""
    print("Creamos 300 clientes que van a venir al banco durante un dia")
    N = 300
    clientes = [cliente(i) for i in range(0, N)]
    #La relacion de clientes preferenciales de generales en 1 en 4, pero se va a asignar de forma aleatoria.
    #Pero ademas ese el orden de llegada de clientes al banco.
    for cliente in clientes:
        tipocliente = random.randint(0, 3) #Tiramos el dado
        if tipocliente == 3:
            cliente.modificarcategoria("Preferencial")
        else:
            cliente.modificarcategoria("General")

    #El banco cuenta con 2 cajas generales generales y 3 cajas preferenciales.
    #Las dos cajas generales estan abiertas todo el tiempo. Las cajas preferenciales se abren cuando llega una cantidad de
    #clientes que obliga a abrir una caja si es que hay disponibles. Si una caja preferencial esta vacia un cierto tiempo, se cierra.
    cajasGenerales = []
    cajasGenerales.append(FilaGeneral())
    cajasGenerales.append(FilaGeneral())
    cajasGenerales[0] .abrircaja()
    cajasGenerales[1] .abrircaja()

    cajasGeneralesAbiertas = 2

    cajasPreferenciales = []

    cajasPreferenciales.append(FilaPreferencial())
    cajasPreferenciales.append(FilaPreferencial())
    cajasPreferenciales.append(FilaPreferencial())
    cajasPreferenciales[0].abrircaja()

    cajasPreferencialesAbiertas = 1

    #Cada loop va a simular 3 minutos. Durante esos 3 minutos, puede llegar un cliente con un probabilidad del 75%
    #Durante esos 3 minutos, un cliente prefencial tiene un 50% de ser atendido
    #Durante esos 3 minutos, un cliente general tiene un 25% de ser atendido
    #Si una caja prerencial pasa 9 minutos (3 loops) sin clientes, se cierra siempre quedando al menos una abierta
    #La fila maxima preferencial por caja es de 10.

    #Vamos a medir, tiempo de espera promedio por cliente preferencial y general
    #Numero de cliente por caja

    clientesAtendidos = 0
    contadorClientes = 0

    while clientesAtendidos < N:

        #Vemos si llega un cliente
        llegoCliente = random.randint(0, 3) #Tiramos el dado

        if llegoCliente > 0:
            print(contadorClientes)
            if clientes[contadorClientes].categoria == "Preferencial": #Si el cliente es preferencial
                #Le asignamos unas de las cajas preferneciales
                cajaN = random.randint(0, cajasPreferencialesAbiertas - 1) #Tiramos el dado
                #Lo agregamos ahi
                cajasPreferenciales[cajaN].insertar(clientes[contadorClientes])
            else:
                #Le asignamos unas de las cajas generales
                cajaN = random.randint(0, cajasGeneralesAbiertas - 1) #Tiramos el dado
                #Lo agregamos ahi
                cajasGenerales[cajaN].insertar(clientes[contadorClientes])

            contadorClientes+= 1 # Aumentamos el contador de clientes que ya llegaron
            clientesAtendidos = contadorClientes

        # Vemos las cajas generales
        for index,caja in enumerate(cajasGenerales):
            #Hay clientes?
            if(caja.enfila != 0):
                atiendeN = random.randint(0, 3) #Tiramos el dado
                if (atiendeN > 2): #Si sale que si, atiende a un cliente
                    caja.atender()
                    print("Cliente antendido en caja general " + str(index))

        # Vemos las cajas preferenciales
        for index,caja in enumerate(cajasPreferenciales):
            #Esta abierta la caja?
            if(caja.apertura == True):
                #Hay clientes?
                if(caja.enfila != 0):
                    atiendeN = random.randint(0, 1) #Tiramos el dado
                    if (atiendeN > 1): #Si sale que si, atiende a un cliente
                        caja.atender()
                        print("Cliente antendido en caja prefencial " + str(index))

        # Vemos si es necesario abrir alguna nueva caja preferencial
        for caja in cajasPreferenciales:
            #Esta abierta la caja?
            if(caja.apertura == True):
                #Vemos si es necesario abrir, para ello vamos probando si queda alguna de las cajas abiertas
                for index,cajanueva in enumerate(cajasPreferenciales):
                    caja.abrircajanueva(3, cajanueva)


    print(cajasGenerales[0].enfila)
    print(cajasGenerales[1].enfila)
    print(cajasPreferenciales[0].enfila)
    print(cajasPreferenciales[1].enfila)
    print(cajasPreferenciales[2].enfila)    
