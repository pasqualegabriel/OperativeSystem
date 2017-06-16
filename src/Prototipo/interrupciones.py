# !/usr/bin/env python
# -*- coding: utf-8 -*-s

from Prototipo.pcb import PCB

class Interrupcion:
    #Proposito:Retorna el pcb que esta actualmente corriendo en el cpu.
    #Precondicion:Debe de haber un pcb cargado.
    def getPCBInCPU(self):
        return self._pcbTable.lookUpPCB(self._dispatcher.getPidActual())

    #Propositon:Retorna el pcb q pertenece al <pid>
    #Precondicion:Debe existir dicho pcb.
    def getPCB(self,pid):
        return self._pcbTable.lookUpPCB(pid)

    def getPIDInCPU(self):
        return self._dispatcher.getPidActual()


class ChangePCBofCPU(Interrupcion):
    # Proposito:Verifica si el es preventivo y si hay que hacer un cambio de procedimiento en el cpu.
    # Precondicion:-
    def isPreemptiveAndIsChange(self, pcb):
        return self._scheduler.isPreemptive() and self._scheduler.isChange(self.getPCBInCPU(), pcb)

    # Proposito:Saca el pcb que esta en cpu corriendo el cpu lo actualiza, lo guarda, y carga otro pcb.
    # Precondicion:-
    def changeOfPCBInCPU(self, pcb):
        pcbEnCPU = self.getPCBInCPU()
        self._dispatcher.save(pcbEnCPU)
        pcbEnCPU.set_status("ready")
        self._scheduler.add(pcbEnCPU)
        pcb.set_status("running")
        self._dispatcher.load(pcb)

    # Proposito:Carga un procedimiento o cambia el procedimiento actual por otro; o encola pid del pcb.
    #
    def isLoadOrChangeOrTail(self, pcb):

        if self._dispatcher.isIdle():
            pcb.set_status("running")
            self._dispatcher.load(pcb)


        elif self.isPreemptiveAndIsChange(pcb):
            self.changeOfPCBInCPU(pcb)

        else:
            pcb.set_status("ready")
            self._scheduler.add(pcb)


class ContextSwitch(Interrupcion):
    #Proposito:Verifica si hay pid por encolar, en caso que haya pide uno y busca el pcb y setea estado a running y lo carga.
    #Precondcion:-
    def contextSwitch(self):
        if self._scheduler.notIsEmpty():
            pid = self._scheduler.pop()
            pcb = self._pcbTable.lookUpPCB(pid)
            pcb.set_status("running")
            self._dispatcher.load(pcb)

class New(ChangePCBofCPU):
    def __init__(self, loader, dispatcher, scheduler, pcbTable):
        self._nexPid     = 0
        self._loader     = loader
        self._scheduler  = scheduler
        self._dispatcher = dispatcher
        self._pcbTable   = pcbTable

    def execute(self, nameProgram):
        pcb = PCB(self._nexPid)
        self._loader.load(pcb, nameProgram)
        self._pcbTable.addPCB(pcb)
        self._nexPid += 1
        self.isLoadOrChangeOrTail(pcb)


class Kill(ContextSwitch):
    def __init__(self, loader, dispatcher, scheduler, pcbTable, timer, memoryManager):
        self._loader        = loader
        self._dispatcher    = dispatcher
        self._pcbTable      = pcbTable
        self._scheduler     = scheduler
        self._timer         = timer
        self._memoryManager = memoryManager

    def execute(self, p):
        pid = self._dispatcher.getPidActual()
        self._memoryManager.freeMemory(pid)
        self._pcbTable.removePCB(pid)
        self._dispatcher.idlePc()
        self.contextSwitch()
        if not self._timer is None:
            self._timer.set_timer()


class IoIn(ContextSwitch):
    def __init__(self, dispatcher, pcbTable, deviceManager, scheduler, timer):
        self._dispatcher    = dispatcher
        self._pcbTable      = pcbTable
        self._deviceManager = deviceManager
        self._scheduler     = scheduler
        self._timer         = timer

    def execute(self, io):
        pcbEnCPU = self.getPCBInCPU()
        self._dispatcher.save(pcbEnCPU)
        pcbEnCPU.set_status("waiting")
        self._deviceManager.add(self.getPIDInCPU(), io.getId())
        self._dispatcher.idlePc()
        self.contextSwitch()
        if not self._timer is None:
            self._timer.set_timer()

