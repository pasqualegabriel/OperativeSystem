#!/usr/bin/env python
# -*- coding: utf-8 -*-s

# Representa al Memory Management Unit (Unidad de Administración de Memoria) del sistema
# Colaboradores internos bd y limit
# El MMU se ecarga de proporcionar al cpu el bd y verificar el limit del proceso actual
class Mmu:
    def __init__(self, memory):
        self._bd = 0
        self._limit = 0
        self._memory = memory

    # Proposito: retorna la instruccion de dicha posicion en memoria y verifica que no se pase del limite.
    # Precondiccion:debe existir dicha posicion en memoria.
    def fetch(self, pc):
        pos = pc + self._bd # variable estetica
        if pos > self._limit:
            return
        return self._memory.get(pos)

    # Proposito: retorna el bd
    # Precondiccion: -
    def get_bd(self):
        return self._bd

    # Proposito: retorna el limit
    # Precondiccion: -
    def get_limit(self):
        return self._limit

    # Proposito: setea el bd
    # Precondiccion: -
    def set_bd(self, bd):
        self._bd = bd

    # Proposito: setea el limit
    # Precondiccion: -
    def set_limit(self, limit):
        self._limit = limit

    def isNillMmu(self):
        return self._limit == -1 and self._bd == -1



