#!/usr/bin/env python
# -*- coding: utf-8 -*-s
import unittest

from SistemaDeProgramas.instructions import *
from SistemaDeProgramas.program import Program
from hardwareAndCollaborators.loader import Loader
from hardwareAndCollaborators.memory import Memory

p = Program("exel.exe", [CPU(2), CPU(1), CPU(2)], 1)
m = Memory()
m.load(p)
l = Loader(m)
l.cargarInMemory(p)  # p.instructions()


class tester(unittest.TestCase):
    def test_1(self):
        self.assertEqual(6, l.get_bd())
        self.assertEqual(5, l.get_limit())


if __name__ == "__main__":
    unittest.main()
