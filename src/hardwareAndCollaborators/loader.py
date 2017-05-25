# !/usr/bin/env python
# -*- coding: utf-8 -*-s
from tabulate import tabulate


class Loader:
    def __init__(self, memoria, mmu, disco, memoryManager):
        self._memory = memoria
        self._mmu = mmu
        self._disco = disco
        self._memoryManager = memoryManager

    # Proposito: carga una lista de instrucciones en la memoria, guarda el bd, el limit
    # y suma un procedimiento a la memoria.
    # Precondiccion:-
    def cargarInMemory(self, pcb, program):
        self._memoryManager.designarEspacio(pcb, program.longitud())
        pos = pcb.get_bd()
        for i in program.getLista():
            self._memory.set_pos(pos, i)
            pos += 1

    def fetch(self, pc):
        return self._mmu.fetch(pc)

    def search_program(self, name):
        for p in self._disco.files():
            try:
                if (p.isProgram() and p.name() == name):
                    return p
            except:
                pass

    # Proposito:librea los espacios de la memory
    # Precondiccion: Existen las posiciones en la memoria
    def liberarMemoria(self, bd, limit, pid):
        self._memoryManager.freeBlock(pid)
        for i in range(bd, limit + 1):
            self._memory.set_pos(i, "")

    """ Proposito: Denota True si hay espacio suficiente en memoria para el tamanio del programa
        Precondicion: -                    """
    def thereIsSpaceInMemoryFor(self, sizeProgram):
        return self._memoryManager.thereIsSpaceInMemoryFor(sizeProgram)

    # para imprimir los bloques
    def getMM(self):
        return self._memoryManager

    def __repr__(self):
        return tabulate(enumerate(self._memoryManager.getBl()), headers=[' ', 'Bloques libres'], tablefmt='psql')


