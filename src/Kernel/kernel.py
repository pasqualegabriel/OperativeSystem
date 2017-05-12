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
from hardwareAndCollaborators.loader import Loader
from hardwareAndCollaborators.memory import Memory
from hardwareAndCollaborators.mmu import Mmu


class Kernel:
    def __init__(self, disco):
        self._disco = disco
        self._memory = Memory()
        self._mmu = Mmu(self._memory)
        self._loader = Loader(self._memory, self._disco)
        self._pcbTable = PCBTable()
        self._intmanager = IntManager()
        self._cpu = Cpu(self._mmu, self._intmanager)
        #self._scheduler = SchedulerFIFO()
        #self._scheduler = SchedulerPriorityPreventive(self._pcbTable)
        #self._scheduler = SchedulerRoundRobin() #FUNCIONA
        self._scheduler = SchedulerSJF() #FUNCIONA
        self._timer = Timer(self._scheduler, self._cpu)
        self._dispatcher = Dispatcher(self._mmu, self._cpu, self._timer)
        self._deviceManager = DeviceManager(self._intmanager, self._scheduler)
        self._intmanager.register("NEW",
                                  New(self._loader, self._dispatcher, self._scheduler, self._pcbTable))
        self._intmanager.register("IO_IN", IoIn(self._loader, self._dispatcher, self._pcbTable, self._deviceManager,
                                                self._scheduler))
        self._intmanager.register("IO_OUT", IoEnd(self._loader, self._dispatcher, self._deviceManager, self._scheduler,
                                                  self._pcbTable))
        self._intmanager.register("KILL", Kill(self._loader, self._dispatcher, self._scheduler, self._pcbTable))
        self._intmanager.register("TIME_OUT",
                                  TimeOut(self._loader, self._dispatcher, self._deviceManager, self._scheduler,
                                          self._pcbTable))
        self._clock = Clock(self._cpu, self._deviceManager, self._timer, self._intmanager)


    def execPrograms(self, ps, log):
        for p in ps:
            self._intmanager.handle("NEW", self._loader.search_program(p))
            print()
            print(p)
            log.debug(self)
        self._cpu.setDispatcher(self._dispatcher)

        self.exec(log)


    def exec(self, log):
        self._clock.runCpu(log)
        log.debug(self)


    def __repr__(self):
        return "{cpu}\n{mem}".format(cpu=self._cpu, mem=self._memory)
