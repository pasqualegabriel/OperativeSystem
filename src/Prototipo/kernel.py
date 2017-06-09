#!/usr/bin/env python
# -*- coding: utf-8 -*-s
from Prototipo.NewProgram import NewProgram
from Prototipo.clock import Clock
from Prototipo.cpu import Cpu
from Prototipo.deviceManager import DeviceManager
from Prototipo.dispatcher import Dispatcher
from Prototipo.intManager import IntManager
from Prototipo.loader import *
from Prototipo.memory import Memory
from Prototipo.memoryManager import *
from Prototipo.mmu import *
from Prototipo.pcbTable import PCBTable
from Prototipo.timer import Timer


class Kernel:
    def __init__(self, disco, schedulerFactory):
        self._sf = schedulerFactory
        self._disco = disco
        self._memory = Memory(64)
        self._pcbTable = PCBTable()
        self._intmanager = IntManager()

        # ASIGNACION CONTINUA
        #self._memoryManager = MemoryManagerFirstFit(self._memory, self._pcbTable, self._intmanager, 1) # El numero indica el moreSpace
        #self._memoryManager = MemoryManagerWorstFit(self._memory, self._pcbTable, self._intmanager, 1) # El numero indica el moreSpace
        self._memoryManager = MemoryManagerBestFit(self._memory, self._pcbTable, self._intmanager, 1) # El numero indica el moreSpace
        self._mmu = Mmu(self._memory)
        self._loader = LoaderBlocks(self._memory, self._mmu, self._disco, self._memoryManager)

        # PAGINAICON
        #self._memoryManager = MemoryManagerPaginacion(self._memory, 4, self._pcbTable) # El numero indica el tamanio de un frame
        #self._mmu = MmuPages(self._memory, self._memoryManager.getFrame())
        #self._loader = LoaderPages(self._memory, self._mmu, self._disco, self._memoryManager)

        self._scheduler = self._sf.getScheduler(self._pcbTable)
        self._timer = Timer(self._scheduler, self._intmanager, self._sf.getQuantum()) # el numero indica el quantum del scheduler Round Robin
        self._cpu = Cpu(self._mmu, self._intmanager)
        self._dispatcher = Dispatcher(self._mmu, self._cpu, self._timer)
        self._deviceManager = DeviceManager(self._intmanager)
        self._intmanager.setInterruptions(self._loader, self._dispatcher, self._scheduler, self._pcbTable, self._deviceManager, self._memoryManager, self._timer)
        self._newProgram = NewProgram()
        self._clock = Clock(self._cpu, self._deviceManager, self._timer, self._newProgram)



    #Carga todos los programas en la memoria y empieza a correr el clock
    def execPrograms(self, ps, log):
        for nameProgram in ps:
            self._intmanager.handle("NEW", nameProgram)

        # Imprime la memoria y el memoryManager, y setea para porteriores impresiones
        log.initialImpression(ps, self._memoryManager, self._memory, self._dispatcher, self._cpu, self._intmanager)
        # Comienza a correr el clock
        self._clock.runCpu(log)



