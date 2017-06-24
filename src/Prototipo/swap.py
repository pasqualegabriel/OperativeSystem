#!/usr/bin/env python
# -*- coding: utf-8 -*-s
from tabulate import tabulate

from Prototipo.memory import Memory
from Prototipo.frame import Frame


class Swap:
    def __init__(self, size):
        self._virtualMemory    = {}
        self._lenVirtualMemory = 0
        self._size = size

    # Proposito:seatea el valor<valor> en la posicion<pos> de la memoria
    # precondiccion: Debe existir pos en la memoria
    def setPos(self, position, valor):
        self._virtualMemory[position] = valor

    # Proposito: Retorna la instruccion del pc recibido como argumento.
    # Precondiccion: Debe existir dicha posicion en la memoria
    def get(self, position):
        return self._virtualMemory.get(position)

    def lenVirtualMemory(self):
        return self._lenVirtualMemory

    #Proposito:Retorna el tamaño del swap
    #Proposito:-
    def size(self):
        return self._size

    def __repr__(self):
        return ""

