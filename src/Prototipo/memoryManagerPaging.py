# !/usr/bin/env python
# -*- coding: utf-8 -*-s

from tabulate import tabulate

from Prototipo.Schedulers.Tuple import Tuple
from Prototipo.Schedulers.queues import QueueFIFO
from Prototipo.frame import Frame
from Prototipo.intManager import Irq


class MemoryManagerPaging:
    def __init__(self, memory, sizeFrame, PCBTable, swap, pageReplacementAlgorithm, intManager):
        self._memory                       = memory
        self._sizeFrame                    = sizeFrame
        self._pcbTable                     = PCBTable
        self._swap                         = swap
        self._intManager                   = intManager
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
    def assignFrame(self, pid):
        if self.thereIsSpaceInMemory():

            return self.assignFramePhysicalMemory(pid)

        elif self.thereIsSpaceInSwap():

            return self.victimSelection(pid)

        else:

            raise SystemError("Insufficient memory")


    # Proposito:te asigna un marco libre en la memoryPyhisical.
    # Precondicion: hay al menos un frame en self._freeFramesPhysicalMemory
    def assignFramePhysicalMemory(self, pid):
        newUsedFrame = self._freeFramesPhysicalMemory.pop(0)
        newUsedFrame.setPid(pid)
        newUsedFrame.setUsed(True)
        self._usedFramesPhysicalMemory.add(newUsedFrame)
        self._cantFreeFramesPhysicalMemory -= 1
        return newUsedFrame.getBD()

    # Proposito:te asigna un marco libre del swap.
    # Precondicion: hay al menos un frame en self._freeFramesVirtualMemory
    def assignFrameSwap(self, victimFrame):
        pcb = self._pcbTable.lookUpPCB(victimFrame.getPId())
        page = pcb.getPageTable().searchPage(victimFrame.getBD())
        newUsedFrame = self._freeFramesSwap.pop(0)
        newUsedFrame.setUsed(True)
        newUsedFrame.setPid(victimFrame.getPId())
        self._usedFramesSwap.append(newUsedFrame)
        page.setBDVirtualMemory(newUsedFrame.getBD())
        self._cantFreeFramesSwap -= 1
        self._intManager.handle(Irq.IN_SWAP, page)

    #Proposito:selecciona un marco usuado y le asigna un nuevo pid.
    #Precondicion: hay al menos un frame en self._freeFramesVirtualMemory
    def victimSelection(self, pid):
        victimFrame = self._usedFramesPhysicalMemory.getVictim()
        self.assignFrameSwap(victimFrame)
        victimFrame.setPid(pid)
        self._usedFramesPhysicalMemory.add(victimFrame)
        return victimFrame.getBD()


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


    def freeFramesPhysicalMemory(self):
        return self._freeFramesPhysicalMemory

    def usedFramesPhysicalMemory(self):
        return self._usedFramesPhysicalMemory

    def freeFramesSwap(self):
        return self._freeFramesSwap

    def usedFramesSwap(self):
        return self._usedFramesSwap


    # Proposito:libera marcos ocupadas por un por el <pid> en la memoria fisica y swap.
    # Precondicion:-
    def freeMemory(self, pid):
        self.removeUsedPhysicalMemory(pid)
        self.removeUsedSwap(pid)

    # mirar bien (SOlo para mi nahuel)
    #
    #def changeUsedFramesToFree(self, pid,framesUsed,collectionUsedFrame,collectionFreeFrame,cantFreeFrames):
    #    for frame in framesUsed:
    #        frame.setPid(-1)
    #        frame.setUsed(False)
    #        collectionUsedFrame.removeFrame(frame)
    #        collectionFreeFrame.append(frame)
    #        cantFreeFrames+=1



    # Proposito: libera marcos ocupadas por un procedimiento en la memoria.
    # Precondicion: Deben existir los frame con los bds de <pages> en self._usedFramesPhysicalMemory
    def removeUsedPhysicalMemory(self, pid):
        frameUsed = self.getFrameUsedMemory(pid)
        for frame in frameUsed:
            frame.setPid(-1)
            frame.setUsed(False)
            self._usedFramesPhysicalMemory.removeFrame(frame)
            self._freeFramesPhysicalMemory.append(frame)
            self._cantFreeFramesPhysicalMemory+=1

    #Proposito: libera los marcos ocupados por un procedimiento en el swap
    #Precondicion: Deben existir los frame con los bds de <pages> en self._usedFramesSwap
    def removeUsedSwap(self, pid):
        frameUsed = self.getFrameUsedSwap(pid)
        for frame in frameUsed:
            frame.setPid(-1)
            frame.setUsed(False)
            self._usedFramesSwap.remove(frame)
            self._freeFramesSwap.append(frame)
            self._cantFreeFramesSwap += 1

    #Proposito: Mueve al frame con bd <bdVirtualMemory> de self._usedFramesSwap a self._freeFramesSwap
    #Precondicion: Debe existir el frame con bd <bdVirtualMemory> en self._usedFramesSwap
    def moveToFreeSwap(self, bdVirtualMemory):
        frameToFree = self.getFrameUsedSwap(bdVirtualMemory)
        frameToFree.setPid(-1)
        frameToFree.setUsed(False)
        self._freeFramesSwap.append(frameToFree)
        self._usedFramesSwap.remove(frameToFree)
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
        return "{p1}\n{p2}\n{p3}\n{p4}".format(p1=tabulate(usedFrames, headers=['Used Frames Memory   '], tablefmt='psql'),p2=tabulate(freeFrames, headers=['Free Frames Memory   '], tablefmt='psql'), p3=tabulate(usedFramesSwap, headers=['Used Frames SWAP     '], tablefmt='psql'), p4=tabulate(freeFramesSwap, headers=['Free Frames SWAP     '], tablefmt='psql'))


