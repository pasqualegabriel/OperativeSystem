#!/usr/bin/env python
# -*- coding: utf-8 -*-s
import unittest

from mock import mock

from Prototipo.page import Page
from Prototipo.pageTable import PageTable
from Prototipo.pcb import PCB
from Prototipo.swap import Swap
from Prototipo.disco import *
from Prototipo.instructions import *
from Prototipo.intManager import IntManager
from Prototipo.loader import *
from Prototipo.memory import *

########### Programas a cargar en disco ###############
from Prototipo.memoryManagerPaging import MemoryManagerPaging, FirstInFirstOutPageReplacementAlgorithm
from Prototipo.frame import Frame
from Prototipo.mmu import MmuPages
from Prototipo.pcbTable import PCBTable
from Prototipo.program import Program

p0 = Program("SO.exe", [CPU(2)], 2)
p1 = Program("Word.exe", [CPU(4)], 1)
p2 = Program("PC.exe", [CPU(3)], 3)
p3 = Program("Text.exe", [CPU(5)], 1)

p4 = Program("paint.exe", [CPU(1)], 2)
p5 = Program("vlc.exe", [CPU(10), IO_2(3), CPU(2)], 2)
p6 = Program("sdasd",[CPU(2),IO_1(1)],1)
p7 = Program("sdasd",[CPU(1),IO_1(2)],1)
######################################################

disco = Disco()
ls = [p0, p1, p2, "so.pdf", p3, p4, p5]
disco.add_files(ls)

class MyTestCase(unittest.TestCase):
    def setUp(self):

        self._memory = Memory(64)
        self._swap = Swap(128)
        self._memoryManager = MemoryManagerPaging(self._memory, 4, mock.Mock(), self._swap, FirstInFirstOutPageReplacementAlgorithm()) # El numero indica el tamanio de un frame
        self._mmu = MmuPages(self._memory, self._memoryManager.sizeFrame(),mock.Mock())
        self._loader = LoaderPages(self._memory, self._mmu,disco, self._memoryManager, self._swap )
        self._page  =Page()
        self._pageTable=PageTable(2)
        self._pageTable.getPages()[0].setBDPhysicalMemory(0)
        self._pageTable.getPages()[0].setPhysicalMemory(True)
        self._pageTable.getPages()[1].setBDPhysicalMemory(8)
        self._pageTable.getPages()[1].setPhysicalMemory(True)
        pcb = PCB(1)
        pcb.setPages(self._pageTable)
        self._mmu.setPosition(pcb)

        self._loader.loadInPhysicalMemory(p6.instructions(),self._pageTable.getPages()[0])
        self._loader.loadInPhysicalMemory(p7.instructions(),self._pageTable.getPages()[1])

    def testMemory(self):
        self.assertTrue(self._memory.get(0).isCPU())
        self.assertTrue(self._memory.get(1).isCPU())
        self.assertTrue(self._memory.get(2).isIO())
        self.assertTrue(self._memory.get(3).isExit())

    def testMMU(self):
        self.assertTrue(self._mmu.fetch(0, mock.Mock()).isCPU())
        self.assertTrue(self._mmu.fetch(1, mock.Mock()).isCPU())
        self.assertTrue(self._mmu.fetch(2, mock.Mock()).isIO())
        self.assertTrue(self._mmu.fetch(3, mock.Mock()).isExit())
        self.assertTrue(self._mmu.fetch(4, mock.Mock()).isCPU())
        self.assertTrue(self._mmu.fetch(5, mock.Mock()).isIO())
        self.assertTrue(self._mmu.fetch(6, mock.Mock()).isIO())
        self.assertTrue(self._mmu.fetch(7, mock.Mock()).isExit())



if __name__ == '__main__':
    unittest.main()
