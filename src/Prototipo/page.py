class Page:
    def __init__(self):
        self._bdPhysicalMemory = -1
        self._bdVirtualMemory  = -1
        self._physicalMemory   = False
        self._swap             = False
        self._referenceBit = 0

    #Proposito:Retorna el bd en memoria fisica
    #Precondicion:-
    def getBDPhysicalMemory(self):
        return self._bdPhysicalMemory

    #Proposito:retorna el bd en swap
    #Precondicion:-
    def getBDVirtualMemory(self):
        return self._bdVirtualMemory

    #Proposito:retorna el bit de referencia.
    #Precondicion:
    def getReferenceBit(self):
        return self._referenceBit

    #Proposito: setea el bit<bit> de referencia
    #Precondicion:-
    def setReferenceBit(self,bit):
        self._referenceBit=bit

    #Proposito:setea el bd<bd> del swap
    #Precondicion:-
    def setBDVirtualMemory(self, bd):
        self._bdVirtualMemory = bd

    #Proposito:setea el bd<bd> de la memoria fisica.
    #Precondicion:-
    def setBDPhysicalMemory(self, bd):
        self._bdPhysicalMemory = bd

    #Proposito:setea el valid<valid> del swap.
    #Precondicion:-
    def setSwap(self,valid):
        self._swap=valid

    #Proposito:setea el valid<valid> de la memoria fisica.
    #Precondicion:
    def setPhysicalMemory(self, valid):
        self._physicalMemory=valid

    #Proposito:Retorna true si esta en memoria fisica
    #Precondicion:-
    def isInPhysicalMemory(self):
        return self._physicalMemory

    #Proposito:retorna true si esta en swap.
    #Precondicion:-
    def inSwap(self):
        return self._swap

    #Proposito:Retorna true si esta en swap y no esta en memoria fisica.
    #Precondicion:-
    def isInSwapOrDisk(self):
        return self.inSwap() or not self.isInPhysicalMemory()


    #Proposito:cambia los estados de swap al contrario visebersa para estado de physicalMemory.
    #Precondicion:-
    def change(self):
        self.setSwap(not self._swap)
        self.setPhysicalMemory(not self._physicalMemory)

    def __repr__(self):
        return "bdMemory={p:2d}  bdSwap={b:2d}  isInMemory={e:1}  isInSwap={c:1} \n".format(p=self._bdPhysicalMemory,b=self._bdVirtualMemory,e=self._physicalMemory,c=self._swap)
