#!/usr/bin/env python
# -*- coding: utf-8 -*-s
from Prototipo.intManager import Irq

class NewPrograms:
    def __init__(self, intManager):
        self._intManager = intManager
        self._programs = None
        self._proxProgram = None
        self._proxStart = None

    def tick(self, count, log):
        if count == self._proxStart:
            self._intManager.handle(Irq.NEW, self._proxProgram)
            log.printNewMemoryAndMemoryManager(self._proxProgram)
            self.updateNextProgram()

    def setPrograms(self, programs):
        self._programs = programs
        self.updateNextProgram()

    def updateNextProgram(self):
        if len(self._programs) > 0:
            firstProgram = self._programs[0]
            self._proxProgram = firstProgram[1]
            self._proxStart = firstProgram[0]
            self._programs.remove(firstProgram)

    def getPrograms(self):
        return self._programs

    def getProxProgram(self):
        return self._proxProgram

    def getProxStart(self):
        return self._proxStart





