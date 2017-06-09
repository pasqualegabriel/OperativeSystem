#!/usr/bin/env python
# -*- coding: utf-8 -*-s
import unittest

from Prototipo.pcb import PCB
from Prototipo.pcbTable import PCBTable

pcb1 = PCB(1)
pcb2 = PCB(2)
pcbt = PCBTable()
pcbt.addPCB(pcb1)
pcbt.addPCB(pcb2)


class tester(unittest.TestCase):
    def test_1(self):
        self.assertEqual(pcb1, pcbt.lookUpPCB(1))
        self.assertEqual(pcb2, pcbt.lookUpPCB(2))

    def test_2(self):
        pcbt.removePCB(1)
        pcbt.removePCB(2)
        self.assertEqual(True, pcbt.pcbTabletIsNill())


if __name__ == "__main__":
    unittest.main()
