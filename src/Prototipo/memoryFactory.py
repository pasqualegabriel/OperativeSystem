#!/usr/bin/env python
# -*- coding: utf-8 -*-s
from Prototipo.loader import LoaderBlocks, LoaderPages
from Prototipo.memory import Memory
from Prototipo.memoryManagerContinuousAssignment import *
from Prototipo.memoryManagerPaging import *
from Prototipo.mmu import Mmu, MmuPages
from Prototipo.swap import Swap


class MemoryFactory:
    def __init__(self, pcbTable, intManager, disco):
        self._pcbTable   = pcbTable
        self._intManager = intManager
        self.initializePageReplacementAlgorithms()
        self._idMemory   = int(input("Choise Memory:\n1 Continuous Assignment\n2 Paging\n".format()))
        self._sizeMemory = int(input("Size Memory:\n".format()))
        self._memory     = Memory(self._sizeMemory)
        self._swap       = Swap(self._memory.size())
        self._sizeFrame  = 4
        self.initializeMemoryManagerContinuousAssignment()
        self.initializeMemoryManagerPaging()
        self.initializeMmu()
        self.initializeLoader(disco)

    def initializeLoader(self, disco):
        self._loaderPages = LoaderPages( self._memory, self.getMmu(), disco, self.getMemoryManager(), self._swap)
        if self._idMemory == 2:
            self._memoryManager.setLoader(self._loaderPages)
        self._loaders = {1: LoaderBlocks(self._memory, self.getMmu(), disco, self.getMemoryManager()),
                         2: self._loaderPages}

    def initializeMmu(self):
        self._mmu = {1: Mmu(self._memory),
                     2: MmuPages(self._memory, self._sizeFrame, self._intManager)}

    def initializeMemoryManagerPaging(self):
        if self._idMemory == 2:
            self._idPageReplacementAlgorithm = int(input(
                "Choise Page Replacement Algorithm:\n1 First In First Out\n2 Second Chance\n3 Clock\n".format()))
            self._memoryManager = MemoryManagerPaging(self._memory, self._sizeFrame, self._pcbTable, self._swap,
                                                      self._pageReplacementAlgorithm.get(self._idPageReplacementAlgorithm))

    def initializeMemoryManagerContinuousAssignment(self):
        if self._idMemory == 1:
            self.idMemoryManager = int(input(
                "Choise Memory Manager:\n1 Continuous Assignment First Fit\n2 Continuous Assignment Best Fit\n3 Continuous Assignment Worst Fit\n".format()))
            self._memoryManagerContinuousAssignment = {
                1: MemoryManagerContinuousAssignmentFirstFit(self._memory, self._pcbTable, self._intManager, 1),
                2: MemoryManagerContinuousAssignmentBestFit(self._memory, self._pcbTable, self._intManager, 1),
                3: MemoryManagerContinuousAssignmentWorstFit(self._memory, self._pcbTable, self._intManager, 1)}
            self._memoryManager = self._memoryManagerContinuousAssignment.get(self.idMemoryManager)

    def initializePageReplacementAlgorithms(self):
        self._pageReplacementAlgorithm = {1: FirstInFirstOutPageReplacementAlgorithm(),
                                          2: SecondChancePageReplacementAlgorithm(),
                                          3: ClockPageReplacementAlgorithm()}


    def getMemoryManager(self):
        return self._memoryManager

    def getMmu(self):
        return self._mmu.get(self._idMemory)

    def getLoader(self):
        return self._loaders.get(self._idMemory)

    def getMemory(self):
        return self._memory