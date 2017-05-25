import unittest

from SistemaDeProcedimientos.pcb import PCB
from SistemaDeProgramas.program import Program
from SistemaDeProgramas.instructions import *
from hardwareAndCollaborators.disco import Disco
from hardwareAndCollaborators.loader import *
from hardwareAndCollaborators.memory import *


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self._mm = MemoryManagerFirstFit(Memory())

        self._block1 = Block(0, 9, 0)
        self._block2 = Block(10, 24, 1)
        self._block3 = Block(25, 44, 2)
        self._block4 = Block(45, 54, 3)
        self._block5 = Block(55, 64, 4)

        self._mm.getBu().append(self._block4)
        self._mm.getBu().append(self._block3)
        self._mm.getBu().append(self._block1)
        self._mm.getBu().append(self._block5)
        self._mm.getBu().append(self._block2)
        self._mm.orderingBu()

    def testMemory(self):
        self.assertEquals([self._block1, self._block2, self._block3, self._block4, self._block5], self._mm.getBu())