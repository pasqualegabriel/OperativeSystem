#!/usr/bin/env python
# -*- coding: utf-8 -*-s

import unittest

from Prototipo.Schedulers.SchedulerSJF import SchedulerSJFPreemptive
from Prototipo.instructions import *
from Prototipo.pcb import PCB
from Prototipo.program import Program


class MyTestCase(unittest.TestCase):

    def setUp(self):
        #Se crea el pcb del primer programa
        self._program1 = Program("so.exe", [CPU(2), CPU(1)], 1)
        self._PCBProgram1=PCB(0)
        self._PCBProgram1.initialize(self._program1, self._program1.longitud() // 4)

        # Se crea el pcb del segundo programa
        self._program2 = Program("exel.exe", [CPU(1), IO(1)], 2)
        self._PCBProgram2 = PCB(1)
        self._PCBProgram2.initialize(self._program2, self._program2.longitud() // 4)

        # Se crea el pcb del tercer programa
        self._program3 = Program("paint.exe", [CPU(4), IO(1)], 3)
        self._PCBProgram3 = PCB(2)
        self._PCBProgram3.initialize(self._program3, self._program3.longitud() // 4)

        # Se crea al schedulerSJF
        self._shedulerSJF = SchedulerSJFPreemptive()
        # Se agregan el pid, la prioridad(en este caso no se utiliza),
        # y el primer burst de los programas 2 y 3
        self._shedulerSJF.add(self._PCBProgram2)
        self._shedulerSJF.add(self._PCBProgram3)

        # Obtiene el primer burst del programa 1
        firstBurstProgram1 = self._PCBProgram1.get_firstBurst()
        # Setea el primer burst del programa que esta en la CPU
        self._shedulerSJF.set_burstPCBInCPU(firstBurstProgram1)

    def testSchedulerSJF(self):

        # Obtiene el primer burst del programa 2
        firstBurstProgram2 = self._PCBProgram2.get_firstBurst()
        # Se comprueba que el burst del programa 2 es menor que el programa que esta en CPU
        self.assertTrue(self._shedulerSJF.isChange(self._PCBProgram3, self._PCBProgram2))

        # El scheduler desencola un programa
        pid = self._shedulerSJF.pop()
        # Se comprueba que desencolo al pid del programa con menor burst
        self.assertEqual(pid,self._PCBProgram2.get_pid())

        # Setea el busrt del programa que ahora esta en CPU
        self._shedulerSJF.set_burstPCBInCPU(firstBurstProgram2)

        # Se comprueba que el burst del programa 3 es menor que el programa que esta en CPU
        self.assertFalse(self._shedulerSJF.isChange(self._PCBProgram2, self._PCBProgram3))


if __name__ == '__main__':
    unittest.main()
