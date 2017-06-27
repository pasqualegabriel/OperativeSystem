#!/usr/bin/env python
# -*- coding: utf-8 -*-s
from enum import Enum

from Prototipo.interrupciones import *

class IntManager:
    def __init__(self):
        self._irq       = {}

    #Proposito:Setea todoas las interrupciones con sus respectivos atributos
    #Precondicion:-
    def setInterruptions(self, loader, dispatcher, scheduler, pcbTable, deviceManager, memoryManager, timer):
        self.register(Irq.NEW, New(loader, dispatcher, scheduler, pcbTable))
        self.register(Irq.IO_IN, IoIn(dispatcher, pcbTable, deviceManager, scheduler, timer))
        self.register(Irq.IO_OUT, IoOut(dispatcher, scheduler, pcbTable))
        self.register(Irq.KILL, Kill(loader, dispatcher, scheduler, pcbTable, timer,memoryManager))
        self.register(Irq.TIME_OUT, TimeOut(dispatcher, scheduler, pcbTable))
        self.register(Irq.COMPACT_MEMORY, CompactMemory(dispatcher, pcbTable, memoryManager))
        self.register(Irq.PAGE_FAULT, PageFault(loader, scheduler, pcbTable, dispatcher, memoryManager))
        #self.register(Irq.IN_SWAP, InSwap(loader, scheduler, pcbTable, dispatcher))
        #self.register(Irq.UPDATE_ReferenceBit, UpdateReferenceBit(memoryManager))

    #Proposito:
    #Precondicion:
    def register(self, instructionName, routine):
        self._irq[instructionName] = routine

    #Proposito:
    #Precondicion:
    def handle(self, instructionName, parameter):
        self._irq.get(instructionName).execute(parameter)


class Irq(Enum):
    NEW                 = 1
    IO_IN               = 2
    IO_OUT              = 3
    KILL                = 4
    TIME_OUT            = 5
    COMPACT_MEMORY      = 6
    PAGE_FAULT          = 7
    #IN_SWAP             = 8
    #UPDATE_ReferenceBit = 9

                
    

