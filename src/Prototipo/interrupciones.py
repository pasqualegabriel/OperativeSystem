# !/usr/bin/env python
# -*- coding: utf-8 -*-s

from Prototipo.pcb import PCB

class interruption:
    #Proposito:Retorna el pcb que esta actualmente corriendo en el cpu.
    #Precondicion:Debe de haber un pcb cargado.
    def getPCBInCPU(self):
        return self._pcbTable.lookUpPCB(self._dispatcher.getPidInCpu())

    #Propositon:Retorna el pcb q pertenece al <pid>
    #Precondicion:Debe existir dicho pcb.
    def getPCB(self,pid):
        return self._pcbTable.lookUpPCB(pid)

    def getPIDInCPU(self):
        return self._dispatcher.getPidInCpu()

    # Proposito:actualiza el PRograma conter del pcb en cpu, verifica si es preventivo
    # y si hay q cabiar de prosedimiento.
    # Precondicion:-
    def isPreemptiveAndIsChange(self, pcb):
        self._dispatcher.save(self.getPCBInCPU())
        return self._scheduler.isPreemptive() and self._scheduler.isChange(self.getPCBInCPU(), pcb)

    # Proposito:Saca el pcb que esta en cpu corriendo el cpu lo actualiza, lo guarda, y carga otro pcb.
    # Precondicion:-
    def changeOfPCBInCPU(self, pcb):
        pcbEnCPU = self.getPCBInCPU()
        #self._dispatcher.save(pcbEnCPU)
        pcbEnCPU.set_status("ready")
        self._scheduler.add(pcbEnCPU)
        pcb.set_status("running")
        self._dispatcher.load(pcb)

    # Proposito:Carga un procedimiento o cambia el procedimiento actual por otro; o encola pid del pcb.
    def isLoadOrChangeOrToReady(self, pcb):

        if self._dispatcher.isIdle():
            pcb.set_status("running")
            self._dispatcher.load(pcb)

        elif self.isPreemptiveAndIsChange(pcb):
            self.changeOfPCBInCPU(pcb)
        else:
            pcb.set_status("ready")
            self._scheduler.add(pcb)

    #Proposito:Verifica si hay pid por encolar, en caso que haya pide uno y busca el pcb y setea estado a running y lo carga.
    #Precondcion:-
    def contextSwitch(self):
        if self._scheduler.notIsEmpty():
            pid = self._scheduler.pop()
            pcb = self._pcbTable.lookUpPCB(pid)
            pcb.set_status("running")
            self._dispatcher.load(pcb)


class New(interruption):
    def __init__(self, loader, dispatcher, scheduler, pcbTable):
        self._nexPid     = 0
        self._loader     = loader
        self._scheduler  = scheduler
        self._dispatcher = dispatcher
        self._pcbTable   = pcbTable

    #Proposioto:Crear un proceso y ve si tiene q cargarlo en el cpu o encolarlo.
    #Precondicion:-
    def execute(self, nameProgram):
        pcb = PCB(self._nexPid)
        self._loader.load(pcb, nameProgram)
        self._pcbTable.addPCB(pcb)
        self._nexPid += 1
        self.isLoadOrChangeOrToReady(pcb)


class Kill(interruption):
    def __init__(self, loader, dispatcher, scheduler, pcbTable, timer, memoryManager):
        self._loader        = loader
        self._dispatcher    = dispatcher
        self._pcbTable      = pcbTable
        self._scheduler     = scheduler
        self._timer         = timer
        self._memoryManager = memoryManager

    #Proposito:libera todos los marcos o blockes(segun el mm) usados por el proceso actual en el pcu,y despues lo borra pcbtablet,
    #carga otro procedimiento de la cola de ready si lo hay.
    #Precondicion:-
    def execute(self, p):
        pid = self._dispatcher.getPidInCpu()
        self._memoryManager.freeMemory(pid)
        self._pcbTable.removePCB(pid)
        self._dispatcher.idlePc()
        self.contextSwitch()
        if not self._timer is None:
            self._timer.resetTimer()


