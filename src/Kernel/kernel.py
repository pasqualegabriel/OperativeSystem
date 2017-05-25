#!/usr/bin/env python
# -*- coding: utf-8 -*-s
from SistemaClock.clock import Clock
from SistemaClock.timer import Timer
from SistemaDeInterrupciones.deviceManager import DeviceManager
from SistemaDeInterrupciones.intManager import IntManager
from SistemaDeInterrupciones.interrupciones import *
from SistemaDeProcedimientos.pcbTable import PCBTable
from SistemaDeScheduler.scheduler import *
from hardwareAndCollaborators.cpu import Cpu
from hardwareAndCollaborators.dispatcher import Dispatcher
from hardwareAndCollaborators.loader import *
from hardwareAndCollaborators.memory import Memory
from hardwareAndCollaborators.mmu import Mmu


class Kernel:
    def __init__(self, disco):
        self._disco = disco
        self._memory = Memory()
        self._mmu = Mmu(self._memory)
        self._pcbTable = PCBTable()
        self._intmanager = IntManager()
        #self._memoryManager = MemoryManagerFirstFit(self._memory, self._pcbTable, self._intmanager, 1)
        #self._memoryManager = MemoryManagerWorstFit(self._memory, self._pcbTable, self._intmanager, 1)
        self._memoryManager = MemoryManagerBestFit(self._memory, self._pcbTable, self._intmanager, 1)
        # El numero indica el moreSpace
        self._loader = Loader(self._memory, self._mmu, self._disco, self._memoryManager)
        self._cpu = Cpu(self._loader, self._intmanager)
        #self._scheduler = SchedulerFCFS()
        #self._scheduler = SchedulerPriorityPreemptive(self._pcbTable,3) # el numero indica el aging
        #self._scheduler = SchedulerRoundRobin()
        self._scheduler = SchedulerSJF()
        #self._scheduler = SchedulerSJFNonPreemptive()
        #self._scheduler = SchedulerPriorityNonPreemptive(self._pcbTable, 3) # el numero indica el aging
        self._timer = Timer(self._scheduler, self._intmanager, 3) # el numero indica el quantum del scheduler Round Robin
        self._dispatcher = Dispatcher(self._mmu, self._cpu, self._timer)
        self._deviceManager = DeviceManager(self._intmanager, self._scheduler)
        self._intmanager.register("NEW", New(self._loader, self._dispatcher, self._scheduler, self._pcbTable))
        self._intmanager.register("IO_IN", IoIn(self._dispatcher, self._pcbTable, self._deviceManager, self._scheduler, self._timer))
        self._intmanager.register("IO_OUT", IoOut(self._dispatcher, self._scheduler, self._pcbTable))
        self._intmanager.register("KILL", Kill(self._loader, self._dispatcher, self._scheduler, self._pcbTable, self._timer))
        self._intmanager.register("TIME_OUT", TimeOut(self._dispatcher, self._scheduler, self._pcbTable, self._timer))
        self._intmanager.register("COMPACT_MEMORY", CompactMemory(self._dispatcher, self._scheduler, self._pcbTable, self._memoryManager))
        self._clock = Clock(self._cpu, self._deviceManager, self._timer)

    #Carga todos los programas en la memoria y empieza a correr el clock
    def execPrograms(self, ps, log):
        for p in ps:
            self._intmanager.handle("NEW", self._loader.search_program(p))

            log.debug("{np}:".format(np=p)) # Para imprimir
        log.debug(self)       # Para imprimir
        self._cpu.setDispatcher(self._dispatcher) # Para imprimir
        self._cpu.set_kernel(self)# Para imprimir
        self._clock.set_kernel(self) # Para imprimir

        #Comienza a correr el clock y imprime a la memoria en pantalla
        self._clock.runCpu(log)

    def new(self, p, log):  # Para imprimir
        self._intmanager.handle("NEW", p)  # Para imprimir
        log.debug("NEW: {np}".format(np=p.name()))  # Para imprimir
        log.debug(self)                   # Para imprimir

    def __repr__(self):
        return "{cpu}\n{mem}\nFree={free}\n{mm}\n{l}".format(cpu=self._cpu, mem=self._memory, free=self._loader.getMM().get_Free(), mm=self._loader.getMM(), l=self._loader)
