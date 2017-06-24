#!/usr/bin/env python
# -*- coding: utf-8 -*-s
from Prototipo.Schedulers.SchedulersFactory import *
from Prototipo.memoryFactory import MemoryFactory
from Prototipo.memoryManagerContinuousAssignment import *
from Prototipo.swap import Swap
from Prototipo.newProgram import NewPrograms
from Prototipo.clock import Clock
from Prototipo.cpu import Cpu
from Prototipo.deviceManager import DeviceManager
from Prototipo.dispatcher import Dispatcher
from Prototipo.intManager import *
from Prototipo.loader import *
from Prototipo.memory import *
from Prototipo.memoryManagerPaging import *
from Prototipo.mmu import *
from Prototipo.pcbTable import PCBTable
from Prototipo.print import *

class Kernel:
    def __init__(self, disco):
        self._disco = disco
        self._pcbTable = PCBTable()
        self._schedulerFactory = SchedulersFactory(self._pcbTable)
        self._scheduler = self._schedulerFactory.getScheduler()
        self._intmanager = IntManager()
        self._memoryFactory = MemoryFactory(self._pcbTable, self._intmanager, disco)
        self._memory = self._memoryFactory.getMemory()
        self._memoryManager = self._memoryFactory.getMemoryManager()
        self._mmu = self._memoryFactory.getMmu()
        self._loader = self._memoryFactory.getLoader()
        self._timer = self._schedulerFactory.getTimer(self._intmanager)
        self._cpu = Cpu(self._mmu, self._intmanager)
        self._dispatcher = Dispatcher(self._mmu, self._cpu)
        self._deviceManager = DeviceManager(self._intmanager)
        self._intmanager.setInterruptions(self._loader, self._dispatcher, self._scheduler, self._pcbTable, self._deviceManager, self._memoryManager, self._timer)
        self._newPrograms = NewPrograms(self._intmanager)
        self._clock = Clock(self._cpu, self._deviceManager, self._timer, self._newPrograms)



    def execPrograms(self, programs, log):
        # Imprime la memoria y el memoryManager, y setea para porteriores impresiones
        self._waitTimeAndAverageReturn = WaitTimeAndAverageReturn()
        log.set(self._memoryManager, self._memory, self._dispatcher, self._intmanager, self._pcbTable, self._scheduler, self._waitTimeAndAverageReturn)
        self._newPrograms.setPrograms(programs, self._waitTimeAndAverageReturn)
        # Comienza a correr el clock
        self._clock.runCpu(log)
        log.printWaitTimeAndAverageReturn()