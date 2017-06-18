#!/usr/bin/env python
# -*- coding: utf-8 -*-s

import unittest

from Prototipo.memoryManagerPaging import FirstInFirstOutPageReplacementAlgorithm


class tester(unittest.TestCase):
    def setUp(self):
        self._algorithmMemoryManagerFifo = FirstInFirstOutPageReplacementAlgorithm()

    def test0001WithThreeFrames(self):
        # mismo ejemplo del pdf
        self._algorithmMemoryManagerFifo.add(1)
        self._algorithmMemoryManagerFifo.add(2)
        self._algorithmMemoryManagerFifo.add(3)
        # Se lleno la memoria
        # usedFrames: 1 2 3

        # PageFault: Se agrega el 4 y sale el 1
        self.assertEqual(1, self._algorithmMemoryManagerFifo.getVictim())
        self._algorithmMemoryManagerFifo.add(4)
        # usedFrames: 2 3 4

        # PageFault: Se agrega el 1 y sale el 2
        self.assertEqual(2, self._algorithmMemoryManagerFifo.getVictim())
        self._algorithmMemoryManagerFifo.add(1)
        # usedFrames: 3 4 1

        # PageFault: Se agrega el 2 y sale el 3
        self.assertEqual(3, self._algorithmMemoryManagerFifo.getVictim())
        self._algorithmMemoryManagerFifo.add(2)
        # usedFrames: 4 1 2

        # PageFault: Se agrega el 5 y sale el 4
        self.assertEqual(4, self._algorithmMemoryManagerFifo.getVictim())
        self._algorithmMemoryManagerFifo.add(5)
        # usedFrames: 1 2 5

        # PageFault: Se agrega el 3 y sale el 1
        self.assertEqual(1, self._algorithmMemoryManagerFifo.getVictim())
        self._algorithmMemoryManagerFifo.add(3)
        # usedFrames: 2 5 3

        # PageFault: Se agrega el 4 y sale el 2
        self.assertEqual(2, self._algorithmMemoryManagerFifo.getVictim())
        self._algorithmMemoryManagerFifo.add(4)
        # usedFrames: 5 3 2


if __name__ == "__main__":
    unittest.main()