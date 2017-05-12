#!/usr/bin/env python
# -*- coding: utf-8 -*-s
import unittest
from SistemaDeScheduler.scheduler import *

s = SchedulerPriorityPreventive()
for i in range(4):
    s.add(i)

class tester(unittest.TestCase):

    def test_1(self):
        self.assertEqual(4, s.lenReady())


    def test_2(self):
        self.assertEqual(0, s.pop())
        self.assertEqual(3, s.lenReady())

    
if __name__ == "__main__":
    unittest.main()