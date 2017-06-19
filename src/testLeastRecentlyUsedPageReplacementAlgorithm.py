#!/usr/bin/env python
# -*- coding: utf-8 -*-s

import unittest

from Prototipo.frame import Frame
from Prototipo.memoryManagerPaging import LeastRecentlyUsedPageReplacementAlgorithm

class tester(unittest.TestCase):
    def setUp(self):
        self._frame0 = Frame(0)
        self._frame1 = Frame(1)
        self._frame2 = Frame(2)
        self._frame3 = Frame(3)
        self._frame4 = Frame(4)
        self._frame5 = Frame(5)
        self._algorithmLRU = LeastRecentlyUsedPageReplacementAlgorithm()

    def test0001WithThreeFrames(self):
        # mismo ejemplo del pdf
        self._algorithmLRU.add(self._frame5)
        self._algorithmLRU.add(self._frame0)
        self._algorithmLRU.add(self._frame1)
        # Se lleno la memoria
        # usedFrames: 5 0 1

        self.assertEqual(0, self._frame5.getTimeBit())
        self.assertEqual(1, self._frame0.getTimeBit())
        self.assertEqual(2, self._frame1.getTimeBit())

        # PageFault: Se agrega el 2 y sale el 5
        self.assertEqual(5, self._algorithmLRU.getVictim().getBD())
        self._algorithmLRU.add(self._frame2)
        # usedFrames: 0 1 2

        self.assertEqual(0, self._frame5.getTimeBit())
        self.assertEqual(1, self._frame0.getTimeBit())
        self.assertEqual(3, self._frame2.getTimeBit())

        # Se accede al 0
        self._algorithmLRU.updateReferenceBit(self._frame0.getBD())
        self.assertEqual(4, self._frame0.getTimeBit())

        # PageFault: Se agrega el 3 y sale el 1
        self.assertEqual(1, self._algorithmLRU.getVictim().getBD())
        self._algorithmLRU.add(self._frame3)
        # usedFrames: 0 2 3

        # Se accede al 0
        self._algorithmLRU.updateReferenceBit(self._frame0.getBD())
        self.assertEqual(6, self._frame0.getTimeBit())

        self.assertEqual(6, self._frame0.getTimeBit())
        self.assertEqual(3, self._frame2.getTimeBit())
        self.assertEqual(5, self._frame3.getTimeBit())

        # PageFault: Se agrega el 4 y sale el 2
        self.assertEqual(2, self._algorithmLRU.getVictim().getBD())
        self._algorithmLRU.add(self._frame4)
        # usedFrames: 0 3 4

        # PageFault: Se agrega el 2 y sale el 3
        self.assertEqual(3, self._algorithmLRU.getVictim().getBD())
        self._algorithmLRU.add(self._frame2)
        # usedFrames: 0 4 2

        # PageFault: Se agrega el 3 y sale el 0
        self.assertEqual(0, self._algorithmLRU.getVictim().getBD())
        self._algorithmLRU.add(self._frame3)
        # usedFrames: 4 2 3

        # PageFault: Se agrega el 0 y sale el 4
        self.assertEqual(4, self._algorithmLRU.getVictim().getBD())
        self._algorithmLRU.add(self._frame0)
        # usedFrames: 2 3 0

        # Se accede al 3
        self.assertEqual(9, self._frame3.getTimeBit())
        self._algorithmLRU.updateReferenceBit(self._frame3.getBD())
        self.assertEqual(11, self._frame3.getTimeBit())

        # Se accede al 2
        self.assertEqual(8, self._frame2.getTimeBit())
        self._algorithmLRU.updateReferenceBit(self._frame2.getBD())
        self.assertEqual(12, self._frame2.getTimeBit())

        # PageFault: Se agrega el 1 y sale el 0
        self.assertEqual(0, self._algorithmLRU.getVictim().getBD())
        self._algorithmLRU.add(self._frame1)
        # usedFrames: 2 3 1


if __name__ == "__main__":
    unittest.main()