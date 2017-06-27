#!/usr/bin/env python
# -*- coding: utf-8 -*-s

from time import sleep
from Prototipo.intManager import Irq

class Cpu:
    def __init__(self, mmu, intManager):
        self._pc            = (-1)
        self._ir            = None
        self._mmu           = mmu
        self._intManager    = intManager

    #Proposito:Hace un tick al cpu
    #Precondicion:-
    def tick(self, log):
        if (self._pc == -1):
            return

        log.setPidEjecutado() # para imprimir el pid ejecutado

        self._fetch(log)
        self._decode()
        self._execute(log)

    #Proposito:fechea una intruccion de la memoria y actualiza el pc.
    #Precondicion:debe existir dicha posicion que fechea.
    def _fetch(self, log):
        self._ir = self._mmu.fetch(self._pc, log)
        self._pc += 1

    #Proposito:Levanta una interrupcion dependiendo la si la intruccion es un exit o un io, en caso q no sea
    #          ninguna de estas no hace nada.
    #Precondicion:-
    def _decode(self):
        if self._ir.isExit():
            self._intManager.handle(Irq.KILL, None)

        elif self._ir.isIO():
            self._intManager.handle(Irq.IO_IN, self._ir)

    #Proposito:imprime por consola la intruccion y el pc de la proxima intruccion.
    #Precondicion:-
    def _execute(self, log):
        log.printExecuteCPU(self._ir, self._pc)
        sleep(0.25)

    #Proposito:setea el pc<pc>
    #Precondicion:-
    def set_pc(self, pc):
        self._pc = pc

    #Proposito:retorna el pc
    #Precondicion:-
    def get_pc(self):
        return self._pc

    #Proposito:Retorna el ir
    #Precondicion:-
    def get_ir(self):
        return self._ir

    def __repr__(self):
        return "CPU(PC={pc})".format(pc=self._pc)
        
