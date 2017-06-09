import unittest

from Prototipo.memoryManager import MemoryManagerPaginacion
from Prototipo.memory import Memory
from Prototipo.pcbTable import PCBTable


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self._mm = MemoryManagerPaginacion(Memory(24), 4, PCBTable())

    def testMemory(self):
        self.assertEquals(6, self._mm.sizeFree())