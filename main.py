#!/usr/bin/env python

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
    print("hola")

    pass
