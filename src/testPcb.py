#!/usr/bin/env python
# -*- coding: utf-8 -*-s
import unittest

from Prototipo.pcb import PCB




class tester(unittest.TestCase):
    def setUp(self):
        self._pcbTest = PCB(1)
        self._pcbTest.set_bd(4)
        self._pcbTest.set_status("new")
        self._pcbTest.set_limit(5)
        self._pcbTest.set_priority(1)
        self._pcbTest.set_bursts([2,1])

    def test0000(self):
        self.assertEqual(1, self._pcbTest.get_pid())
        self.assertEqual(5, self._pcbTest.get_limit())
        self.assertEqual("new", self._pcbTest.get_status())
        self.assertEqual(4, self._pcbTest.get_bd())
        self.assertEqual(1,self._pcbTest.get_priority())
        self.assertEqual([2,1],self._pcbTest.get_bursts())
        self.assertEqual(2,self._pcbTest.get_headBurst())
        #el headBurst solo saca el elemento lo vuelve a poner y te lo retorna por eso en la segunda sigue siendo 2.
        self.assertEqual(2,self._pcbTest.get_headBurst())
        self.assertEqual(2,self._pcbTest.get_burst())
        self.assertEqual(2,self._pcbTest.get_burst())

    def test0001(self):
        self._pcbTest.set_pc(2)
        self.assertEqual(1, self._pcbTest.get_burst())

if __name__ == "__main__":
    unittest.main()
