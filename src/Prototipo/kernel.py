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
        self._disco            = disco
        self._pcbTable         = PCBTable()
        self._schedulerFactory = SchedulersFactory(self._pcbTable)
        self._scheduler        = self._schedulerFactory.getScheduler()
        self._intManager       = IntManager()
        self._memoryFactory    = MemoryFactory(self._pcbTable, self._intManager, disco)
        self._memory           = self._memoryFactory.getMemory()
        self._memoryManager    = self._memoryFactory.getMemoryManager()
        self._mmu              = self._memoryFactory.getMmu()
        self._loader           = self._memoryFactory.getLoader()
        self._timer            = self._schedulerFactory.getTimer(self._intManager)
        self._cpu              = Cpu(self._mmu, self._intManager)
        self._dispatcher       = Dispatcher(self._mmu, self._cpu)
        self._deviceManager    = DeviceManager(self._intManager)
        self._intManager.setInterruptions(self._loader, self._dispatcher, self._scheduler, self._pcbTable, self._deviceManager, self._memoryManager, self._timer)
        self._newPrograms      = NewPrograms(self._intManager)
        self._clock            = Clock(self._cpu, self._deviceManager, self._timer, self._newPrograms)


    #Proposito:
    #Precondicion:
    def execPrograms(self, programs, log):
        # Imprime la memoria y el memoryManager, y setea para porteriores impresiones
        self._waitTimeAndAverageReturn = WaitTimeAndAverageReturn()
        log.set(self._memoryManager, self._memory, self._dispatcher, self._intManager, self._pcbTable, self._scheduler, self._waitTimeAndAverageReturn)
        self._newPrograms.setPrograms(programs, self._waitTimeAndAverageReturn)
        # Comienza a correr el clock
        self._clock.runCpu(log)
        log.printWaitTimeAndAverageReturn()


class Kernel2(Kernel):
    def __init__(self, disco):
        self._disco = disco
        self._memory = Memory(8)
        self._pcbTable = PCBTable()
        self._intManager = IntManager()
        sizeFrame = 4
        pageReplacementAlgorithm = SecondChancePageReplacementAlgorithm()
        self._swap = Swap(sizeFrame)
        self._memoryManager = MemoryManagerPaging(self._memory, sizeFrame, self._pcbTable, self._swap, pageReplacementAlgorithm)
        self._mmu = MmuPages(self._memory, sizeFrame, self._intManager)
        self._loader = LoaderPages(self._memory, self._mmu, self._disco, self._memoryManager, self._swap)
        self._memoryManager.setLoader(self._loader)  # Es para no hacer la interrupcion swapIN (el memoryManager y el loader se conocen mutuamente)
        self._scheduler = SchedulerSJFPreemptive()
        self._timer = None
        self._cpu = Cpu(self._mmu, self._intManager)
        self._dispatcher = Dispatcher(self._mmu, self._cpu)
        self._deviceManager = DeviceManager(self._intManager)
        self._intManager.setInterruptions(self._loader, self._dispatcher, self._scheduler, self._pcbTable, self._deviceManager, self._memoryManager, self._timer)
        self._newPrograms = NewPrograms(self._intManager)
        self._clock = Clock(self._cpu, self._deviceManager, self._timer, self._newPrograms)