class MemoryManager:
    def __init__(self, memory, PCBTable, intmanager, moreSpace):
        self._memory = memory
        self._free = self._memory.size()
        self._bl = [Block(0, self._free - 1, -1)]
        self._bu = []
        self._pcbTable = PCBTable
        self._intManager = intmanager
        self._moreSpace = moreSpace

    """Proposito: Retorna el espacio libre de la memoria
       Precondicion:  -  """
    def get_Free(self):
        return self._free

    """ Proposito: Retorna la lista de bloques libres
        Precondicion: -                   """
    def getBl(self):
        return self._bl

    """ Proposito: Retorna la lista de bloques ocupados
        Precondicion:  -               """
    def getBu(self):
        return self._bu

    """ Proposito: Asigna el bd y el limit al pcb
        Precondicion: -                 """
    def setearPCBAndLoader(self, pcb, bd, limit):
        pcb.set_bd(bd)
        pcb.set_limit(limit)

    """ Proposito: Verifica si hay al menos un bloque con el tamanio nesesario, en caso de no haberlo compacta la memoria,
        designa al programa a un bloque.
        Precondicion: -                    """
    def designarEspacio(self, pcb, sizeProgram):
        if not self.hayBloqueParaElPrograma(sizeProgram):
            self._intManager.handle("COMPACT_MEMORY", None)
        self.addProgram(pcb, sizeProgram)

    """ Proposito: Busca un bloque libre (FirstFit, BestFit, WorstFit),
        en caso que el bloque le quede <self._moreSpace>
        mas de lo que requiera el procedimiento se le
        otorga dicho espacio,caso contrario ocupa el bloque
        nesesario, en los dos asigna el bd y el limit correspondiente al bloque
        con su respectivo pid.
        Precondicion:  -                   """
    def addProgram(self, pcb, sizeProgram):
        bloque = self.getBlock(sizeProgram)
        bd = bloque.get_Bd()
        moreSpace = bloque.get_Size() - sizeProgram
        if moreSpace > self._moreSpace:
            moreSpace = 0
        limit = bd + sizeProgram - 1
        self.set_Block(bloque, pcb, bd, limit, moreSpace, sizeProgram)

    """Proposito: asigna valores al pcb, creo un nuevo bloque usado asignando su bd, limit y pid,; lo agrega a
       la lista bloques usuados, y por ultimo acomoda ese bloque, y modifica el espacio libre.
       Precondicion: -                  """
    def set_Block(self, bloque, pcb, bd, limit, moreSpace, sizeProgram):
        self.setearPCBAndLoader(pcb, bd, limit)
        newBlock = Block(bd, limit + moreSpace, pcb.get_pid())
        newBlock.set_moreSpace(moreSpace)
        self._bu.append(newBlock)
        self.accommodateBl(bloque, limit + moreSpace, sizeProgram, moreSpace)
        self._free -= newBlock.get_Limit() - newBlock.get_Bd() + 1

    """Proposito: en caso del que el bloque libre tenga distinto tamanio al del tamanio del programa
       y no le haya agregado mas espacios que el tamanio del programa,
       modifica el bloque libre, caso contrario que el tamanio del bloque libre sea igual al tamanio
       del programa elimina el bloque libre.
       Precondicion: -                  """
    def accommodateBl(self, bloque, limit, sizeProgram, moreSpace):
        if bloque.get_Size() != sizeProgram and moreSpace == 0:
            bloque.set_bd(limit + 1)
            bloque.set_pid(-1)
        else:
            self._bl.remove(bloque)

    """Proposito: Elimina el bloque usado, y este lo pone en la cola libre, en caso que se pueda unir con otros bloques libres lo hace.
       Precondiccion: - """
    def freeBlock(self, pid):
        block = self.searchBlockBu(pid)
        block.set_moreSpace(0)
        self._free += block.get_Size()
        self.joinBlocks(block)
        self._bu.remove(block)

    """Proposito: Dado un pid, busca el bloque ocupado que pertenece a ese pid y lo retorna
       Precondiccion: Debe existir al menos un bloque con ese pid """
    def searchBlockBu(self, pid):
        for bloque in self._bu:
            if bloque.get_Pid() == pid:
                return bloque

    """Proposito: verifica si el bloque puede unirlo con otros, en caso q no pueda lo encola en la lista.
       Precondiccion: - """
    def joinBlocks(self, block):
        newBlock = self.joinBlocksDawn(self.joinBlocksUp(block))
        if block.get_Pid() == newBlock.get_Pid():
            newBlock.set_pid(-1)
            self._bl.append(newBlock)

    """Proposito: Une el bloque libre con uno que esta arriba y lo retorna, y en caso contrario devuelve el mismo bloque
       Precondiccion: - """
    def joinBlocksUp(self, block):
        for oneBlock in self._bl:
            if block.get_Bd() - 1 == oneBlock.get_Limit():
                block.set_bd(oneBlock.get_Bd())
                block.set_pid(-1)
                self._bl.remove(oneBlock)
                return block
        return block

    """Proposito: Une el bloque libre con uno que esta abajo y lo retorna, y en caso contrario devuelve el mismo bloque
       Precondiccion: - """
    def joinBlocksDawn(self, block):
        for oneBlock in self._bl:
            if oneBlock.get_Bd() == block.get_Limit() + 1:
                block.set_limit(oneBlock.get_Limit())
                block.set_pid(-1)
                self._bl.remove(oneBlock)
                return block
        return block

    """Proposito: Retorna True si hay espacio en la memoria para el sizeProgram, y False en caso contrario
       Precondiccion: - """
    def thereIsSpaceInMemoryFor(self, sizeProgram):
        return self._free >= sizeProgram

    """Proposito: Retorna True si hay un bloque para ese sizeProgram, y False en caso contrario
       Precondiccion: - """
    def hayBloqueParaElPrograma(self, sizeProgram):
        for oneBlock in self._bl:
            if oneBlock.get_Size() >= sizeProgram:
                return True
        return False

    """Proposito: Compacta la memoria
       Precondiccion: - """
    def toCompact(self):
        self.orderingBu()
        indexPos = 0
        for oneBlockU in self._bu:
            if oneBlockU.get_Bd() != indexPos or oneBlockU.get_moreSpace() != 0:
                self.updateBlockAndPCB(indexPos, oneBlockU)
            indexPos = oneBlockU.get_Limit() + 1
        self.updateBl(indexPos)

    """Proposito: Actualiza blockBl luego de una compactacion
       Precondiccion: - """
    def updateBl(self, indexPos):
        if (indexPos - 1) != self._free:
            blockBl = Block(indexPos, self._memory.size() - 1, -1)
            self._bl = [blockBl]
            self._free = blockBl.get_Size()
        else:
            self._bl = []
            self._free = 0

    """Proposito: Ordena los bloques usados (el bd mas chico al inicio)
       Precondiccion: - """
    def orderingBu(self):
        for i in range(1, len(self._bu)):
            for j in range(0, len(self._bu) - i):
                if self._bu[j].get_Bd() > self._bu[j + 1].get_Bd():
                    k = self._bu[j + 1]
                    self._bu[j + 1] = self._bu[j]
                    self._bu[j] = k

    def updateBlockAndPCB(self, indexPos, block):
        pcb = self._pcbTable.lookUpPCB(block.get_Pid())
        size = block.get_Size()
        oldPos = pcb.get_bd()
        for i in range(indexPos, indexPos + size):
            ir = self._memory.get(oldPos)
            self._memory.set_pos(i, ir)
            oldPos += 1
        self.setearPCBAndLoader(pcb, indexPos, indexPos + size - 1)
        self.setearBlock(block, indexPos, indexPos + size - 1)

    def setearBlock(self, block, bd, limit):
        block.set_bd(bd)
        block.set_limit(limit)
        block.set_moreSpace(0)

    def __repr__(self):
        return tabulate(enumerate(self._bu), headers=[' ', 'Bloques usados'], tablefmt='psql')


