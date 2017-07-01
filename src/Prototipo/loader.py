# !/usr/bin/env python
# -*- coding: utf-8 -*-s

class Loader:
    #Proposito: Retorna un programa en el disco con el name<name> en caso q no lo encuetre no hace nada.
    #Precondicion:-
    def searchProgram(self, name):
        for p in self._disco.files():
            try:
                if (p.isProgram() and p.name() == name):
                    return p
            except:
                pass


    #Proposito:Retorna el memoryManager
    #Precondicion:-
    def getMemoryManager(self):
        return self._memoryManager

    #Proposito:Retorna el swap          ##MIRARA ESTE MSJ SI SIVER
    #Precondicion:-
    def getSwapManager(self):
        return self._swap

    #Proposito:inicializa atributos del pcb.
    #Precondicion:-
    def setPCB(self,pcb, program,requiredPages):
        pcb.initialize(program, requiredPages)



class LoaderBlocks(Loader):
    def __init__(self, memory, mmu, disco, memoryManager):
        self._memory = memory
        self._mmu = mmu
        self._disco = disco
        self._memoryManager = memoryManager

    # Proposito:Carga el programa a la memoria.
    # Precondicion:-
    def load(self, pcb, nameProgram):
        program = self.searchProgram(nameProgram)
        self.setPCB(pcb, program, None)
        if not self._memoryManager.thereIsSpaceInMemoryFor(program.longitud()):
            raise SystemError("Memoria insuficiente")
        block = self._memoryManager.getFreeBlock(pcb.get_pid(), program.longitud())
        pcb.set_bd_limit(block.getBd(), block.getLimit())
        pos = pcb.get_bd()
        for i in program.getInstructions():
            self._memory.setPos(pos, i)
            pos += 1

    # Proposito: libera memoria del memoryManager.
    # Precondiccion:-
    def freeMemory(self, pcb):
        self._memoryManager.freeMemory(pcb.get_pid())


class LoaderPages(Loader):
    def __init__(self, memory, mmu, disco, memoryManager, swap):
        self._memory = memory
        self._mmu = mmu
        self._disco = disco
        self._memoryManager = memoryManager
        self._swap=swap

    ##MIRAR QUE PROPOSITO Y CONDICION DEBE TENER.
    #Proposito:
    #Precondicion:
    def load(self, pcb, nameProgram):
        program = self.searchProgram(nameProgram)
        requiredPages = self.requiredPages(program.longitud())
        self.setPCB(pcb, program,requiredPages)

    
    # Proposito:Retorna la cantidad de paginas que nesesita el programa segun su tamaño<sizeProgram>.
    # Precondicion:-
    def requiredPages(self, sizeProgram):
        number = divmod(sizeProgram, self.getMemoryManager().sizeFrame())
        requiredPages = number[0]
        if number[1] != 0:
            requiredPages += 1
        return requiredPages


    #Proposito:Carga intrucciones<instructions> en la memoria fisica segun la pagina<page> dada.
    #Precondicion:-
    def loadInPhysicalMemory(self, instructions, page):
        positionInstruction = page.getBDPhysicalMemory()
        for instruction in instructions:
            self._memory.setPos(positionInstruction, instruction)
            positionInstruction += 1

    #Proposito:carga intruccciones en la
    #Precondicion:-
    def swapIN(self, indexPhysicalMemory, indexSwap):
        instruction = []
        for index in range(indexPhysicalMemory, indexPhysicalMemory + self.getMemoryManager().sizeFrame()):
            instruction.append(self._memory.get(index))
        self._swap.setPos(indexSwap, instruction)

    #Proposito:Retorna las intrucciones que hay en la posicion<position>
    #Precondicion:Debe haber un valor en dicha posicion<position>.
    def swapOut(self, position):
        return self._swap.get(position)


