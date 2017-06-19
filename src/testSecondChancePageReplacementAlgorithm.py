#!/usr/bin/env python
# -*- coding: utf-8 -*-s

import unittest

from Prototipo.frame import Frame
from Prototipo.memoryManagerPaging import SecondChancePageReplacementAlgorithm

class tester(unittest.TestCase):
    def setUp(self):
        self._frame0 = Frame(0)
        self._frame1 = Frame(1)
        self._frame2 = Frame(2)
        self._frame3 = Frame(3)
        self._frame4 = Frame(4)
        self._frame5 = Frame(5)
        self._algorithmSecondChance = SecondChancePageReplacementAlgorithm()

    def test0001SecondChancePageReplacementAlgorithmWithCounterWithThreeFrames(self):
        # mismo ejemplo del pdf
        self._algorithmSecondChance.add(self._frame5)
        self._algorithmSecondChance.add(self._frame0)
        self._algorithmSecondChance.add(self._frame1)
        # Se lleno la memoria
        # usedFrames: 5 0 1

        self.assertEqual(1, self._frame5.getReferenceBit())
        self.assertEqual(1, self._frame0.getReferenceBit())
        self.assertEqual(1, self._frame1.getReferenceBit())

        # PageFault: Se agrega el 2 y sale el 5
        self.assertEqual(5, self._algorithmSecondChance.getVictim().getBD())
        self._algorithmSecondChance.add(self._frame2)
        # usedFrames: 0 1 2

        self.assertEqual(0, self._frame0.getReferenceBit())
        self.assertEqual(0, self._frame1.getReferenceBit())
        self.assertEqual(1, self._frame2.getReferenceBit())

        # Se accede al 0
        self._algorithmSecondChance.updateReferenceBit(self._frame0.getBD())
        # usedFrames: 0 1 2

        self.assertEqual(1, self._frame0.getReferenceBit())
        self.assertEqual(0, self._frame1.getReferenceBit())
        self.assertEqual(1, self._frame2.getReferenceBit())

        # PageFault: Se agrega el 3 y sale el 1
        self.assertEqual(1, self._algorithmSecondChance.getVictim().getBD())
        self._algorithmSecondChance.add(self._frame3)
        # usedFrames: 2 0 3

        self.assertEqual(1, self._frame2.getReferenceBit())
        self.assertEqual(0, self._frame0.getReferenceBit())
        self.assertEqual(1, self._frame3.getReferenceBit())

        # PageFault: Se agrega el 4 y sale el 0
        self.assertEqual(0, self._algorithmSecondChance.getVictim().getBD())
        self._algorithmSecondChance.add(self._frame4)
        # usedFrames: 3 2 4

        self.assertEqual(1, self._frame3.getReferenceBit())
        self.assertEqual(0, self._frame2.getReferenceBit())
        self.assertEqual(1, self._frame4.getReferenceBit())

        # Se accede al 2
        self._algorithmSecondChance.updateReferenceBit(self._frame2.getBD())
        # usedFrames: 3 2 4

        self.assertEqual(1, self._frame3.getReferenceBit())
        self.assertEqual(1, self._frame2.getReferenceBit())
        self.assertEqual(1, self._frame4.getReferenceBit())

        # Se accede al 3
        self._algorithmSecondChance.updateReferenceBit(self._frame3.getBD())
        # usedFrames: 3 2 4

        self.assertEqual(1, self._frame3.getReferenceBit())
        self.assertEqual(1, self._frame2.getReferenceBit())
        self.assertEqual(1, self._frame4.getReferenceBit())

        # PageFault: Se agrega el 0 y sale el 3
        self.assertEqual(3, self._algorithmSecondChance.getVictim().getBD())
        self._algorithmSecondChance.add(self._frame0)
        # usedFrames: 2 4 0

        self.assertEqual(0, self._frame2.getReferenceBit())
        self.assertEqual(0, self._frame4.getReferenceBit())
        self.assertEqual(1, self._frame0.getReferenceBit())

        # PageFault: Se agrega el 3 y sale el 2
        self.assertEqual(2, self._algorithmSecondChance.getVictim().getBD())
        self._algorithmSecondChance.add(self._frame3)
        # usedFrames: 4 0 3

        self.assertEqual(0, self._frame4.getReferenceBit())
        self.assertEqual(1, self._frame0.getReferenceBit())
        self.assertEqual(1, self._frame3.getReferenceBit())

        # PageFault: Se agrega el 2 y sale el 4
        self.assertEqual(4, self._algorithmSecondChance.getVictim().getBD())
        self._algorithmSecondChance.add(self._frame2)
        # usedFrames: 0 3 2

        self.assertEqual(1, self._frame0.getReferenceBit())
        self.assertEqual(1, self._frame3.getReferenceBit())
        self.assertEqual(1, self._frame2.getReferenceBit())

        # PageFault: Se agrega el 1 y sale el 3
        self.assertEqual(0, self._algorithmSecondChance.getVictim().getBD())
        self._algorithmSecondChance.add(self._frame1)
        # usedFrames: 3 2 1

        self.assertEqual(0, self._frame3.getReferenceBit())
        self.assertEqual(0, self._frame2.getReferenceBit())
        self.assertEqual(1, self._frame1.getReferenceBit())


if __name__ == "__main__":
    unittest.main()