# !/usr/bin/env python
# -*- coding: utf-8 -*-s

from tabulate import tabulate

from Prototipo.Schedulers.queues import QueueFIFO
from Prototipo.frame import Frame
from Prototipo.intManager import Irq


class MemoryManagerPaging:
    def __init__(self, memory, sizeFrame, PCBTable, swap, pageReplacementAlgorithm, intManager, loader):
        self._memory                       = memory
        self._sizeFrame                    = sizeFrame
        self._pcbTable                     = PCBTable
        self._swap                         = swap
        self._intManager                   = intManager
        self._loader                       = loader
        ##MARCOS DEL LA MEMORIA FISICA
        self._freeFramesPhysicalMemory     = self.calculateFreeFrames(self._memory.size())
        self._usedFramesPhysicalMemory     = pageReplacementAlgorithm
        self._cantFreeFramesPhysicalMemory = len(self._freeFramesPhysicalMemory)
        ##MARCOS DEL SWAP
        self._freeFramesSwap               = self.calculateFreeFrames(self._memory.size() * 2)
        self._usedFramesSwap               = []
        self._cantFreeFramesSwap           = len(self._freeFramesSwap)


    # Proposito:Si tiene un marco de la memoria fisica lo retorna en caso q no busca uno del swap en caso
    # que no tenga ninguno de los dos levanta una exepcion
    # Precondiccion: -
    def assignFrame(self, pid, pageNumber):
        if self.thereIsSpaceInMemory():

            return self.assignFramePhysicalMemory(pid, pageNumber)

        elif self.thereIsSpaceInSwap():
            #Para actualizar todos los frame antes de seleccionar una victima
            self._usedFramesPhysicalMemory.updateFrame(self._pcbTable)
            return self.victimSelection(pid, pageNumber)

        else:

            raise SystemError("Insufficient memory")


    # Proposito:te asigna un marco libre en la memoryPyhisical.
    # Precondicion: hay al menos un frame en self._freeFramesPhysicalMemory
    def assignFramePhysicalMemory(self, pid, pageNumber):
        newUsedFrame = self._freeFramesPhysicalMemory.pop(0)
        newUsedFrame.setPid(pid)
        newUsedFrame.setPageNumber(pageNumber)
        self._usedFramesPhysicalMemory.add(newUsedFrame)
        self._cantFreeFramesPhysicalMemory -= 1
        return newUsedFrame.getBD()

    # Proposito:te asigna un marco libre del swap.
    # Precondicion: hay al menos un frame en self._freeFramesVirtualMemory
    def assignFrameSwap(self, victimFrame):
        #busco la pagina de la del frame que seleccione como victima
        pidVictimFrame=victimFrame.getPId()
        pcb = self._pcbTable.lookUpPCB(pidVictimFrame)
        page = pcb.getPageTable().searchPage(victimFrame.getBD())

        #verifico si ya habia sido cargada la pagina en el swap para no volver a cargar.
        if self.isPageInSwap(page, pidVictimFrame):
            return

        #En caso que no este pido un frame en el swap
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

        #self._intManager.handle(Irq.IN_SWAP, page)

    #Proposito:selecciona un marco usuado y le asigna un nuevo pid.
    #Precondicion: hay al menos un frame en self._freeFramesVirtualMemory
    def victimSelection(self, pid, pageNumber):
        victimFrame = self._usedFramesPhysicalMemory.getVictim()
        self.assignFrameSwap(victimFrame)
        victimFrame.setPid(pid)
        victimFrame.setPageNumber(pageNumber)
        self._usedFramesPhysicalMemory.add(victimFrame)
        return victimFrame.getBD()

    #Proposito:Denota true si page<page> con el pid<pid> ya fue cargada en swap.
    #Precondcion:-
    def isPageInSwap(self, page, pid):
        for usedFrame in self._usedFramesSwap:
            if page.getBDVirtualMemory()==usedFrame.getBD() and pid==usedFrame.getPId():
                return True
        return False


    # Proposito:denota true si hay al menos un marco en la memoria fisica.
    # Precondiccion:-
    def thereIsSpaceInMemory(self):
        return self._cantFreeFramesPhysicalMemory > 0

    #Proposito:denota true si hay al menos un marco en la swap.
    #
    def thereIsSpaceInSwap(self):
        return self._cantFreeFramesSwap > 0

    # Proposito:retorna una cantidad de marcos x segun el size de la memoria.
    # Precondiccion: -
    def calculateFreeFrames(self, sizeMemory):
        result = []
        for i in range(0, (sizeMemory // self._sizeFrame)):
            result.append(Frame(i * self._sizeFrame))
        return result

    def getUsedFramesPhysicalMemory(self):
        return self._usedFramesPhysicalMemory

    # Proposito:libera marcos ocupadas por un por el <pid> en la memoria fisica y swap.
    # Precondicion:-
    def freeMemory(self, pid):
        self.removeUsedPhysicalMemory(pid)
        self.removeUsedSwap(pid)

    # Proposito: libera marcos ocupadas por un procedimiento en la memoria.
    # Precondicion: Deben existir los frame con los bds de <pages> en self._usedFramesPhysicalMemory
    def removeUsedPhysicalMemory(self, pid):
        frameUsed = self.getFrameUsedMemory(pid)
        for frame in frameUsed:
            frame.setPid(-1)
            frame.setPageNumber(-1)
            self._usedFramesPhysicalMemory.removeFrame(frame)
            self._freeFramesPhysicalMemory.append(frame)
            self._cantFreeFramesPhysicalMemory+=1

    #Proposito: libera los marcos ocupados por un procedimiento en el swap
    #Precondicion: Deben existir los frame con los bds de <pages> en self._usedFramesSwap
    def removeUsedSwap(self, pid):
        frameUsed = self.getFrameUsedSwap(pid)
        for frame in frameUsed:
            frame.setPid(-1)
            frame.setPageNumber(-1)
            self._usedFramesSwap.remove(frame)
            self._freeFramesSwap.append(frame)
            self._cantFreeFramesSwap += 1

    #Proposito:Retorna la cantidad de marcos dispobibles de la memoria fisica.
    def sizeFreePhysicalMemory(self):
        return self._cantFreeFramesPhysicalMemory

    # Proposito:Retorna la cantidad de marcos dispobibles de la memoria swap.
    def sizeFreeSwap(self):
        return self._cantFreeFramesSwap

    #Proposito:Retorna el tamaño del marco.
    #Precondicion:-
    def sizeFrame(self):
        return self._sizeFrame

    #Proposito: retorna el frame con <bd>
    #Precondicion: debe existir <bd> en self._usedFramesSwap
    def getFrameUsedSwap(self, pid):
        res=[]
        for frameUsed in self._usedFramesSwap:
            if frameUsed.getPId() == pid:
                res.append(frameUsed)
        return  res
    #Proposito: retorna el frame con <bd>
    #Precondicion: debe existir <bd> en self._usedFramesPhysicalMemory
    def getFrameUsedMemory(self, pid):
        return self._usedFramesPhysicalMemory.getFrame(pid)

    def isMemoryManagerPaging(self):
        return True

    #Proposito:retorna los marcos libres de la memoria fisica
    #Precondicion:-----
    def getFreeFrames(self):
        return self._freeFramesPhysicalMemory

    #PRoposito:retorna el swap.
    #PRecondicion:
    def getSwap(self):
        return self._swap

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

    #Proposito:remueve un marco de la queue
    #precondcion: debe existir <frame> en self._usedFrames
    def removeFrame(self, frame):
        self._usedFrames.remove(frame)

    #Proposito: retorna los frame con los pid<pid>
    #Precondicion: -
    def getFrame(self, pid):
        res=[]
        for frameUsed in self.getUsedFrames():
            if frameUsed.getPId() == pid:
                res.append(frameUsed)
        return  res

    #Proposito:retorna la lista de la queue
    #Proposito:-
    def getUsedFrames(self):
        return self._usedFrames.list()

    #Proposito: selecciona un marco como victima y la retorna
    #Precondicion:-
    def getVictim(self):
        return self._usedFrames.pop()

    # Proposito: Actualiza el frame referenciado
    # precondcion: debe existir el frame con el bd<bd> en self._usedFrames
    def updateReferenceBit(self,bd):
        pass

    #Proposito:retorna el frame con el bd<bd>
    #Precondicion:debe existir dicho frame
    def searchFrame(self, bd):
        for frameUsed in self.getUsedFrames():
            if frameUsed.getBD() == bd:
                return frameUsed


class FirstInFirstOutPageReplacementAlgorithm(PageReplacementAlgorithm):
    def __init__(self):
        self._usedFrames = QueueFIFO()

    #Proposito:Agrega un marco a la queue
    #Precondicion:---
    def add(self, frame):
        self._usedFrames.add(frame)

    #Proposito: selecciona un marco como victima y la retorna
    #Precondicion:-
    def getVictim(self):
        return self._usedFrames.pop()


class SecondChancePageReplacementAlgorithm(PageReplacementAlgorithm):
    def __init__(self):
        self._usedFrames = QueueFIFO()

    # Proposito:Agrega un marco a la queue
    # Precondicion:---
    def add(self, frame):
        frame.setReferenceBit(1)
        self._usedFrames.add(frame)

    # Proposito: selecciona un marco como victima y la retorna
    # Precondicion:-
    def getVictim(self):
        referenceBit=1
        usedFrame=None
        while referenceBit != 0:
            usedFrame = self._usedFrames.pop()
            if usedFrame.getReferenceBit() == 1:
                usedFrame.setReferenceBit(0)
                self._usedFrames.add(usedFrame)
            else:
                referenceBit = 0
        return usedFrame

    #Proposito:actualiza el bit de referencia del frame con el bd<bd>
    #Precondicion:---
    def updateReferenceBit(self, bd):
        self.searchFrame(bd).setReferenceBit(1)

    #proposito:Actualiza bit de referencia de las frame que fueron asignados a las pages<pages>
    #Precondicion:-
    def updateFrame(self,pcbTablet):
        for unFrame in self._usedFrames:
            pcb=pcbTablet.lookUpPCB(unFrame.getPId())
            page=pcb.getPageTable().searchPage(unFrame.getBD())
            if page.getReferenceBit()==1:
                unFrame.setReferenceBit(1)
                page.setReferenceBit(0)




class LeastRecentlyUsedPageReplacementAlgorithm(PageReplacementAlgorithm):
    def __init__(self):
        self._usedFrames = []
        self._countTimer = 0

    #Proposito:Agrega un marco a la queue
    #Precondicion:---
    def add(self, frame):
        frame.setTimeBit(self._countTimer)
        self._usedFrames.append(frame)
        self._countTimer+=1

    #Proposito:selecciona una victima y la retorna
    #Precondicion:la lista de usedFrame debe de haber al menos uno
    def getVictim(self):
        minFrame = self._usedFrames[0]
        lenUsedFrames = len(self._usedFrames)
        if lenUsedFrames > 1:
            for index in range(1, lenUsedFrames):
                compare = self._usedFrames[index]
                if minFrame.getTimeBit() > compare.getTimeBit():
                    minFrame = compare
        self._usedFrames.remove(minFrame)
        return minFrame

    #Proposito:actualiza el bit de tiempo del frame con el bd<bd>
    #Precondicion:---
    def updateReferenceBit(self, bd):
        self.searchFrame(bd).setTimeBit(self._countTimer)
        self._countTimer+=1

    # Proposito:retorna la lista de frames usados
    # Proposito:-
    def getUsedFrames(self):
        return self._usedFrames


class LeastRecentlyUsedPageReplacementAlgorithmWithQueue(FirstInFirstOutPageReplacementAlgorithm):

    #Proposito:actualiza el bit de tiempo del frame con el bd<bd>
    #Precondicion:---
    def updateReferenceBit(self, bd):
        frameReferenced = self.searchFrame(bd)
        self._usedFrames.remove(frameReferenced)
        self.add(frameReferenced)

