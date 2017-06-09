# !/usr/bin/env python
# -*- coding: utf-8 -*-s

class Loader:
    def __init__(self, memory, mmu, disco, memoryManager):
        self._memory = memory
        self._mmu = mmu
        self._disco = disco
        self._memoryManager = memoryManager


    # Busca un programa en el disco
    def search_program(self, name):
        for p in self._disco.files():
            try:
                if (p.isProgram() and p.name() == name):
                    return p
            except:
                pass

    # para imprimir los bloques
    def getMM(self):
        return self._memoryManager

    def setPCB(self,pcb, program):
        pcb.set_burstAndPriority(program)



class LoaderBlocks(Loader):
    # Proposito:
    # Precondicion:-
    def load(self, pcb, nameProgram):
        program = self.search_program(nameProgram)
        self.setPCB(pcb, program)
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
    def load(self, pcb, nameProgram):
        program = self.search_program(nameProgram)
        self.setPCB(pcb, program)
        if not self._memoryManager.thereIsSpaceInMemoryFor(program.longitud()):
            raise SystemError("Insufficient memory")
        cantPages = self.requiredPages(program.longitud())
        pcb.setPages(self._memoryManager.returnRequiredPages(cantPages))
        pages = pcb.getPages()  # lista de paginas a cargar
        countPages = 0  # contador de paginas
        indexMemory = pages[countPages].getBd()  # posicion de la memoria segun el bd de la pagina
        countInstruction = 0  # contador de intrucciones para el cambio de pagina
        for instruction in program.getLista():
            if countInstruction == self.getMM().getFrame():
                countInstruction = 0
                countPages += 1
                indexMemory = pages[countPages].getBd()

            self._memory.set_pos(indexMemory + countInstruction, instruction)
            countInstruction += 1

    # Proposito:Retorna la cantidad de paginas que nesesita el programa
    # Precondicion:-
    def requiredPages(self, sizeProgram):
        number = divmod(sizeProgram, self.getMM().getFrame())
        requiredPages = number[0]
        if number[1] != 0:
            requiredPages += 1
        return requiredPages

    def freeMemory(self, pcb):
        self._memoryManager.freeMemory(pcb.getPages())




