class Page:
    def __init__(self):
        self._bdPhysicalMemory = -1
        self._bdVirtualMemory  = -1
        self._physicalMemory   = False
        self._swap             = False

    def getBDPhysicalMemory(self):
        return self._bdPhysicalMemory

    def getBDVirtualMemory(self):
        return self._bdVirtualMemory

    def setBDVirtualMemory(self, bd):
        self._bdVirtualMemory = bd

    def setBDPhysicalMemory(self, bd):
        self._bdPhysicalMemory = bd

    def setSwap(self,valid):
        self._swap=valid

    def setPhysicalMemory(self, valid):
        self._physicalMemory=valid

    def isInPhysicalMemory(self):
        return self._physicalMemory

    def inSwap(self):
        return self._swap

    def isInSwapOrDisk(self):
        return self.inSwap() or not self.isInPhysicalMemory()

        # return self.inSwap() or self._bdPhysicalMemory == -1

    #Proposito:cambia los estados de swap al contrario visebersa para estado de physicalMemory.
    #Precondicion:-
    def change(self):
        self.setSwap(not self._swap)
        self.setPhysicalMemory(not self._physicalMemory)

    def __repr__(self):
        return "Page: bdMemory={p:2d}  bdSwap={b:2d}  isInMemory={e:1}  isInSwap={c:1} \n".format(p=self._bdPhysicalMemory,b=self._bdVirtualMemory,e=self._physicalMemory,c=self._swap)
