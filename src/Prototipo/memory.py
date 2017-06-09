# !/usr/bin/env python
# -*- coding: utf-8 -*-s
from tabulate import tabulate

class Memory:
    def __init__(self, size):
        self._memory = {}
        self._size = size

    # Proposito:seatea el valor<valor> en la posicion<pos> de la memoria
    # precondiccion: Debe existir pos en la memoria
    def set_pos(self, posicion, valor):
        # self._memory.insert(posicion, valor)
        self._memory[posicion] = valor

    # Proposito: Retorna la instruccion del pc recibido como argumento.
    # Precondiccion: Debe existir dicha posicion en la memoria
    def get(self, posicion):
        return self._memory.get(posicion)

    def size(self):
        return self._size

    def __repr__(self):
        res = []
        for k, v in self._memory.items():
            res.append([k, v])
        return tabulate(res, tablefmt='psql')  # pretty print.