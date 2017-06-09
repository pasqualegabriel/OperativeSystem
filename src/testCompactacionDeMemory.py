import unittest

from Prototipo.disco import Disco
from Prototipo.instructions import *
from Prototipo.intManager import IntManager
from Prototipo.loader import *
from Prototipo.memory import *
from Prototipo.memoryManager import MemoryManagerFirstFit
from Prototipo.mmu import Mmu
from Prototipo.pcb import PCB
from Prototipo.pcbTable import PCBTable
from Prototipo.program import Program


class MyTestCase(unittest.TestCase):
    def setUp(self):

        # Se crea al pcbTable
        self._pcbTable = PCBTable()

        # Se crea el pcb del primer programa
        self._program1 = Program("so.exe", [CPU(10)], 2)
        self._PCBProgram1=PCB(0,self._program1)



        # Se crea el pcb del segundo programa
        self._program2 = Program("exel.exe", [IO(1),CPU(9)], 1)
        self._PCBProgram2 = PCB(1, self._program2)


        # Se crea el pcb del tercer programa
        self._program3 = Program("paint.exe", [CPU(10)], 3)
        self._PCBProgram3 = PCB(2, self._program3)


        # Se crea el pcb del cuarto programa
        self._program4 = Program("word.exe", [CPU(10)], 2)
        self._PCBProgram4 = PCB(3, self._program4)


        # Se crea el pcb del quint programa
        self._program5 = Program("pycharm.exe", [CPU(10)], 2)
        self._PCBProgram5 = PCB(4, self._program5)


        # Se crea el pcb del sexto programa
        self._program6 = Program("pharo.exe", [CPU(40)], 2)
        self._PCBProgram6 = PCB(5, self._program6)


        self._pcbTable.addPCB(self._PCBProgram1)
        self._pcbTable.addPCB(self._PCBProgram2)
        self._pcbTable.addPCB(self._PCBProgram3)
        self._pcbTable.addPCB(self._PCBProgram4)
        self._pcbTable.addPCB(self._PCBProgram5)
        self._pcbTable.addPCB(self._PCBProgram6)

        # Se inicializa la memoria
        self._memory = Memory(100)

        #self._intmanager = IntManager()
        #self._intmanager.register("COMPACT_MEMORY", CompactMemory(self._loader, self._dispatcher, self._memoryManager , self._scheduler,
        #                                  self._pcbTable))

        # Se inicializa el memoryManager, y el Loader
        self._memoryManager = MemoryManagerFirstFit(self._memory, self._pcbTable, IntManager(), 2)
        self._loader = LoaderBlocks(self._memory, Mmu(self._memory), Disco(), self._memoryManager)

        # Se cargan cinco programas a memoria
        self._loader.load(self._PCBProgram1, self._program1)
        self._loader.load(self._PCBProgram2, self._program2)
        self._loader.load(self._PCBProgram3, self._program3)
        self._loader.load(self._PCBProgram4, self._program4)
        self._loader.load(self._PCBProgram5, self._program5)
        self._loader.load(self._PCBProgram6, self._program6)


        # Se elimina un programa
        #self._loader.liberarMemoria(self._PCBProgram1.get_bd(), self._PCBProgram1.get_limit(), self._PCBProgram1.get_pid())
        #self._loader.liberarMemoria(self._PCBProgram4.get_bd(), self._PCBProgram4.get_limit(), self._PCBProgram4.get_pid())
        #self._memoryManager.toCompact()
        # En este caso se hace la compactacion
        #self._loader.cargarInMemory(self._PCBProgram6, self._program6)


    def testCompactacion(self):
        #self.assertTrue(4, len(self._loader.getMM().getBu()))
        #self.assertEquals(1, len(self._loader.getMM().getBl()))
        #self.assertNotEquals(self._PCBProgram5.get_bd(), self._c)
        self.assertFalse(self._memoryManager.thereIsBlockForProgram(10))
        self._loader.freeMemory(self._PCBProgram1)
        self._loader.freeMemory(self._PCBProgram4)
        sizeAntesCompac= self._memoryManager.get_Free()
        self._memoryManager.toCompact()
        sizeDepuesCompac=self._memoryManager.get_Free()
        self.assertTrue(self._memory.get(0).isIO())
        self.assertTrue(self._memoryManager.thereIsBlockForProgram(10))
        self.assertEqual(sizeAntesCompac,sizeDepuesCompac)

if __name__ == "__main__":
    unittest.main()