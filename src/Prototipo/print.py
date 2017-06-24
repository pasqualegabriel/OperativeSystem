#!/usr/bin/env python
# -*- coding: utf-8 -*-s
import logging

from tabulate import tabulate


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

    def set(self, memoryManager, memory, dispatcher, intManager, pcbTable, scheduler, waitTimeAndAverageReturn):
        self._memoryManager = memoryManager
        self._memory = memory
        self._dispatcher = dispatcher
        self._intManager = intManager
        self._pidEjecutado = None
        self._pcbTable = pcbTable
        self._scheduler = scheduler
        self._cantPageFault = 0
        self._waitTimeAndAverageReturn = waitTimeAndAverageReturn

    def printExecuteCPU(self, ir, pc):
        self._log.debug("Exec:  {op}  PidExec={pe:2}   PC={npc:2d}   Pid={pid:2d}   {s}".format(pe=self.getPidEjecutado(), op=ir, npc=pc, pid=self.getPidActual(), s=self._scheduler))
        if ir.isExit():
            self.printMemoryManager()

    def printNameProgram(self, nameProgram):
        self._log.debug("{np}:".format(np=nameProgram))

    def printMemoryAndMemoryManager(self):
        self._log.debug(self._memory)
        self._log.debug(self)

    def setPidEjecutado(self):
        self._pidEjecutado = self._dispatcher.getPidActual()
        self._waitTimeAndAverageReturn.update(self._scheduler.list())

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
        self._cantPageFault += 1
        self._log.debug("Page Fault:")
        self._log.debug(self)
        self.printPcbTable()

    def forPrint(self, forPrint):
        self._log.debug("{i}".format(i=forPrint))

    def printWaitTimeAndAverageReturn(self):
        self._log.debug(self._waitTimeAndAverageReturn)
        self._log.debug("\nAverage Return: {result}".format(result=self._waitTimeAndAverageReturn.calculateAverageReturn()))
        if self._memoryManager.isMemoryManagerPaging():
            self._log.debug("\nNumber of page faults: {cpf}".format(cpf=self._cantPageFault))

    def printPcbTable(self):
        for k, v in self._pcbTable.getPcbs().items():
            self._log.debug(v)
        self._log.debug("")


    def __repr__(self):
        if self._memoryManager.isMemoryManagerPaging():
            return "\n{mm}\n".format(free=self._memoryManager.sizeFreePhysicalMemory(),freeS=self._memoryManager.sizeFreeSwap() ,mm=self._memoryManager)
        else:
            return "\n{mm}\n".format(mm=self._memoryManager)


class WaitTimeAndAverageReturn:
    def __init__(self):
        self._waitingTimes = {}
        self._cantPrograms = 0

    def addPid(self, pid):
        self._waitingTimes[pid] = 0
        self._cantPrograms += 1

    def calculateAverageReturn(self):
        return self.totalWaitingTimes() / self._cantPrograms

    def update(self, pids):
        for pid in pids:
            waitingTimes = self._waitingTimes.get(pid) + 1
            self._waitingTimes[pid] = waitingTimes

    def totalWaitingTimes(self):
        res = 0
        for k, v in self._waitingTimes.items():
            res += v
        return res

    def __repr__(self):
        res = []
        for k, v in self._waitingTimes.items():
            res.append([k, v])
        return tabulate(res, headers=["Pid","WaitTime"], tablefmt='psql')


