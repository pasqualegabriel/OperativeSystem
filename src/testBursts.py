#!/usr/bin/env python
# -*- coding: utf-8 -*-s

import unittest

from Prototipo.Schedulers.bursts import Bursts
from Prototipo.instructions import *
from Prototipo.program import Program

class tester(unittest.TestCase):
    def setUp(self):
        self._programTestOne=Program("so.exe", [CPU(2), CPU(1)], 1)
        self._programTestTwo=Program("pc.exe", [CPU(2), CPU(2), IO(1),CPU(2),IO(3),CPU(1)], 2)
        self._burstTestOne=Bursts(self._programTestOne)
        self._burstTestTwo=Bursts(self._programTestTwo)

    def test0000TheHeadOfProgramOneIs4(self):
        self.assertEqual(4, self._burstTestOne.getHeadBurst())

    def test0001TheHeadOfProgramTwoIs5(self):
        self.assertEqual(5, self._burstTestTwo.getHeadBurst())

    def test0002TheBurstsOfProgramOneIsOneListOfIntegersWithNumbers(self):
        self.assertEqual([], self._burstTestOne.getBursts())

    def test0003TheBurstsOfProgramTwoIsOneListOfIntegersWithNumbers(self):
        self.assertEqual([3,1,1,2], self._burstTestTwo.getBursts())

    def test0004(self):
        self.assertEqual(4,self._burstTestOne.get(0))
        self.assertEqual(3,self._burstTestOne.get(1))
        self.assertEqual(2,self._burstTestOne.get(2))
        self.assertEqual(1,self._burstTestOne.get(3))
        self.assertEqual(0,self._burstTestOne.get(4))

    def test0005(self):
        self.assertEqual(5, self._burstTestTwo.get(0))
        self.assertEqual(4, self._burstTestTwo.get(1))
        self.assertEqual(3, self._burstTestTwo.get(2))
        self.assertEqual(2, self._burstTestTwo.get(3))
        self.assertEqual(1,self._burstTestTwo.get(4))
        self.assertEqual(3,self._burstTestTwo.get(5))
        self.assertEqual(2,self._burstTestTwo.get(6))
        self.assertEqual(1,self._burstTestTwo.get(7))
        self.assertEqual(1,self._burstTestTwo.get(8))
        self.assertEqual(1,self._burstTestTwo.get(9))
        self.assertEqual(2,self._burstTestTwo.get(11))
        self.assertEqual(1,self._burstTestTwo.get(12))
        self.assertEqual(0,self._burstTestTwo.get(13))

if __name__ == "__main__":
    unittest.main()  