#!/usr/bin/env python
# -*- coding: utf-8 -*-s

from time import sleep




class Cpu:
    def __init__(self, mmu, intManager):
        self._pc = (-1)
        self._ir = None
        self._mmu = mmu
        self._intManager = intManager
        self._dispatcher = None
        self._PCBTablet=None


    def tick(self, log):
        if (self._pc == -1):
            return

        self._fetch()
        self._decode()
        self._execute(log)


    def _fetch(self):
        self._ir = self._mmu.fetch(self._pc)
        self._pc += 1


    def _decode(self):
        if (self._ir.isExit()):
            self._intManager.handle("KILL", None)
            

        elif (self._ir.isIO()):
            self._intManager.handle("IO_IN", None)
                


    def _execute(self, log):
        p=self._dispatcher.get_PidActual()
        log.debug("Exec: {op}, PC={pc}, Pid={pid}".format(op=self._ir,pc=self._pc, pid=p))
        sleep(0.25)


    def set_pc(self, n):
        self._pc = n


    def get_pc(self):
        return self._pc




    def get_ir(self):
        return self._ir

    def setDispatcher(self, dispatcher):
        self._dispatcher = dispatcher


    def __repr__(self):
        return "CPU(PC={pc})".format(pc=self._pc)
        