class IoIn(interruption):
    def __init__(self, dispatcher, pcbTable, deviceManager, scheduler, timer):
        self._dispatcher    = dispatcher
        self._pcbTable      = pcbTable
        self._deviceManager = deviceManager
        self._scheduler     = scheduler
        self._timer         = timer


    #Proposito:Manda el proceso actual al a la cola del deviceManager,
    #carga otro procedimiento de la cola de ready si lo hay.
    #Precondicion:
    def execute(self, io):
        pcbEnCPU = self.getPCBInCPU()
        self._dispatcher.save(pcbEnCPU)
        pcbEnCPU.set_status("waiting")
        self._deviceManager.add(self.getPIDInCPU(), io.getId())
        self._dispatcher.idlePc()
        self.contextSwitch()
        if not self._timer is None:
            self._timer.resetTimer()

class IoOut(interruption):
    def __init__(self, dispatcher, scheduler, pcbTable):
        self._dispatcher = dispatcher
        self._pcbTable   = pcbTable
        self._scheduler  = scheduler

    #Proposito:El proceso Que acaba de salir de la cola de deviceManager, lo pone en running o en ready.
    def execute(self, pid):
        pcb = self._pcbTable.lookUpPCB(pid)
        self.isLoadOrChangeOrToReady(pcb)


class TimeOut(interruption):
    def __init__(self, dispatcher, scheduler, pcbTable):
        self._dispatcher = dispatcher
        self._pcbTable = pcbTable
        self._scheduler = scheduler

    #Proposito:Saca un proceso de la cpu y cambia por otro si es que lo hay
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


class CompactMemory(interruption):
    def __init__(self, dispatcher, pcbTable, memoryManager):
        self._dispatcher    = dispatcher
        self._pcbTable      = pcbTable
        self._memoryManager = memoryManager

    #Proposito:Frena el cpu, guarda el ultimo program contact en el respectivo Proceso, compacta la memoria, y vuelve a cargar ese proceso
    def execute(self, p):
        pcbInCpu = self.getPCBInCPU()
        self._dispatcher.save(pcbInCpu)
        self._dispatcher.idlePc()
        self._memoryManager.toCompact()
        self._dispatcher.load(pcbInCpu)



class PageFault(interruption):
    def __init__(self, loader, scheduler, pcbTable, dispatcher,memoryManager):
        self._loader        = loader
        self._scheduler     = scheduler
        self._pcbTable      = pcbTable
        self._dispatcher    = dispatcher
        self._memoryManager = memoryManager

    #Proposito:actualiza el mmu y carga una pagina que le assigno el mm a la memoria.
    def execute(self, pageForPageFault):
        pcbInCpu = self.getPCBInCPU()
        self._dispatcher.save(pcbInCpu)
        self._dispatcher.idlePc()
        pc = pcbInCpu.get_pc()
        pageNumber = pc // self._memoryManager.sizeFrame()

        if pageForPageFault.inSwap():
            bdVirtualMemory = pageForPageFault.getBDVirtualMemory()
            instructions = self._loader.swapOut(bdVirtualMemory)
            bdPyshicalMemory = self._memoryManager.assignFrame(pcbInCpu.get_pid(), pageNumber)
            pageForPageFault.setBDPhysicalMemory(bdPyshicalMemory)
            pageForPageFault.change()
            self._loader.loadInPhysicalMemory(instructions, pageForPageFault)

        else:
            bdPyshicalMemory = self._memoryManager.assignFrame(pcbInCpu.get_pid(), pageNumber)
            pageForPageFault.setBDPhysicalMemory(bdPyshicalMemory)
            pageForPageFault.setPhysicalMemory(True)
            program = self._loader.searchProgram(pcbInCpu.get_name())
            instructions = program.getSubInstructions(pc, pc + self._memoryManager.sizeFrame())
            self._loader.loadInPhysicalMemory(instructions, pageForPageFault)

        self._dispatcher.load(pcbInCpu)

