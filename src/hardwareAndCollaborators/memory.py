#!/usr/bin/env python
# -*- coding: utf-8 -*-s
from tabulate import tabulate

class Memory:
    def __init__(self):
        self._memory = []

    # Proposito:Carga la instrucciones en la memoria.
    # Precondiccion:-
    def load(self, intrucciones):
        for i in intrucciones.getLista():
            self._memory.append(i)

    # Proposito:seatea el valor<valor> en la posicion<pos> de la memoria
    # precondiccion: Debe existir pos en la memoria
    def set_pos(self, posicion, valor):
        self._memory[posicion] = valor

    # Proposito: Retorna la instruccion del pc recibido como argumento.
    # Precondiccion: Debe existir dicha posicion en la memoria
    def get(self, posicion):
        return self._memory[posicion]

    def __repr__(self):
        return tabulate(enumerate(self._memory), tablefmt='psql')  # pretty print.
