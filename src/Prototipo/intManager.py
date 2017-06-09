#!/usr/bin/env python
# -*- coding: utf-8 -*-s
from Prototipo.interrupciones import New, IoIn, IoOut, Kill, TimeOut, CompactMemory

class IntManager:
    def __init__(self):
        self._irq = {}

    def setInterruptions(self, loader, dispatcher, scheduler, pcbTable, deviceManager, memoryManager, timer):
        self.register("NEW", New(loader, dispatcher, scheduler, pcbTable))
        self.register("IO_IN", IoIn(dispatcher, pcbTable, deviceManager, scheduler, timer))
        self.register("IO_OUT", IoOut(dispatcher, scheduler, pcbTable))
        self.register("KILL", Kill(loader, dispatcher, scheduler, pcbTable, timer))
        self.register("TIME_OUT", TimeOut(dispatcher, scheduler, pcbTable, timer))
        self.register("COMPACT_MEMORY", CompactMemory(dispatcher, pcbTable, memoryManager))

    def register(self, instructionName,routine):
        self._irq[instructionName]=routine

    def handle(self,instructionName,program):
        self._irq.get(instructionName).execute(program)

                
    

