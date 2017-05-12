#!/usr/bin/env python
# -*- coding: utf-8 -*-s
import unittest

from SistemaDeProgramas.instructions import *
from SistemaDeProgramas.program import Program
from hardwareAndCollaborators.memory import Memory

p = Program("exel.exe", [IO(2), CPU(1), CPU(2)], 1)
m = Memory()
m.load(p)


class tester(unittest.TestCase):
    # Verifica que la posicion 0 tenga el valor correcto
    def test_1(self):
        self.assertEqual(True, m.get(0).isIO())

        # Proposito:Verifico que la posicion 2 se seteo con el elemento <None>

    def test_2(self):
        self.assertEqual(True, m.get(5).isExit())
        m.set_pos(2, "")
        self.assertEqual("", m.get(2))


if __name__ == "__main__":
    unittest.main()
