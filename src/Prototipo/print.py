#!/usr/bin/env python
# -*- coding: utf-8 -*-s
import logging


class Print:
    def __init__(self):
        logger = logging.getLogger()
        handler = logging.StreamHandler()
        # tail -f /tmp/myapp.log
        #handler = logging.FileHandler('C:\log\myapp.log')
        formatter = logging.Formatter('%(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
        logger.info('Starting emulator')
        self._log = logger

    def initialImpression(self, namesProgram, memoryManager, memory, dispatcher, cpu, intManager, pcbTable):
        self._memoryManager = memoryManager
        self._memory = memory
        self._dispatcher = dispatcher
        self._intManager = intManager
        self._pidEjecutado = None
        self._pcbTable = pcbTable
        for np in namesProgram:
            self.printNameProgram(np)
        self.printCpu(cpu)
        self.printMemoryAndMemoryManager()
        if self._memoryManager.isMemoryManagerPaging():
            self.printPcbTable()

    def printExecuteCPU(self, ir, pc):
        self._log.debug("Exec:  {op}  PidExec={pe:2}   PC={npc:2d}   Pid={pid:2d}".format(pe=self.getPidEjecutado(), op=ir, npc=pc, pid=self.getPidActual()))
        if ir.isExit():
            self.printMemoryManager()

    def printNameProgram(self, nameProgram):
        self._log.debug("{np}:".format(np=nameProgram))

    def printMemoryAndMemoryManager(self):
        self._log.debug(self._memory)
        self._log.debug(self)

    def setPidEjecutado(self):
        self._pidEjecutado = self._dispatcher.getPidActual()

    def getPidEjecutado(self):
        return self._pidEjecutado

    def getPidActual(self):
        return self._dispatcher.getPidActual()

    def printMemoryManager(self):
        self._log.debug(self)

    def printNewMemoryAndMemoryManager(self, nameProgram):
        self._log.debug("\nNEW: {np}".format(np = nameProgram))
        self._log.debug(self._memory)
        self._log.debug(self)

    def printCpu(self, cpu):
        self._log.debug(cpu)

    def printPageFalut(self):
        self._log.debug("Page Fault:")
        self._log.debug(self)
        self.printPcbTable()

    def forPrint(self, forPrint):
        self._log.debug("{i}".format(i=forPrint))

    def printPcbTable(self):
        for k, v in self._pcbTable.getPcbs().items():
            self._log.debug("PCB Pid={pid}, PageTable:\n{pcbTable}".format(pid=k, pcbTable=v))

    def __repr__(self):
        if self._memoryManager.isMemoryManagerPaging():
            return "\nMemoryManager_FreeFrames={free}\nSwap_FreeFrames={freeS}\n{mm}\n".format(free=self._memoryManager.sizeFreePhysicalMemory(),freeS=self._memoryManager.sizeFreeSwap() ,mm=self._memoryManager)
        else:
            return "\nFree={free}\n{mm}\n".format(free=self._memoryManager.get_Free(), mm=self._memoryManager)




