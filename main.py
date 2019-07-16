#!/usr/bin/env python

class Fila(object):
    """Clase base de fila"""

    def __init__(self):
        """constructor de la clase Fila """
        self.enfila=0
        self.fila = []

class FilaPreferencial(Fila):
    """Clase de la fila de los clientes preferenciales"""

    def insertar(self, cliente):
        """Inserta un nuevo cliente en la fila preferencial"""
        if (cliente.categoria == "Preferencial"):
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
        #if (maxenfila < self.enfila):
        #    filanueva =
        pass



class FilaGeneral(Fila):
    """Clase que mantiene una fila de clientes no preferenciales"""

    def insertar(self, cliente):
        """Inserta un nuevo cliente en la fila no preferencial"""
        if (cliente.categoria != "Preferencial"):
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
    pass
