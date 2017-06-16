import unittest

from mock import mock

from Prototipo.instructions import *
from Prototipo.memory import *
from Prototipo.memoryManagerContinuousAssignment import MemoryManagerContinuousAssignmentFirstFit
from Prototipo.pcb import PCB
from Prototipo.program import Program


class MyTestCase(unittest.TestCase):
    def setUp(self):
        #Se crea el pcb del primer programa
        self._program1 = Program("so.exe", [CPU(9)], 2)
        self._PCBProgram1=PCB(0)

        # Se crea el pcb del segundo programa
        self._program2 = Program("exel.exe", [CPU(12)], 1)
        self._PCBProgram2 = PCB(1)

        # Se crea el pcb del tercer programa
        self._program3 = Program("paint.exe", [CPU(8)], 3)
        self._PCBProgram3 = PCB(2)

        # Se crea el pcb del cuarto programa
        self._program4 = Program("word.exe", [CPU(7)], 2)
        self._PCBProgram4 = PCB(3)

        # Se crea el pcb del cuarto programa
        self._program5 = Program("pycharm.exe", [CPU(1)], 2)
        self._PCBProgram5 = PCB(4)

        # Se inicializa la memoria
        self._memory = Memory(64)

        # Se inicializa el disco y el Loader
        self._memoryManager = MemoryManagerContinuousAssignmentFirstFit(self._memory, mock.Mock(), mock.Mock(), 1)  # El numero indica el moreSpace

    def testMemory(self):

        # Se cargan cuatro programas a memoria
        self._memoryManager.addProgram(self._PCBProgram1.get_pid(), self._program1.longitud())
        self._memoryManager.addProgram(self._PCBProgram2.get_pid(), self._program2.longitud())
        self._memoryManager.addProgram(self._PCBProgram3.get_pid(), self._program3.longitud())
        self._memoryManager.addProgram(self._PCBProgram4.get_pid(), self._program4.longitud())

        # Se verifica que el memoryManager tenga la cantidad correcta de bloques en cada lista
        self.assertEquals(4, len(self._memoryManager.getBu()))
        self.assertEquals(1, len(self._memoryManager.getBl()))

        # Se elimina un programa
        self._memoryManager.freeMemory(self._PCBProgram1.get_pid())

        # Se verifica que el memoryManager tenga la cantidad correcta de bloques en cada lista
        self.assertEquals(3, len(self._memoryManager.getBu()))
        self.assertEquals(2, len(self._memoryManager.getBl()))

        # Se elimina un programa
        self._memoryManager.freeMemory(self._PCBProgram3.get_pid())

        # Se verifica que el memoryManager tenga la cantidad correcta de bloques en cada lista
        self.assertEquals(2, len(self._memoryManager.getBu()))
        self.assertEquals(3, len(self._memoryManager.getBl()))

        # Se elimina un programa
        self._memoryManager.freeMemory(self._PCBProgram2.get_pid())

        # Se verifica que el memoryManager tenga la cantidad correcta de bloques en cada lista
        self.assertEquals(1, len(self._memoryManager.getBu()))
        self.assertEquals(2, len(self._memoryManager.getBl()))

        # Se carga un quinto programa a memoria
        self._memoryManager.addProgram(self._PCBProgram5.get_pid(), self._program5.longitud())

        # Se verifica que el memoryManager tenga la cantidad correcta de bloques en cada lista
        self.assertEquals(2, len(self._memoryManager.getBu()))
        self.assertEquals(2, len(self._memoryManager.getBl()))

        # Se elimina un programa
        self._memoryManager.freeMemory(self._PCBProgram4.get_pid())

        # Se verifica que el memoryManager tenga la cantidad correcta de bloques en cada lista
        self.assertEquals(1, len(self._memoryManager.getBu()))
        self.assertEquals(2, len(self._memoryManager.getBl()))

        # Se elimina un programa
        self._memoryManager.freeMemory(self._PCBProgram5.get_pid())

        # Se verifica que el memoryManager tenga la cantidad correcta de bloques en cada lista
        self.assertEquals(0, len(self._memoryManager.getBu()))
        self.assertEquals(1, len(self._memoryManager.getBl()))
