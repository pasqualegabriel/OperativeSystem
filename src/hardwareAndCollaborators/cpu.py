#!/usr/bin/env python
# -*- coding: utf-8 -*-s

from time import sleep

class Cpu:
    def __init__(self, loader, intManager):
        self._pc = (-1)
        self._ir = None
        self._loader = loader
        self._intManager = intManager

        self._dispatcher = None # para imprimir
        self.pidEjecutado = None # para imprimir
        self._kernel = None # para imprimir

    def tick(self, log):
        if (self._pc == -1):
            return

        # Solo para imprimir
        self.pidEjecutado = self._dispatcher.get_PidActual() # para imprimir

        self._fetch()
        self._decode()
        self._execute(log)

    def _fetch(self):
        self._ir = self._loader.fetch(self._pc)
        self._pc += 1

    def _decode(self):
        if (self._ir.isExit()):
            self._intManager.handle("KILL", None)

        elif (self._ir.isIO()):
            self._intManager.handle("IO_IN", None)
                
    def _execute(self, log):
        log.debug("Exec: {op}, PidExec={pe},  PC={pc}, Pid={pid}".format(pe=self.pidEjecutado ,op=self._ir, pc=self._pc, pid=self._dispatcher.get_PidActual()))
        sleep(0.25)

        if (self._ir.isExit()): # para imprimir
            log.debug(self._kernel) # para imprimir

    def set_pc(self, n):
        self._pc = n

    def get_pc(self):
        return self._pc

    def get_ir(self):
        return self._ir

    def set_kernel(self,kernel): # para imprimir
        self._kernel = kernel # para imprimir

    def setDispatcher(self, dispatcher): # para imprimir
        self._dispatcher = dispatcher # para imprimir

    def __repr__(self):
        return "CPU(PC={pc})".format(pc=self._pc)
        
