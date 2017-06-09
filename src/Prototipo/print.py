#!/usr/bin/env python
# -*- coding: utf-8 -*-s
import logging

class Print:
    def __init__(self):
        logger = logging.getLogger()
        handler = logging.StreamHandler()
        # tail -f /tmp/myapp.log
        #handler = logging.FileHandler('/tmp/myapp.log')
        formatter = logging.Formatter('%(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
        logger.info('Starting emulator')
        self._log = logger

    def initialImpression(self, namesProgram, memoryManager, memory, dispatcher, cpu, intManager):
        self._memoryManager = memoryManager
        self._memory = memory
        self._dispatcher = dispatcher
        self._intManager = intManager
        for np in namesProgram:
            self.printNameProgram(np)
        self.printCpu(cpu)
        self.printMemoryAndMemoryManager()

    def printExecuteCPU(self, ir, pc):
        self._log.debug("Exec: {op}, PidExec={pe},  PC={npc}, Pid={pid}".format(pe=self.getPidEjecutado(), op=ir, npc=pc, pid=self.getPidActual()))
        if ir.isExit():
            self.printMemoryManager()

    def printNameProgram(self, nameProgram):
        self._log.debug("{np}:".format(np=nameProgram))

    def printMemoryAndMemoryManager(self):
        self._log.debug(self._memory)
        self._log.debug(self)

    def setPidEjecutado(self):
        self._pidEjecutado = self._dispatcher.get_PidActual()

    def getPidEjecutado(self):
        return self._pidEjecutado

    def getPidActual(self):
        return self._dispatcher.get_PidActual()

    def printMemoryManager(self):
        self._log.debug(self)

    def printNewMemoryAndMemoryManager(self, nameProgram):
        self._log.debug("NEW: {np}".format(np = nameProgram))
        self._log.debug(self._memory)
        self._log.debug(self)

    def printCpu(self, cpu):
        self._log.debug(cpu)

    def forPrint(self, forPrint):
        self._log.debug("{i}".format(i=forPrint))

    def getIntManager(self):
        return self._intManager

    def __repr__(self):
        if self._memoryManager.isMemoryManagerPaging():
            return "\nFreePages={free}\n{mm}\n".format(free=self._memoryManager.sizeFree(),mm=self._memoryManager)
        else:
            return "\nFree={free}\n{mm}\n".format(free=self._memoryManager.get_Free(), mm=self._memoryManager)


