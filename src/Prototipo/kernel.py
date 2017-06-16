#!/usr/bin/env python
# -*- coding: utf-8 -*-s
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


class Kernel:
    def __init__(self, disco, schedulerFactory):
        self._schedulerFactory = schedulerFactory
        self._disco = disco
        self._memory = Memory(8)
        self._pcbTable = PCBTable()
        self._intmanager = IntManager()

        # ASIGNACION CONTINUA
        #self._memoryManager = MemoryManagerContinuousAssignmentFirstFit(self._memory, self._pcbTable, self._intmanager, 1) # El numero indica el moreSpace
        #self._memoryManager = MemoryManagerContinuousAssignmentWorstFit(self._memory, self._pcbTable, self._intmanager, 1) # El numero indica el moreSpace
        #self._memoryManager = MemoryManagerContinuousAssignmentBestFit(self._memory, self._pcbTable, self._intmanager, 1) # El numero indica el moreSpace
        #self._mmu = Mmu(self._memory)
        #self._loader = LoaderBlocks(self._memory, self._mmu, self._disco, self._memoryManager, None)
        ######################################################################################################################################

        # PAGINAICON
        self._sizeFrame = 4
        self._pageReplacementAlgorithm = FirstInFirstOutPageReplacementAlgorithm()
        self._swap = Swap()
        self._memoryManager = MemoryManagerPaging(self._memory, self._sizeFrame, self._pcbTable, self._swap, self._pageReplacementAlgorithm,self._intmanager)
        self._mmu = MmuPages(self._memory, self._sizeFrame, self._intmanager)
        self._loader = LoaderPages(self._memory, self._mmu, self._disco, self._memoryManager, self._swap)

        ######################################################################################################################################
        self._scheduler = self._schedulerFactory.getScheduler(self._pcbTable)
        self._timer = self._schedulerFactory.getTimer(self._intmanager)
        self._cpu = Cpu(self._mmu, self._intmanager)
        self._dispatcher = Dispatcher(self._mmu, self._cpu, self._timer)
        self._deviceManager = DeviceManager(self._intmanager)
        self._intmanager.setInterruptions(self._loader, self._dispatcher, self._scheduler, self._pcbTable, self._deviceManager, self._memoryManager, self._timer)
        self._newPrograms = NewPrograms(self._intmanager)
        self._clock = Clock(self._cpu, self._deviceManager, self._timer, self._newPrograms)



    #Carga todos los programas en la memoria y empieza a correr el clock
    def execPrograms(self, startPrograms, programs, log):
        for nameProgram in startPrograms:
            self._intmanager.handle(Irq.NEW, nameProgram)

        # Imprime la memoria y el memoryManager, y setea para porteriores impresiones
        log.initialImpression(startPrograms, self._memoryManager, self._memory, self._dispatcher, self._cpu, self._intmanager, self._pcbTable)
        self._newPrograms.setPrograms(programs)
        # Comienza a correr el clock
        self._clock.runCpu(log)



