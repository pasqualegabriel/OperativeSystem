import unittest

from Prototipo.Schedulers.SchedulerPriority import SchedulerPriorityPreemptive
from Prototipo.instructions import *
from Prototipo.pcb import PCB
from Prototipo.pcbTable import PCBTable
from Prototipo.program import Program


class MyTestCase(unittest.TestCase):
    def setUp(self):
        #Se crea el pcb del primer programa
        self._program1 = Program("so.exe", [CPU(2), CPU(1)], 2)
        self._PCBProgram1=PCB(0)
        self._PCBProgram1.set_priority(self._program1.get_priority())

        # Se crea el pcb del segundo programa
        self._program2 = Program("exel.exe", [CPU(1), IO(1)], 1)
        self._PCBProgram2 = PCB(1)
        self._PCBProgram2.set_priority(self._program2.get_priority())

        # Se crea el pcb del tercer programa
        self._program3 = Program("paint.exe", [CPU(4), IO(1)], 3)
        self._PCBProgram3 = PCB(2)
        self._PCBProgram3.set_priority(self._program3.get_priority())

        # Se crea el pcb del tercer programa
        self._program4 = Program("word.exe", [CPU(4), IO(1)], 2)
        self._PCBProgram4 = PCB(3)
        self._PCBProgram4.set_priority(self._program4.get_priority())

        # Se inicializa al SchedulerPriorityPreventive con un aging de 3
        self._pcbTable=PCBTable()
        self._pcbTable.addPCB(self._PCBProgram1)
        self._pcbTable.addPCB(self._PCBProgram2)
        self._pcbTable.addPCB(self._PCBProgram3)
        self._pcbTable.addPCB(self._PCBProgram4)
        self._aging=3
        self._shedulerTest=SchedulerPriorityPreemptive(self._pcbTable, self._aging)

        # Se agregan los pid, prioridad y los primeros burst de los tres programas
        self._shedulerTest.add(self._PCBProgram1)
        self._shedulerTest.add(self._PCBProgram2)
        self._shedulerTest.add(self._PCBProgram3)
        self._shedulerTest.add(self._PCBProgram4)

    def testSchedulerPriorityPreventive(self):
        # Se comprueba que se desencola primero el pid del programa 2, porque es el de menor prioridad
        self.assertEqual(self._shedulerTest.pop(), self._PCBProgram2.get_pid())

        # Se comprueba que se desencola el pid del programa 1, porque es siguiente de menor prioridad
        self.assertEqual(self._shedulerTest.pop(), self._PCBProgram1.get_pid())
        # y la prioridad del programa 1 sigue siendo de 2
        self.assertEqual(self._PCBProgram1.get_priority(), 2)

        # Se comprueba que se desencola el pid del programa 4, porque es siguiente de menor prioridad
        self.assertEqual(self._shedulerTest.pop(), self._PCBProgram4.get_pid())
        # el aging llego a 3
        # y la prioridad del programa 1 ahora es de 2 por el aging del scheduler
        self.assertEqual(self._PCBProgram4.get_priority(), 1)

        # Se comprueba que se desencola el pid del programa 3, porque es siguiente de menor prioridad
        self.assertEqual(self._shedulerTest.pop(), self._PCBProgram3.get_pid())
        # y la prioridad del programa 1 ahora es de 2 por el aging del scheduler
        self.assertEqual(self._PCBProgram3.get_priority(), 2)


if __name__ == '__main__':
    unittest.main()