class MemoryManagerFirstFit(MemoryManager):
    # Proposito:
    # Precondicion: Hay al menos un bloque en self._bl
    def getBlock(self, sizeProgram):
        for bloque in self._bl:
            if bloque.get_Size() >= sizeProgram:
                return bloque


class MemoryManagerBestFit(MemoryManager):
    # Proposito:
    # Precondicion: Hay al menos un bloque en self._bl
    def getBlock(self, sizeProgram):
        blockBest = self._bl[0]
        for bloque in self._bl:
            if bloque.get_Size() >= sizeProgram and blockBest.get_Size() > bloque.get_Size():
                blockBest = bloque
        return blockBest


class MemoryManagerWorstFit(MemoryManager):
    # Proposito:
    # Precondicion: Hay al menos un bloque en self._bl
    def getBlock(self, sizeProgram):
        blockWort = self._bl[0]
        for bloque in self._bl:
            if bloque.get_Size() >= sizeProgram and blockWort.get_Size() < bloque.get_Size():
                blockWort = bloque
        return blockWort


class Block:
    def __init__(self, bd, limit, pid):
        self._bd = bd
        self._limit = limit
        self._moreSpace = 0
        self._pid = pid

    def get_Bd(self):
        return self._bd

    def get_Limit(self):
        return self._limit

    def get_Pid(self):
        return self._pid

    def get_Size(self):
        if self._moreSpace != 0:
            return self._limit - self._bd + 1 - self._moreSpace
        return self._limit - self._bd + 1

    def set_bd(self, bd):
        self._bd = bd

    def set_limit(self, limit):
        self._limit = limit

    def set_pid(self, pid):
        self._pid = pid

    def set_moreSpace(self, moreSpace):
        self._moreSpace = moreSpace

    def get_moreSpace(self):
        return self._moreSpace

    def __repr__(self):
        return "Bd={bd}, Limit={limit}, Size={size}, Pid={pid}, Ms={ms}".format(bd=self._bd, limit=self._limit,
                                                                       size=self.get_Size(),
                                                                       pid=self._pid, ms=self._moreSpace)
