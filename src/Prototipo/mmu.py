#!/usr/bin/env python
# -*- coding: utf-8 -*-s

# Representa al Memory Management Unit (Unidad de Administración de Memoria) del sistema
# Colaboradores internos bd y limit
# El MMU se ecarga de proporcionar al cpu el bd y verificar el limit del proceso actual
from Prototipo.intManager import Irq


class Mmu:
    def __init__(self, memory):
        self._bd     = 0
        self._limit  = 0
        self._memory = memory

    # Proposito: retorna la instruccion de dicha posicion en memoria y verifica que no se pase del limite.
    # Precondiccion:debe existir dicha posicion en memoria.
    def fetch(self, pc, log):
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

    def setPosition(self, pcb):
        self._bd = pcb.get_bd()
        self._limit = pcb.get_limit()

class MmuPages:
    def __init__(self, memory, sizeFrame, intmanager):
        self._memory     = memory
        self._sizeFrame  = sizeFrame
        self._intmanager = intmanager
        #self._usedPages = None

    def fetch(self, pc, log):

        pageNumber = divmod(pc, self._sizeFrame)[0]
        pageOffset = divmod(pc, self._sizeFrame)[1]

        page = self._usedPages.getPage(pageNumber)

        if page.isInSwapOrDisk():
            self._intmanager.handle(Irq.PAGE_FAULT, page)
            log.printPageFalut()

        return self._memory.get(page.getBDPhysicalMemory() + pageOffset)


    def setPosition(self, pcb):
        self._usedPages = pcb.getPageTable()

    def setPosition2(self, pageTablet):
        self._usedPages = pageTablet