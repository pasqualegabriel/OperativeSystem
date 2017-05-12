#!/usr/bin/env python
# -*- coding: utf-8 -*-s
import unittest

from SistemaDeProgramas.instructions import *
from SistemaDeProgramas.program import Program
from hardwareAndCollaborators.memory import Memory
from hardwareAndCollaborators.mmu import Mmu

p = Program("Exel.exe", [CPU(2), CPU(1), CPU(2)],1)
m = Memory()
m.load(p)
mmu = Mmu(m)
mmu.set_bd(0)
mmu.set_limit(3)


class tester(unittest.TestCase):
    def test_1(self):
        self.assertEqual(0, mmu.get_bd())
        self.assertEqual(3, mmu.get_limit())


if __name__ == "__main__":
    unittest.main()
