# !/usr/bin/env python
# -*- coding: utf-8 -*-s
from tabulate import tabulate

class Memory:
    def __init__(self, size):
        self._memory = {}
        self._size = size

    # Proposito:En la key<position> setea el value<value>.
    # precondiccion:-
    def setPos(self, position, value):
        self._memory[position] = value

    # Proposito:retorna el value que esta guardado en la key<position>
    # Precondiccion: Debe existir dicha key<position> en la memory.
    def get(self, position):
        return self._memory.get(position)

    #Proposito:Retorna el tamaño de la memoria
    #Proposito:-
    def size(self):
        return self._size

    def __repr__(self):
        res = []
        for k, v in self._memory.items():
            res.append([k, v])
        if len(res) == 0:
            return "Physical Memory is Empty"
        return tabulate(res, tablefmt='psql')  # pretty print.

