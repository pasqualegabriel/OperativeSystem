#!/usr/bin/env python
# -*- coding: utf-8 -*-s

import unittest
import mock

from Prototipo.disco import Disco
from Prototipo.instructions import *
from Prototipo.intManager import IntManager
from Prototipo.loader import *
from Prototipo.memory import *
from Prototipo.memoryManagerContinuousAssignment import MemoryManagerContinuousAssignmentFirstFit
from Prototipo.mmu import Mmu
from Prototipo.pcb import PCB
from Prototipo.pcbTable import PCBTable
from Prototipo.program import Program


class MyTestCase(unittest.TestCase):
    def setUp(self):

        # Se crea al pcbTable
        self._pcbTable = PCBTable()

        # Se crea el pcb del primer programa
        self._program1 = Program("so.exe", [CPU(10)], 2)
        self._PCBProgram1=PCB(0)

        # Se crea el pcb del segundo programa
        self._program2 = Program("exel.exe", [IO(1),CPU(9)], 1)
        self._PCBProgram2 = PCB(1)

        # Se crea el pcb del tercer programa
        self._program3 = Program("paint.exe", [CPU(10)], 3)
        self._PCBProgram3 = PCB(2)

        # Se crea el pcb del cuarto programa
        self._program4 = Program("word.exe", [CPU(10)], 2)
        self._PCBProgram4 = PCB(3)

        # Se crea el pcb del quint programa
        self._program5 = Program("pycharm.exe", [CPU(10)], 2)
        self._PCBProgram5 = PCB(4)

        # Se crea el pcb del sexto programa
        self._program6 = Program("pharo.exe", [CPU(60)], 2)
        self._PCBProgram6 = PCB(5)

        self._pcbTable.addPCB(self._PCBProgram1)
        self._pcbTable.addPCB(self._PCBProgram2)
        self._pcbTable.addPCB(self._PCBProgram3)
        self._pcbTable.addPCB(self._PCBProgram4)
        self._pcbTable.addPCB(self._PCBProgram5)
        self._pcbTable.addPCB(self._PCBProgram6)

        # Se inicializa la memoria
        self._memory = Memory(100)

        # Se cargan los gprogramas al disco
        self._disk = Disco()
        ls = [self._program1, self._program2, "so.pdf", self._program3, self._program4, self._program5, self._program6]
        self._disk.add_files(ls)

        # Se inicializa el intManager, memoryManager, y el Loader
        self._intmanager = IntManager()
        self._memoryManager = MemoryManagerContinuousAssignmentFirstFit(self._memory, self._pcbTable, self._intmanager, 2)
        self._loader = LoaderBlocks(self._memory, Mmu(self._memory), self._disk, self._memoryManager, mock.Mock())
        self._intmanager.setInterruptions(self._loader, mock.Mock(), mock.Mock(), self._pcbTable,
                                          mock.Mock(), self._memoryManager, mock.Mock())

        # Se cargan cinco programas a memoria
        self._loader.load(self._PCBProgram1, self._program1.name())
        self._loader.load(self._PCBProgram2, self._program2.name())
        self._loader.load(self._PCBProgram3, self._program3.name())
        self._loader.load(self._PCBProgram4, self._program4.name())
        self._loader.load(self._PCBProgram5, self._program5.name())

    def testCompactacion(self):
        self.assertEqual(1, len(self._memoryManager.getBl()))
        self.assertEqual(5, len(self._memoryManager.getBu()))
        self._loader.freeMemory(self._PCBProgram1)
        self._loader.freeMemory(self._PCBProgram4)
        self.assertEqual(3, len(self._memoryManager.getBl()))
        self.assertEqual(3, len(self._memoryManager.getBu()))
        self.assertFalse(self._memoryManager.thereIsBlockForProgram(60))
        self.assertFalse(self._memory.get(0).isIO())
        self.assertEqual(67, self._memoryManager.get_Free())

        # compacta
        self._loader.load(self._PCBProgram6, self._program6.name())

        self.assertTrue(self._memory.get(0).isIO())
        self.assertEqual(1, len(self._memoryManager.getBl()))
        self.assertEqual(4, len(self._memoryManager.getBu()))
        self.assertEqual(6, self._memoryManager.get_Free())

    def testCompactacion2(self):
        self.assertEqual(5, len(self._loader.getMemoryManager().getBu()))
        self.assertEquals(1, len(self._loader.getMemoryManager().getBl()))
        self._loader.freeMemory(self._PCBProgram1)
        self._loader.freeMemory(self._PCBProgram4)
        sizeAntesCompac= self._memoryManager.get_Free()
        self.assertEqual(3, len(self._memoryManager.getBl()))
        self.assertEqual(3, len(self._memoryManager.getBu()))
        self._memoryManager.toCompact()
        self.assertEqual(1, len(self._memoryManager.getBl()))
        self.assertEqual(3, len(self._memoryManager.getBu()))
        sizeDepuesCompac=self._memoryManager.get_Free()
        self.assertTrue(self._memory.get(0).isIO())
        self.assertEqual(sizeAntesCompac,sizeDepuesCompac)

if __name__ == "__main__":
    unittest.main()