import unittest

from SistemaDeProcedimientos.pcb import PCB
from SistemaDeProgramas.program import Program
from SistemaDeProgramas.instructions import *
from hardwareAndCollaborators.disco import Disco
from hardwareAndCollaborators.loader import Loader
from hardwareAndCollaborators.memory import *


class MyTestCase(unittest.TestCase):
    def setUp(self):
        #Se crea el pcb del primer programa
        self._program1 = Program("so.exe", [CPU(9)], 2)
        self._PCBProgram1=PCB(0,self._program1)

        # Se crea el pcb del segundo programa
        self._program2 = Program("exel.exe", [CPU(12)], 1)
        self._PCBProgram2 = PCB(1, self._program2)

        # Se crea el pcb del tercer programa
        self._program3 = Program("paint.exe", [CPU(8)], 3)
        self._PCBProgram3 = PCB(2, self._program3)

        # Se crea el pcb del cuarto programa
        self._program4 = Program("word.exe", [CPU(7)], 2)
        self._PCBProgram4 = PCB(3, self._program4)

        # Se crea el pcb del cuarto programa
        self._program5 = Program("pycharm.exe", [CPU(1)], 2)
        self._PCBProgram5 = PCB(4, self._program5)

        # Se inicializa la memoria
        self._memory = Memory()

        # Se inicializa el disco y el Loader
        self._disco = Disco()
        self._loader = Loader(self._memory, self._disco)

    def testMemory(self):

        # Se cargan cuatro programas a memoria
        self._loader.designateSpace(self._PCBProgram1,self._program1.longitud())
        self._loader.cargarInMemory(self._PCBProgram1.get_bd(), self._program1)
        self._loader.designateSpace(self._PCBProgram2,self._program2.longitud())
        self._loader.cargarInMemory(self._PCBProgram2.get_bd(), self._program2)
        self._loader.designateSpace(self._PCBProgram3,self._program3.longitud())
        self._loader.cargarInMemory(self._PCBProgram3.get_bd(), self._program3)
        self._loader.designateSpace(self._PCBProgram4,self._program4.longitud())
        self._loader.cargarInMemory(self._PCBProgram4.get_bd(), self._program4)

        # Se verifica que el memoryManager tenga la cantidad correcta de bloques en cada lista
        self.assertEquals(4, len(self._loader.getMM().getBu()))
        self.assertEquals(1, len(self._loader.getMM().getBl()))

        # Se elimina un programa
        self._loader.liberarMemoria(self._PCBProgram1.get_bd(), self._PCBProgram1.get_limit(), self._PCBProgram1.get_pid())

        # Se verifica que el memoryManager tenga la cantidad correcta de bloques en cada lista
        self.assertEquals(3, len(self._loader.getMM().getBu()))
        self.assertEquals(2, len(self._loader.getMM().getBl()))

        # Se elimina un programa
        self._loader.liberarMemoria(self._PCBProgram3.get_bd(), self._PCBProgram3.get_limit(), self._PCBProgram3.get_pid())

        # Se verifica que el memoryManager tenga la cantidad correcta de bloques en cada lista
        self.assertEquals(2, len(self._loader.getMM().getBu()))
        self.assertEquals(3, len(self._loader.getMM().getBl()))

        # Se elimina un programa
        self._loader.liberarMemoria(self._PCBProgram2.get_bd(), self._PCBProgram2.get_limit(), self._PCBProgram2.get_pid())

        # Se verifica que el memoryManager tenga la cantidad correcta de bloques en cada lista
        self.assertEquals(1, len(self._loader.getMM().getBu()))
        self.assertEquals(2, len(self._loader.getMM().getBl()))

        # Se carga un quinto programa a memoria
        self._loader.designateSpace(self._PCBProgram5,self._program5.longitud())
        self._loader.cargarInMemory(self._PCBProgram5.get_bd(), self._program5)

        # Se verifica que el memoryManager tenga la cantidad correcta de bloques en cada lista
        self.assertEquals(2, len(self._loader.getMM().getBu()))
        self.assertEquals(2, len(self._loader.getMM().getBl()))

        # Se elimina un programa
        self._loader.liberarMemoria(self._PCBProgram4.get_bd(), self._PCBProgram4.get_limit(), self._PCBProgram4.get_pid())

        # Se verifica que el memoryManager tenga la cantidad correcta de bloques en cada lista
        self.assertEquals(1, len(self._loader.getMM().getBu()))
        self.assertEquals(2, len(self._loader.getMM().getBl()))

        # Se elimina un programa
        self._loader.liberarMemoria(self._PCBProgram5.get_bd(), self._PCBProgram5.get_limit(), self._PCBProgram5.get_pid())

        # Se verifica que el memoryManager tenga la cantidad correcta de bloques en cada lista
        self.assertEquals(0, len(self._loader.getMM().getBu()))
        self.assertEquals(1, len(self._loader.getMM().getBl()))