class IoOut(ChangePCBofCPU):
    def __init__(self, dispatcher, scheduler, pcbTable):
        self._dispatcher = dispatcher
        self._pcbTable   = pcbTable
        self._scheduler  = scheduler

    def execute(self, pid):
        pcb = self._pcbTable.lookUpPCB(pid)
        self.isLoadOrChangeOrTail(pcb)


class TimeOut(Interrupcion):
    def __init__(self, dispatcher, scheduler, pcbTable):
        self._dispatcher = dispatcher
        self._pcbTable = pcbTable
        self._scheduler = scheduler

    def execute(self, p):
        if not self._scheduler.notIsEmpty():
            return
        pcbEnCPU = self.getPCBInCPU()
        self._dispatcher.save(pcbEnCPU)
        self._dispatcher.idlePc()
        pcbEnCPU.set_status("ready")
        self._scheduler.add(pcbEnCPU)
        pidForAdd = self._scheduler.pop()
        pcbForAdd = self._pcbTable.lookUpPCB(pidForAdd)
        pcbForAdd.set_status("running")
        self._dispatcher.load(pcbForAdd)


class CompactMemory(Interrupcion):
    def __init__(self, dispatcher, pcbTable, memoryManager):
        self._dispatcher    = dispatcher
        self._pcbTable      = pcbTable
        self._memoryManager = memoryManager

    def execute(self, p):
        pcbInCpu = self.getPCBInCPU()
        self._dispatcher.save(pcbInCpu)
        self._dispatcher.idlePc()
        self._memoryManager.toCompact()
        self._dispatcher.load(pcbInCpu)



class PageFault(Interrupcion):
    def __init__(self, loader, scheduler, pcbTable, dispatcher,memoryManager):
        self._loader        = loader
        self._scheduler     = scheduler
        self._pcbTable      = pcbTable
        self._dispatcher    = dispatcher
        self._memoryManager = memoryManager

    def execute(self, pageForPageFault):
        pcbInCpu = self.getPCBInCPU()
        self._dispatcher.save(pcbInCpu)
        self._dispatcher.idlePc()
        if pageForPageFault.inSwap():
            bdVirtualMemory = pageForPageFault.getBDVirtualMemory()
            instructions = self._loader.swapOut(bdVirtualMemory)
            self._memoryManager.moveToFreeSwap(bdVirtualMemory)
            bdPyshicalMemory = self._memoryManager.assignFrame(pcbInCpu.get_pid())
            pageForPageFault.setBDPhysicalMemory(bdPyshicalMemory)
            pageForPageFault.change()
            self._loader.loadInPhysicalMemory(instructions, pageForPageFault)

        else:
            pc = pcbInCpu.get_pc()
            bdPyshicalMemory = self._memoryManager.assignFrame(pcbInCpu.get_pid())
            pageForPageFault.setBDPhysicalMemory(bdPyshicalMemory)
            pageForPageFault.setPhysicalMemory(True)
            program = self._loader.searchProgram(pcbInCpu.get_name())
            instructions = program.getSubInstructions(pc,pc + self._memoryManager.sizeFrame())  ##PARA CREAR LA SUBLISTA QUE VAMOS A CARGAR EN MEMORIA
            self._loader.loadInPhysicalMemory(instructions, pageForPageFault)

        self._dispatcher.load(pcbInCpu)


class InSwap(Interrupcion):
    def __init__(self, loader, scheduler, pcbTable, dispatcher):
        self._loader     = loader
        self._scheduler  = scheduler
        self._pcbTable   = pcbTable
        self._dispatcher = dispatcher


    def execute(self, pageInSwap):
        self._loader.swapIN(pageInSwap.getBDPhysicalMemory(), pageInSwap.getBDVirtualMemory())
        pageInSwap.setBDPhysicalMemory(-1)
        pageInSwap.change()