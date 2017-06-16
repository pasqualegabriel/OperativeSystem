#!/usr/bin/env python
# -*- coding: utf-8 -*-s

from time import sleep
from tokenize import String

from Prototipo.intManager import Irq


class Cpu:
    def __init__(self, mmu, intManager):
        self._pc  = (-1)
        self._ir  = None
        self._mmu = mmu
        self._intManager = intManager

    def tick(self, log):
        if (self._pc == -1):
            return

        log.setPidEjecutado() # para imprimir el pid ejecutado

        self._fetch(log)
        self._decode()
        self._execute(log)

    def _fetch(self, log):
        self._ir = self._mmu.fetch(self._pc, log)
        self._pc += 1

    def _decode(self):
        if (self._ir.isExit()):
            self._intManager.handle(Irq.KILL, None)

        elif (self._ir.isIO()):
            self._intManager.handle(Irq.IO_IN, self._ir)
                
    def _execute(self, log):
        log.printExecuteCPU(self._ir, self._pc)
        sleep(0.25)

    def set_pc(self, n):
        self._pc = n

    def get_pc(self):
        return self._pc

    def get_ir(self):
        return self._ir

    def __repr__(self):
        return "CPU(PC={pc})".format(pc=self._pc)
        
