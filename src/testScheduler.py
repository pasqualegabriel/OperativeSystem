#!/usr/bin/env python
# -*- coding: utf-8 -*-s
import unittest
from prototipo.scheduler import Scheduler

# Se crea un Scheduler s
# Con 4 elementos en la Queue de ready y waiting,
# el pid 3 en running y el pid 1 en terminated
s = Scheduler("a","b")
for i in range(4):
    s.encolarEnReady(i)
    s.encolarEnWaiting(i)
s.set_running(3)
s.set_terminated(1)

class tester(unittest.TestCase):
    # La Queue de ready tiene 4 elementos
    def test_1(self):
        self.assertEqual(4,s.lenReady())
     
    # La Queue de waiting tiene 4 elementos   
    def test_2(self):
        self.assertEqual(4,s.lenWaiting())
    
    # running = 3
    def test_3(self):
        self.assertEqual(3,s.get_Running())
    
    # terminated = 1
    def test_4(self):
        self.assertEqual(1,s.getTerminated())

    # el primer elemento a desencolar de ready es 0
    # y la longitud ahora es de 3
    def test_5(self):
        self.assertEqual(0, s.desencolarEnReady())
        self.assertEqual(3,s.lenReady())

    # el primer elemento a desencolar de waiting es 0
    # y la longitud ahora es de 3
    def test_6(self):
        self.assertEqual(0, s.desencolarEnWaiting())
        self.assertEqual(3,s.lenWaiting())
  
if __name__ == "__main__":
    unittest.main()