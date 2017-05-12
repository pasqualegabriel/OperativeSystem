#!/usr/bin/env python
# -*- coding: utf-8 -*-s

class Loader:
    def __init__(self, memoria, disco):
        self._memory = memoria
        self._disco = disco
        self._bd = 0
        self._limit = (-1)

    # Proposito: carga una lista de instrucciones en la memoria, guarda el bd, el limit
    # y suma un procedimiento a la memoria.
    # Precondiccion:-
    def cargarInMemory(self, instrucciones):
        self._limit += instrucciones.longitud()
        self._bd += instrucciones.longitud()
        self._memory.load(instrucciones)

    def search_program(self, name):
        for p in self._disco.files():
            try:
                if(p.isProgram() and p.name()==name):
                    return p
            except:
                pass

    # Proposito: retorna el bd
    # Precondiccion: -
    @property
    def get_bd(self):
        return self._bd

    # Proposito:retorna el limit
    # Precondiccion:-
    @property
    def get_limit(self):
        return self._limit

    # Proposito:setea las posiciones de la memoria del programa, la pone en null
    # y resta un procedimiento a la memoria
    # Precondiccion: Existen las posiciones en la memoria
    def liberarMemoria(self, bd, limit):
        for i in range(bd, limit + 1):
            self._memory.set_pos(i, "")