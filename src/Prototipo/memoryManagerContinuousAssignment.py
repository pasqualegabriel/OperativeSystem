#!/usr/bin/env python
# -*- coding: utf-8 -*-s
from tabulate import tabulate

from Prototipo.block import Block
from Prototipo.intManager import Irq


class MemoryManagerContinuousAssignment:
    def __init__(self, memory, pcbTable, intManager, moreSpace):
        self._memory     = memory
        self._free       = self._memory.size()
        self._freeBlocks = [Block(0, self._free - 1, -1)]  # Block(bd, limit, pid)
        self._usedBlocks = []
        self._pcbTable   = pcbTable
        self._intManager = intManager
        self._moreSpace  = moreSpace

    # Proposito: Retorna el espacio libre de la memoria
    def getFree(self):
        return self._free

    # Proposito: Retorna la lista de bloques libres
    def getFreeBlocks(self):
        return self._freeBlocks

    # Proposito: Retorna la lista de bloques ocupados
    def getUsedBlocks(self):
        return self._usedBlocks

    # Proposito: Verifica si hay al menos un bloque con el tamanio nesesario, en caso de no haberlo compacta la memoria,
    # designa al programa a un bloque.
    # Precondicion: self._free >= sizeProgram
    def getFreeBlock(self, pid, sizeProgram):
        if not self.thereIsBlockForProgram(sizeProgram):
            self._intManager.handle(Irq.COMPACT_MEMORY, None)
        return self.addProgram(pid, sizeProgram)

    # Proposito: Busca un bloque libre (FirstFit, BestFit, WorstFit), en caso que el bloque le quede <self._moreSpace>
    # mas de lo que requiera el procedimiento se le otorga dicho espacio,caso contrario ocupa el bloque
    # nesesario, en los dos asigna el bd y el limit correspondiente al bloque con su respectivo pid.
    def addProgram(self, pid, sizeProgram):
        block = self.getBlock(sizeProgram)
        bd = block.getBd()
        moreSpace = block.getSize() - sizeProgram
        if moreSpace > self._moreSpace:
            moreSpace = 0
        limit = bd + sizeProgram - 1
        return self.set_Block(block, pid, bd, limit, moreSpace, sizeProgram)

    # Proposito: Asigna valores al pcb, creo un nuevo bloque usado asignando su bd, limit y pid,; lo agrega a
    # la lista bloques usuados, y por ultimo acomoda ese bloque, y modifica el espacio libre.
    def set_Block(self, bloque, pid, bd, limit, moreSpace, sizeProgram):
        newBlock = Block(bd, limit + moreSpace, pid)
        newBlock.set_moreSpace(moreSpace)
        self._usedBlocks.append(newBlock)
        self.accommodateInUsedBlocks(bloque, limit + moreSpace, sizeProgram, moreSpace)
        self._free -= newBlock.getLimit() - newBlock.getBd() + 1 #+ moreSpace
        return newBlock

    # Proposito: En caso del que el bloque libre tenga distinto tamanio al del tamanio del programa y no le haya agregado
    # mas espacios que el tamanio del programa, modifica el bloque libre,
    # caso contrario que el tamanio del bloque libre sea igual al tamanio del programa elimina el bloque libre.
    def accommodateInUsedBlocks(self, bloque, limit, sizeProgram, moreSpace):
        if bloque.getSize() != sizeProgram and moreSpace == 0:
            bloque.set_bd(limit + 1)
            bloque.set_pid(-1)
        else:
            self._freeBlocks.remove(bloque)

    # Proposito: Elimina el bloque usado, y este lo pone en la cola libre, en caso que se pueda unir con otros bloques libres lo hace.
    def freeMemory(self, pid):
        block = self.searchBlockInUsedBlock(pid)
        block.set_moreSpace(0)
        self._free += block.getSize()
        self.joinBlocks(block)
        self._usedBlocks.remove(block)

    # Proposito: Dado un pid, busca el bloque ocupado que pertenece a ese pid y lo retorna
    # Precondiccion: Debe existir al menos un bloque con ese pid
    def searchBlockInUsedBlock(self, pid):
        for block in self._usedBlocks:
            if block.getPid() == pid:
                return block

    # Proposito: Verifica si el bloque puede unirlo con otros, en caso q no pueda lo encola en la lista.
    def joinBlocks(self, block):
        newBlock = self.joinBlocksDawn(self.joinBlocksUp(block))
        if block.getPid() == newBlock.getPid():
            newBlock.set_pid(-1)
            self._freeBlocks.append(newBlock)

    # Proposito: Une el bloque libre con uno que esta arriba y lo retorna, y en caso contrario devuelve el mismo bloque
    def joinBlocksUp(self, block):
        for oneBlock in self._freeBlocks:
            if block.getBd() - 1 == oneBlock.getLimit():
                block.set_bd(oneBlock.getBd())
                block.set_pid(-1)
                self._freeBlocks.remove(oneBlock)
                return block
        return block

    # Proposito: Une el bloque libre con uno que esta abajo y lo retorna, y en caso contrario devuelve el mismo bloque
    def joinBlocksDawn(self, block):
        for oneBlock in self._freeBlocks:
            if oneBlock.getBd() == block.getLimit() + 1:
                block.set_limit(oneBlock.getLimit())
                block.set_pid(-1)
                self._freeBlocks.remove(oneBlock)
                return block
        return block

    # Proposito: Retorna True si hay espacio en la memoria para el sizeProgram, y False en caso contrario
    def thereIsSpaceInMemoryFor(self, sizeProgram):
        return self._free >= sizeProgram

    # Proposito: Retorna True si hay un bloque para ese sizeProgram, y False en caso contrario
    def thereIsBlockForProgram(self, sizeProgram):
        for oneBlock in self._freeBlocks:
            if oneBlock.getSize() >= sizeProgram:
                return True
        return False

    # Proposito: Compacta la memoria
    def toCompact(self):
        self.orderingUsedBlocks()
        indexPos = 0
        for oneBlockU in self._usedBlocks:
            if oneBlockU.getBd() != indexPos or oneBlockU.getMoreSpace() != 0:
                self.updateBlockAndPCB(indexPos, oneBlockU)
            indexPos = oneBlockU.getLimit() + 1
        self.updateUsedBlocks(indexPos)

    # Proposito: Actualiza <block> en una compactacion
    def updateBlockAndPCB(self, indexPos, block):
        pcb = self._pcbTable.lookUpPCB(block.getPid())
        size = block.getSize()
        oldPos = pcb.get_bd()
        for i in range(indexPos, indexPos + size):
            ir = self._memory.get(oldPos)
            self._memory.setPos(i, ir)
            oldPos += 1
        self.setPCBAndLoader(pcb, indexPos, indexPos + size - 1)
        self.setBlock(block, indexPos, indexPos + size - 1)

    # Proposito: Asigna el bd y el limit al pcb
    def setPCBAndLoader(self, pcb, bd, limit):
        pcb.set_bd(bd)
        pcb.set_limit(limit)

    # Proposito: Setea el bd, limit, y el moreSpace en 0 al block
    def setBlock(self, block, bd, limit):
        block.set_bd(bd)
        block.set_limit(limit)
        block.set_moreSpace(0)

    # Proposito: Actualiza los bloques libres luego de una compactacion
    def updateUsedBlocks(self, indexPos):
        if (indexPos - 1) != self._free:
            blockBl = Block(indexPos, self._memory.size() - 1, -1)
            self._freeBlocks = [blockBl]
            self._free = blockBl.getSize()
        else:
            self._freeBlocks = []
            self._free = 0

    # Proposito: Ordena los bloques usados (el bd mas chico al inicio)
    def orderingUsedBlocks(self):
        for i in range(1, len(self._usedBlocks)):
            for j in range(0, len(self._usedBlocks) - i):
                if self._usedBlocks[j].getBd() > self._usedBlocks[j + 1].getBd():
                    k = self._usedBlocks[j + 1]
                    self._usedBlocks[j + 1] = self._usedBlocks[j]
                    self._usedBlocks[j] = k

    # Solo se utiliza para la impresion
    def isMemoryManagerPaging(self):
        return False

    def __repr__(self):
        return "{p1}\n{p2}".format(p1=tabulate(enumerate(self._usedBlocks), headers=[' ', 'Used blocks                         '], tablefmt='psql'), p2=tabulate(enumerate(self._freeBlocks), headers=[' ', 'Free blocks   (free={free:3d})            '.format(free=self._free)], tablefmt='psql'))



class MemoryManagerContinuousAssignmentFirstFit(MemoryManagerContinuousAssignment):
    # Proposito: Retorna un bloque
    # Precondicion: Hay al menos un bloque en self._bl
    def getBlock(self, sizeProgram):
        for block in self._freeBlocks:
            if block.getSize() >= sizeProgram:
                return block


class MemoryManagerContinuousAssignmentBestFit(MemoryManagerContinuousAssignment):
    # Proposito: Retorna un bloque
    # Precondicion: Hay al menos un bloque en self._bl
    def getBlock(self, sizeProgram):
        blockBest = self._freeBlocks[0]
        for block in self._freeBlocks:
            if block.getSize() >= sizeProgram and blockBest.getSize() > block.getSize():
                blockBest = block
        return blockBest


class MemoryManagerContinuousAssignmentWorstFit(MemoryManagerContinuousAssignment):
    # Proposito: Retorna un bloque
    # Precondicion: Hay al menos un bloque en self._bl
    def getBlock(self, sizeProgram):
        blockWort = self._freeBlocks[0]
        for block in self._freeBlocks:
            if block.getSize() >= sizeProgram and blockWort.getSize() < block.getSize():
                blockWort = block
        return blockWort