class FirstInFirstOutPageReplacementAlgorithm:
    def __init__(self):
        self._usedFrames = QueueFIFO()

    #Proposito:Agrega un marco a la queue
    #Precondicion:---
    def add(self, frame):
        self._usedFrames.add(frame)

    #Proposito:remueve un marco de la queue
    #precondcion: debe existir <frame> en self._usedFrames
    def removeFrame(self, frame):
        self._usedFrames.remove(frame)

    #Proposito: retorna un frame con el <bd>
    #Precondicion: debe existir <bd> en self._usedFrames
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

    #Proposito: setea una lista
    #Precondicion:-
    def setQueue(self, queue):
        self._usedFrames.setQueue(queue)

'''
# !/usr/bin/env python
# -*- coding: utf-8 -*-s

from tabulate import tabulate

from Prototipo.Bloque import Block
from Prototipo.intManager import Irq

class MemoryManagerFrame:
    def __init__(self, memory, sizeFrame, PCBTable, cantFramesForPCB, swap):
        self._memory           = memory
        self._sizeFrame        = sizeFrame
        self._cantFreePages    = 0
        self._freeFrames       = self.calculateFreeFrames(self._memory.size())
        self._usedFrames       = []
        self._pcbTable         = PCBTable
        self._swap             = swap
        self._bitForReference  = 0

    # Proposito:cede un marco.
    # Precondiccion: -
    def returnRequiredPages(self, pid):

        if self.thereIsSpaceInMemoryFor():

            frame = self._freeFrames.pop(0)
            frame.setPid(pid)
            frame.setUsed(True)
            self._usedFrames.append(frame)
            self._cantFreePages -= 1
            return frame.getBD()

        elif self._swap.thereIsSpaceInMemory():

            return self.victimSelection(pid)

        else:

            raise SystemError("Insufficient memory")

    # Proposito:Denota true si hay al menos un 1 espacio,caso contrario False
    # Precondiccion:-
    def thereIsSpaceInMemoryFor(self):
        return self._cantFreePages > 0

    # Proposito:retorna los marcos de la memoria.
    # Precondiccion: -
    def calculateFreeFrames(self, sizeMemory):
        result = []
        for i in range(0, (sizeMemory // self._sizeFrame)):
            result.append(Frame(i * self._sizeFrame))
            self._cantFreePages+=1
        return result

    # Proposito:libera marcos ocupadas por un procedimiento en la memoria.
    # Precondicion:-
    def freeMemory(self, pages):
        for page in pages:
            frameUsed=self.getFrameUsed(page.getBDPhysicalMemory())
            frameUsed.setPid(-1)
            frameUsed.setUsed(False)
            self._freeFrames.append(frameUsed)
            self._usedFrames.remove(frameUsed)
            self._cantFreePages+=1


    #Proposito:Retorna la cantidad de paginas disponibles
    def sizeFree(self):
        return self._cantFreePages

    #Proposito:Retorna el tamaño del marco
    #Precondicion:-
    def sizeFrame(self):
        return self._sizeFrame

    def getFrameUsed(self,bd):
        for frameUsed in self._usedFrames:
            if frameUsed.getBD() == bd:
                return frameUsed
        raise SystemError("ROMPIO")

    def isMemoryManagerPaging(self):
        return True

    def getFreeFrames(self):
        return self._freeFrames

    def getSwap(self):
        return self._swap

    def __repr__(self):
        usedFrames = []
        for uf in self._usedFrames:
            usedFrames.append([uf])
        freeFrames = []
        for ff in self._freeFrames:
            freeFrames.append([ff])
        return "{p1}\n{p2}".format(p1=tabulate(usedFrames, headers=['Used Frames Memory   '], tablefmt='psql'),p2=tabulate(freeFrames, headers=['Free Frames Memory   '], tablefmt='psql'))

class MemoryManagerFrameFIFO(MemoryManagerFrame):

    def victimSelection(self,pid):
        #self.ordering()
        if len(self._usedFrames)>0:
            victimFrame=self._usedFrames.pop(0)
            pcb=self._pcbTable.lookUpPCB(victimFrame.getPId())
            page=pcb.getPageTable().searchPage(victimFrame.getBD())
            page.change()
            self._swap.assignSpace(page,pcb.get_pid())
            victimFrame.setPid(pid)
            self._usedFrames.append(victimFrame)
            return victimFrame.getBD()
        else:
            raise SystemError("ROMPIO EN VICTIMA")

    def ordering(self):
        for i in range(1, len(self._usedFrames)):
            for j in range(0, len(self._usedFrames) - i):
                if self._usedFrames[j].getBD() > self._usedFrames[j + 1].getBD():
                    k = self._usedFrames[j + 1]
                    self._usedFrames[j + 1] = self._usedFrames[j]
                    self._usedFrames[j] = k

class Frame:
    def __init__(self,bd):
        self._bd=bd
        self._used=False
        self._pid=-1
        self._bitForAlgorithm=False

    def getBD(self):
        return self._bd

    def isUsed(self):
        return self._used

    def setUsed(self,valid):
        self._used=valid

    def setPid(self,pid):
        self._pid=pid

    def getPId(self):
        return self._pid

    def __repr__(self):
        return "Pid={pid:2d}   Bd={bd:2d}   Used={used:1}".format(pid=self._pid, bd=self._bd, used=self._used)
'''