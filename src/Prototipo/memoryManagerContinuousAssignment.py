from tabulate import tabulate

from Prototipo.block import Block
from Prototipo.intManager import Irq


class MemoryManagerContinuousAssignment:
    def __init__(self, memory, pcbTable, intManager, moreSpace):
        self._memory     = memory
        self._free       = self._memory.size()
        self._bl         = [Block(0, self._free - 1, -1)]
        self._bu         = []
        self._pcbTable   = pcbTable
        self._intManager = intManager
        self._moreSpace  = moreSpace

    def isMemoryManagerPaging(self):
        return False

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
    def setPCBAndLoader(self, pcb, bd, limit):
        pcb.set_bd(bd)
        pcb.set_limit(limit)

    """ Proposito: Verifica si hay al menos un bloque con el tamanio nesesario, en caso de no haberlo compacta la memoria,
        designa al programa a un bloque.
        Precondicion: -                    """
    def getFreeBlock(self, pid, sizeProgram):
        if not self.thereIsBlockForProgram(sizeProgram):
            self._intManager.handle(Irq.COMPACT_MEMORY, None)
        return self.addProgram(pid, sizeProgram)

    """ Proposito: Busca un bloque libre (FirstFit, BestFit, WorstFit),
        en caso que el bloque le quede <self._moreSpace>
        mas de lo que requiera el procedimiento se le
        otorga dicho espacio,caso contrario ocupa el bloque
        nesesario, en los dos asigna el bd y el limit correspondiente al bloque
        con su respectivo pid.
        Precondicion:  -                   """
    def addProgram(self, pid, sizeProgram):
        block = self.getBlock(sizeProgram)
        bd = block.get_Bd()
        moreSpace = block.get_Size() - sizeProgram
        if moreSpace > self._moreSpace:
            moreSpace = 0
        limit = bd + sizeProgram - 1
        return self.set_Block(block,pid, bd, limit, moreSpace, sizeProgram)

    """Proposito: asigna valores al pcb, creo un nuevo bloque usado asignando su bd, limit y pid,; lo agrega a
       la lista bloques usuados, y por ultimo acomoda ese bloque, y modifica el espacio libre.
       Precondicion: -                  """
    def set_Block(self, bloque, pid, bd, limit, moreSpace, sizeProgram):
        newBlock = Block(bd, limit + moreSpace, pid)
        newBlock.set_moreSpace(moreSpace)
        self._bu.append(newBlock)
        self.accommodateBl(bloque, limit + moreSpace, sizeProgram, moreSpace)
        self._free -= newBlock.get_Limit() - newBlock.get_Bd() + 1 #+ moreSpace
        return newBlock
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
    def freeMemory(self, pid):
        block = self.searchBlockBu(pid)
        block.set_moreSpace(0)
        self._free += block.get_Size()
        self.joinBlocks(block)
        self._bu.remove(block)

    """Proposito: Dado un pid, busca el bloque ocupado que pertenece a ese pid y lo retorna
       Precondiccion: Debe existir al menos un bloque con ese pid """
    def searchBlockBu(self, pid):
        for block in self._bu:
            if block.get_Pid() == pid:
                return block

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
    def thereIsBlockForProgram(self, sizeProgram):
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
            self._memory.setPos(i, ir)
            oldPos += 1
        self.setPCBAndLoader(pcb, indexPos, indexPos + size - 1)
        self.setBlock(block, indexPos, indexPos + size - 1)

    def setBlock(self, block, bd, limit):
        block.set_bd(bd)
        block.set_limit(limit)
        block.set_moreSpace(0)

    def __repr__(self):
        return "{p1}\n{p2}".format(p1=tabulate(enumerate(self._bu), headers=[' ','Used blocks                         '], tablefmt='psql'),p2=tabulate(enumerate(self._bl), headers=[' ', 'Free blocks   (free={free:3d})            '.format(free=self._free)], tablefmt='psql'))



class MemoryManagerContinuousAssignmentFirstFit(MemoryManagerContinuousAssignment):
    # Proposito:
    # Precondicion: Hay al menos un bloque en self._bl
    def getBlock(self, sizeProgram):
        for block in self._bl:
            if block.get_Size() >= sizeProgram:
                return block


class MemoryManagerContinuousAssignmentBestFit(MemoryManagerContinuousAssignment):
    # Proposito:
    # Precondicion: Hay al menos un bloque en self._bl
    def getBlock(self, sizeProgram):
        blockBest = self._bl[0]
        for bloque in self._bl:
            if bloque.get_Size() >= sizeProgram and blockBest.get_Size() > bloque.get_Size():
                blockBest = bloque
        return blockBest


class MemoryManagerContinuousAssignmentWorstFit(MemoryManagerContinuousAssignment):
    # Proposito:
    # Precondicion: Hay al menos un bloque en self._bl
    def getBlock(self, sizeProgram):
        blockWort = self._bl[0]
        for block in self._bl:
            if block.get_Size() >= sizeProgram and blockWort.get_Size() < block.get_Size():
                blockWort = block
        return blockWort