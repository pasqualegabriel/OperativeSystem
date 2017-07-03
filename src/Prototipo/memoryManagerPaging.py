# !/usr/bin/env python
# -*- coding: utf-8 -*-s

from tabulate import tabulate

from Prototipo.Schedulers.queues import QueueFIFO
from Prototipo.frame import Frame

class MemoryManagerPaging:
    def __init__(self, memory, sizeFrame, PCBTable, swap, pageReplacementAlgorithm):
        self._memory                       = memory
        self._sizeFrame                    = sizeFrame
        self._pcbTable                     = PCBTable
        self._swap                         = swap
        ##MARCOS DEL LA MEMORIA FISICA
        self._freeFramesPhysicalMemory     = self.calculateFreeFrames(self._memory.size())
        self._usedFramesPhysicalMemory     = pageReplacementAlgorithm
        self._cantFreeFramesPhysicalMemory = len(self._freeFramesPhysicalMemory)
        ##MARCOS DEL SWAP
        self._freeFramesSwap               = self.calculateFreeFrames(self._memory.size() * 2)
        self._usedFramesSwap               = []
        self._cantFreeFramesSwap           = len(self._freeFramesSwap)


    # Proposito: Si hay un marco libre en la memoria fisica lo retorna, en caso que no, busca uno del swap,
    # en caso que no tenga ninguno de los dos levanta una exepcion
    def assignFrame(self, pid, pageNumber):
        if self.thereIsSpaceInMemory():
            return self.assignFramePhysicalMemory(pid, pageNumber)
        elif self.thereIsSpaceInSwap():
            return self.victimSelection(pid, pageNumber)
        else:
            raise SystemError("Insufficient memory")


    # Proposito: Asigna un marco libre en la memoria fisica.
    # Precondicion: Hay al menos un frame libre en la memoria fisica.
    def assignFramePhysicalMemory(self, pid, pageNumber):
        newUsedFrame = self._freeFramesPhysicalMemory.pop(0)
        newUsedFrame.setPid(pid)
        newUsedFrame.setPageNumber(pageNumber)
        self._usedFramesPhysicalMemory.add(newUsedFrame)
        self._cantFreeFramesPhysicalMemory -= 1
        return newUsedFrame.getBD()

    # Proposito: Asigna un marco libre del swap.
    # Precondicion: Hay al menos un frame libre en el swap
    def assignFrameSwap(self, victimFrame):
        # Se busca la pagina de la del frame que seleccione como victima
        pidVictimFrame=victimFrame.getPId()
        pcb = self._pcbTable.lookUpPCB(pidVictimFrame)
        page = pcb.getPageTable().searchPage(victimFrame.getBD())

        # Se verifica si ya habia sido cargada la pagina en el swap para no volver a cargar.
        if self.isPageInSwap(page, pidVictimFrame):
            return

        # En caso que no este pido un frame en el swap
        newUsedFrame = self._freeFramesSwap.pop(0)
        newUsedFrame.setPid(victimFrame.getPId())
        newUsedFrame.setPageNumber(victimFrame.getPageNumber())
        self._usedFramesSwap.append(newUsedFrame)
        page.setBDVirtualMemory(newUsedFrame.getBD())
        self._cantFreeFramesSwap -= 1

        #Carga de intrucciones en el swap
        self._loader.swapIN(page.getBDPhysicalMemory(), page.getBDVirtualMemory())
        page.setBDPhysicalMemory(-1)
        page.change()

    # Proposito: Selecciona un marco usuado y le asigna un nuevo pid.
    # Precondicion: Hay al menos un frame libre en la memoria fisica
    def victimSelection(self, pid, pageNumber):
        # Para actualizar todos los frame antes de seleccionar una victima
        self._usedFramesPhysicalMemory.updateFrame(self._pcbTable)
        victimFrame = self._usedFramesPhysicalMemory.getVictim()
        self.assignFrameSwap(victimFrame)
        victimFrame.setPid(pid)
        victimFrame.setPageNumber(pageNumber)
        self._usedFramesPhysicalMemory.add(victimFrame)
        return victimFrame.getBD()

    # Proposito: Retorna true si page<page> con el pid<pid> ya fue cargada en swap.
    def isPageInSwap(self, page, pid):
        for usedFrame in self._usedFramesSwap:
            if page.getBDVirtualMemory()==usedFrame.getBD() and pid==usedFrame.getPId():
                return True
        return False


    # Proposito: Retorna true si hay al menos un marco en la memoria fisica.
    def thereIsSpaceInMemory(self):
        return self._cantFreeFramesPhysicalMemory > 0

    # Proposito: Retorna true si hay al menos un marco en la swap.
    def thereIsSpaceInSwap(self):
        return self._cantFreeFramesSwap > 0

    # Proposito: Retorna una cantidad de marcos x segun el size de la memoria.
    def calculateFreeFrames(self, sizeMemory):
        result = []
        for i in range(0, (sizeMemory // self._sizeFrame)):
            result.append(Frame(i * self._sizeFrame))
        return result

    # Proposito: Retorna los marcos usados en la memoria fisica
    def getUsedFramesPhysicalMemory(self):
        return self._usedFramesPhysicalMemory

    # Proposito: Libera marcos ocupadas por un por el <pid> en la memoria fisica y swap.
    def freeMemory(self, pid):
        self.removeUsedPhysicalMemory(pid)
        self.removeUsedSwap(pid)

    # Proposito: Libera marcos ocupadas por un procedimiento en la memoria.
    def removeUsedPhysicalMemory(self, pid):
        framesUsed = self.getFrameUsedMemory(pid)
        for frame in framesUsed:
            frame.setPid(-1)
            frame.setPageNumber(-1)
            self._usedFramesPhysicalMemory.removeFrame(frame)
            self._freeFramesPhysicalMemory.append(frame)
            self._cantFreeFramesPhysicalMemory+=1

    # Proposito: Libera los marcos ocupados por un procedimiento en el swap
    def removeUsedSwap(self, pid):
        frameUsed = self.getFrameUsedSwap(pid)
        for frame in frameUsed:
            frame.setPid(-1)
            frame.setPageNumber(-1)
            self._usedFramesSwap.remove(frame)
            self._freeFramesSwap.append(frame)
            self._cantFreeFramesSwap += 1

    # Proposito: Retorna la cantidad de marcos dispobibles de la memoria fisica.
    def sizeFreePhysicalMemory(self):
        return self._cantFreeFramesPhysicalMemory

    # Proposito: Retorna la cantidad de marcos dispobibles de la memoria swap.
    def sizeFreeSwap(self):
        return self._cantFreeFramesSwap

    # Proposito: Retorna el tamaño del marco.
    def sizeFrame(self):
        return self._sizeFrame

    # Proposito: Retorna el frame con <bd>
    # Precondicion: Debe existir <bd> en self._usedFramesSwap
    def getFrameUsedSwap(self, pid):
        res = []
        for frameUsed in self._usedFramesSwap:
            if frameUsed.getPId() == pid:
                res.append(frameUsed)
        return  res

    # Proposito: Retorna el frame con <bd>
    # Precondicion: Debe existir <bd> en self._usedFramesPhysicalMemory
    def getFrameUsedMemory(self, pid):
        return self._usedFramesPhysicalMemory.getFrame(pid)

    # Solo para la impresion
    def isMemoryManagerPaging(self):
        return True

    # Proposito: Retorna los marcos libres de la memoria fisica
    def getFreeFrames(self):
        return self._freeFramesPhysicalMemory

    # Proposito: Retorna el swap.
    def getSwap(self):
        return self._swap

    # Es para no hacer la interrupcion swapIN (el memoryManager y el loader se conocen mutuamente)
    def setLoader(self, loader):
        self._loader = loader

    def __repr__(self):
        usedFrames = []
        for uf in self._usedFramesPhysicalMemory.getUsedFrames():
            usedFrames.append([uf])
        freeFrames = []
        for ff in self._freeFramesPhysicalMemory:
            freeFrames.append([ff])
        usedFramesSwap = []
        for ufs in self._usedFramesSwap:
            usedFramesSwap.append([ufs])
        freeFramesSwap = []
        for ffs in self._freeFramesSwap:
            freeFramesSwap.append([ffs])
        return "{p1}\n{p2}\n{p3}\n{p4}".format(p1=tabulate(usedFrames, headers=['Used Frames Memory           '], tablefmt='psql'),p2=tabulate(freeFrames, headers=['Free Frames Memory ={uff:2d}       '.format(uff=self._cantFreeFramesPhysicalMemory)], tablefmt='psql'), p3=tabulate(usedFramesSwap, headers=['Used Frames Swap             '], tablefmt='psql'), p4=tabulate(freeFramesSwap, headers=['Free Frames Swap ={ufs:2d}         '.format(ufs=self._cantFreeFramesSwap)], tablefmt='psql'))


class PageReplacementAlgorithm:
    def __init__(self):
        self._usedFrames = QueueFIFO()

    # Proposito: Remueve un marco de la queue
    # precondcion: Debe existir <frame> en self._usedFrames
    def removeFrame(self, frame):
        self._usedFrames.remove(frame)

    # Proposito: Retorna los frame con los pid<pid>
    def getFrame(self, pid):
        res = []
        for frameUsed in self.getUsedFrames():
            if frameUsed.getPId() == pid:
                res.append(frameUsed)
        return  res

    # Proposito: Retorna la lista de frames usados en la memoria fisica
    def getUsedFrames(self):
        return self._usedFrames.list()

    # Proposito: Retorna el frame con el bd<bd>
    # Precondicion: Debe existir dicho frame
    def searchFrame(self, bd):
        for frameUsed in self.getUsedFrames():
            if frameUsed.getBD() == bd:
                return frameUsed

    # Proposito: Actualiza bit de referencia de las frame que fueron asignados a las pages<pages>
    def updateFrame(self, pcbTable):
        pass


class FirstInFirstOutPageReplacementAlgorithm(PageReplacementAlgorithm):

    # Proposito: Agrega un marco a la queue
    def add(self, frame):
        self._usedFrames.add(frame)

    # Proposito: Selecciona un marco como victima y la retorna
    # Precondicion: Debe haber al menos un marco en self._usedFrames
    def getVictim(self):
        return self._usedFrames.pop()


class SecondChancePageReplacementAlgorithm(PageReplacementAlgorithm):

    # Proposito: Agrega un frame en la queue
    def add(self, frame):
        frame.setReferenceBit(1)
        self._usedFrames.add(frame)

    # Proposito: Selecciona un marco como victima y la retorna
    # Precondicion: Debe haber al menos un marco en self._usedFrames
    def getVictim(self):
        referenceBit = 1
        usedFrame = None
        while referenceBit != 0:
            usedFrame = self._usedFrames.pop()
            if usedFrame.getReferenceBit() == 1:
                usedFrame.setReferenceBit(0)
                self._usedFrames.add(usedFrame)
            else:
                referenceBit = 0
        return usedFrame

    # Proposito: Actualiza bit de referencia de las frame que fueron asignados a las pages<pages>
    def updateFrame(self, pcbTable):
        for unFrame in self._usedFrames.list():
            pcb = pcbTable.lookUpPCB(unFrame.getPId())
            page = pcb.getPageTable().searchPage(unFrame.getBD())
            if page.getReferenceBit() == 1:
                unFrame.setReferenceBit(1)
                page.setReferenceBit(0)

class ClockPageReplacementAlgorithm(PageReplacementAlgorithm):
    def __init__(self):
        self._target         = -1
        self._sizeFrameClock =  0

    # Proposito: Retorna la cantidad total de frames usados
    def getSizeFrameClock(self):
        return self._sizeFrameClock

    # Proposito: Retorna el target
    def getTarget(self):
        return self._target

    # Proposito: Setea el target
    def setTarget(self, target):
        self._target = target

    # Proposito: Agrega un frame
    def add(self, oneFrame):
        oneFrame.setReferenceBit(1)
        self._sizeFrameClock += 1
        if self._target == -1:
            self._target = oneFrame
            self._target.updatePreviousFrameClock(self._target)
            self._target.updateNextFrameClock(self._target)
        else:
            oneFrame.updatePreviousFrameClock(self._target.getPreviousFrameClock())
            oneFrame.updateNextFrameClock(self._target)
            if self._sizeFrameClock == 2:
                self._target.updateNextFrameClock(oneFrame)
            else:
                self._target.getPreviousFrameClock().updateNextFrameClock(oneFrame)
            self._target.updatePreviousFrameClock(oneFrame)

    # Proposito: Selecciona un marco como victima y la retorna
    # Precondicion: Debe haber al menos un marco usado en la memoria fisica
    def getVictim(self):
        while self._target.getReferenceBit() == 1:
            self._target.setReferenceBit(0)
            nextTarget = self._target.getNextFrameClock()
            self._target = nextTarget
        victim = self._target
        newTarget = self._target.getNextFrameClock()
        newTarget.updatePreviousFrameClock(self._target.getPreviousFrameClock())
        self._target = newTarget
        self._sizeFrameClock -= 1
        return victim

    # Proposito: Retorna el frame con el bd<bd>
    # Precondicion: Debe existir dicho frame
    def searchFrame(self, bd):
        searchFrame = self._target
        while searchFrame.getBD() != bd:
            searchFrame = searchFrame.getNextFrameClock()
        return searchFrame

    # Proposito: Actualiza bit de referencia de las frame que fueron asignados a las pages<pages>
    def updateFrame(self, pcbTable):
        frameTravel = self._target
        for index in range(0, self.getSizeFrameClock()):
            pcb = pcbTable.lookUpPCB(frameTravel.getPId())
            page = pcb.getPageTable().searchPage(frameTravel.getBD())
            if page.getReferenceBit() == 1:
                frameTravel.setReferenceBit(1)
                page.setReferenceBit(0)
            frameTravel = frameTravel.getNextFrameClock()

    # Proposito: Remueve el frame<frame>
    # precondcion: Debe existir <frame>
    def removeFrame(self, frame):
        self._sizeFrameClock -= 1
        nextFrame = frame.getNextFrameClock()
        previousFrame = frame.getPreviousFrameClock()
        nextFrame.updatePreviousFrameClock(previousFrame)
        previousFrame.updateNextFrameClock(nextFrame)
        if self.getSizeFrameClock() == 0:
            self.setTarget(-1)
        elif frame == self.getTarget():
            self.setTarget(frame.getNextFrameClock())

    # Proposito: Retorna la lista de frames usados en la memoria fisica
    def getUsedFrames(self):
        collectionFrame = []
        frameTravel = self._target
        for index in range(0, self.getSizeFrameClock()):
            collectionFrame.append(frameTravel)
            frameTravel = frameTravel.getNextFrameClock()
        return collectionFrame

