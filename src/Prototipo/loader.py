# !/usr/bin/env python
# -*- coding: utf-8 -*-s

class Loader:
    #Proposito: Busca un programa en el disco
    #Precondicion:-
    def searchProgram(self, name):
        for p in self._disco.files():
            try:
                if (p.isProgram() and p.name() == name):
                    return p
            except:
                pass


    def getMemoryManager(self):
        return self._memoryManager

    def getSwapManager(self):
        return self._swap

    #Proposito:inicializa atributos del pcb.
    #Precondicion:-
    def setPCB(self,pcb, program,requiredPages):
        pcb.initialize(program, requiredPages)



class LoaderBlocks(Loader):
    def __init__(self, memory, mmu, disco, memoryManager, swap):
        self._memory = memory
        self._mmu = mmu
        self._disco = disco
        self._memoryManager = memoryManager

    # Proposito:
    # Precondicion:-
    def load(self, pcb, nameProgram):
        program = self.searchProgram(nameProgram)
        self.setPCB(pcb, program, None)
        if not self._memoryManager.thereIsSpaceInMemoryFor(program.longitud()):
            raise SystemError("Memoria insuficiente")
        block = self._memoryManager.getFreeBlock(pcb.get_pid(), program.longitud())
        pcb.set_bd_limit(block.get_Bd(), block.get_Limit())
        pos = pcb.get_bd()
        for i in program.getLista():
            self._memory.set_pos(pos, i)
            pos += 1

    # Proposito: Dependiendo el memoryManager libera la memoria que ocupa el pcb.
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
    #Proposito:solicita un marco para un pagina, luego la carga en la memoria, tambien actualiza el pcb.
    #Precondicion:
    def load(self, pcb, nameProgram):
        program = self.searchProgram(nameProgram)
        requiredPages = self.requiredPages(program.longitud())
        self.setPCB(pcb, program,requiredPages)

    
    # Proposito:Retorna la cantidad de paginas que nesesita el programa
    # Precondicion:-
    def requiredPages(self, sizeProgram):
        number = divmod(sizeProgram, self.getMemoryManager().sizeFrame())
        requiredPages = number[0]
        if number[1] != 0:
            requiredPages += 1
        return requiredPages


    #Proposito:Carga las intrucciones en la memoria fisica
    #Precondicion:-
    def loadInPhysicalMemory(self, instructions, page):
        positionInstruction = page.getBDPhysicalMemory()
        for instruction in instructions:
            self._memory.set_pos(positionInstruction,instruction)
            positionInstruction+=1

        #for positionMemory in range(page.getBd() ,page.getBd() + self.getMemoryManager().sizeFrame()):
        #    self._memory.set_pos(positionMemory, instructions[positionInstruction])
        #    positionInstruction+=1

    def swapIN(self, bdPhysicalMemory, keySwap):
        instruction = []
        for index in range(bdPhysicalMemory, bdPhysicalMemory + self.getMemoryManager().sizeFrame()):
            instruction.append(self._memory.get(index))
        self._swap.setPos(keySwap, instruction)

    def swapOut(self, keySwap):
        return self._swap.get(keySwap)


