#!/usr/bin/env python
# -*- coding: utf-8 -*-s
from tabulate import tabulate

from Prototipo.memory import Memory
from Prototipo.frame import Frame


class Swap:
    def __init__(self, size):
        self._virtualMemory    = {}
        self._size             = size

    # Proposito:seatea el valor<valor> en la posicion<position> de la memoria
    # precondiccion:-
    def setPos(self, position, valor):
        self._virtualMemory[position] = valor

    # Proposito: Retorna el elemento que se encuentra en dicha posicion<position>
    # Precondiccion: Debe existir dicha posicion en la memoria.
    def get(self, position):
        return self._virtualMemory.get(position)


    #Proposito:Retorna el tamaño del swap
    #Proposito:-
    def size(self):
        return self._size

    def __repr__(self):
        return ""

