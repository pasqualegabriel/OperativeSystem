# !/usr/bin/env python
# -*- coding: utf-8 -*-s

from SistemaDeProcedimientos.pcb import PCB


class New:
    def __init__(self, loader, dispatcher, scheduler, pcbTable):
        self._nexPid = 0
        self._loader = loader
        self._scheduler = scheduler
        self._dispatcher = dispatcher
        self._pcbTable = pcbTable

    def execute(self, program):
        if not self._loader.thereIsSpaceInMemoryFor(program.longitud()):
            return
        pcb = PCB(self._nexPid, program)
        self._loader.cargarInMemory(pcb, program)
        pcb.set_priority(program.get_priority())
        self._pcbTable.addPCB(pcb)
        self.mayorPriority(pcb)
        self._nexPid += 1

    def mayorPriority(self, pcb):
        if self._dispatcher.isIdle():
            pcb.set_status("running")
            self._scheduler.set_burstPCBInCPU(pcb.get_burst())
            self._dispatcher.load(pcb)

        elif self.isSchedulerPriorityOrIsSchedulerSJF(pcb):
            self.changeOfPCBInCPU(pcb)

        else:
            pcb.set_status("ready")
            self._scheduler.add(pcb.get_pid(), pcb.get_priority(), pcb.get_burst())

    def isSchedulerPriorityOrIsSchedulerSJF(self,pcb):
        conditionOne=self._scheduler.isSchedulerPriority() and self._scheduler.maxPriority(pcb.get_priority(), self.get_priorityPCBInCPU())
        conditionTwo=self._scheduler.isSchedulerSJF() and self._scheduler.isMinBurst(pcb.get_burst())
        return conditionOne or conditionTwo

    def get_PCBInCPU(self):
        return self._pcbTable.lookUpPCB(self._dispatcher.get_PidActual())

    def get_priorityPCBInCPU(self):
        pcbInCPU = self.get_PCBInCPU()
        return pcbInCPU.get_priority()

    def changeOfPCBInCPU(self,pcb):
        pcbEnCPU = self.get_PCBInCPU()
        self._dispatcher.save(pcbEnCPU)
        pcbEnCPU.set_status("ready")
        self._scheduler.add(pcbEnCPU.get_pid(), pcbEnCPU.get_priority(), pcbEnCPU.get_burst())
        pcb.set_status("running")
        self._scheduler.set_burstPCBInCPU(pcb.get_burst())
        self._dispatcher.load(pcb)


class Kill:
    def __init__(self, loader, dispatcher, scheduler, pcbTable, timer):
        self._loader = loader
        self._dispatcher = dispatcher
        self._pcbTable = pcbTable
        self._scheduler = scheduler
        self._timer = timer

    def execute(self, p):
        pid = self._dispatcher.get_PidActual()
        pcb = self._pcbTable.lookUpPCB(pid)
        pcb.set_status("terminated")
        self._dispatcher.pcOsioso()
        self._loader.liberarMemoria(pcb.get_bd(), pcb.get_limit(), pcb.get_pid())
        self._pcbTable.removePCB(pid)
        self.contextSwitch()
        self._timer.set_timer()

    def contextSwitch(self):
        if self._scheduler.notIsEmpty():
            pid = self._scheduler.pop()
            pcb = self._pcbTable.lookUpPCB(pid)
            pcb.set_status("running")
            if self._scheduler.isSchedulerSJF():
                    self._scheduler.set_burstPCBInCPU(pcb.get_burst())
            self._dispatcher.load(pcb)


class IoIn:
    def __init__(self, dispatcher, pcbTable, deviceManager, scheduler, timer):
        self._dispatcher = dispatcher
        self._pcbTable = pcbTable
        self._deviceManager = deviceManager
        self._scheduler = scheduler
        self._timer = timer

    def execute(self, p):
        pidEnCPU = self._dispatcher.get_PidActual()
        pcbEnCPU = self._pcbTable.lookUpPCB(pidEnCPU)
        self._dispatcher.save(pcbEnCPU)
        pcbEnCPU.set_status("waiting")
        self._deviceManager.add(pidEnCPU)
        self.contextSwitch()
        self._timer.set_timer()

    def contextSwitch(self):
        if self._scheduler.notIsEmpty():
            pid = self._scheduler.pop()
            pcb = self._pcbTable.lookUpPCB(pid)
            pcb.set_status("running")
            if self._scheduler.isSchedulerSJF():
                    self._scheduler.set_burstPCBInCPU(pcb.get_burst())
            self._dispatcher.load(pcb)



class IoOut:
    def __init__(self, dispatcher, scheduler, pcbTable):
        self._dispatcher = dispatcher
        self._pcbTable = pcbTable
        self._scheduler = scheduler

    def execute(self, pid):
        pcb = self._pcbTable.lookUpPCB(pid)
        self.mayorPriority(pcb)

    def mayorPriority(self, pcb):
        if self._dispatcher.isIdle():
            pcb.set_status("running")
            self._scheduler.set_burstPCBInCPU(pcb.get_burst())
            self._dispatcher.load(pcb)

        elif self.isSchedulerPriorityOrIsSchedulerSJF(pcb):
            self.changeOfPCBInCPU(pcb)

        else:
            pcb.set_status("ready")
            self._scheduler.add(pcb.get_pid(), pcb.get_priority(), pcb.get_burst())

    def isSchedulerPriorityOrIsSchedulerSJF(self,pcb):
        conditionOne=self._scheduler.isSchedulerPriority() and self._scheduler.maxPriority(pcb.get_priority(), self.get_priorityPCBInCPU())
        conditionTwo=self._scheduler.isSchedulerSJF() and self._scheduler.isMinBurst(pcb.get_burst())
        return conditionOne or conditionTwo

    def get_PCBInCPU(self):
        return self._pcbTable.lookUpPCB(self._dispatcher.get_PidActual())

    def get_priorityPCBInCPU(self):
        pcbInCPU = self.get_PCBInCPU()
        return pcbInCPU.get_priority()

    def changeOfPCBInCPU(self,pcb):
        pcbEnCPU = self.get_PCBInCPU()
        self._dispatcher.save(pcbEnCPU)
        pcbEnCPU.set_status("ready")
        self._scheduler.add(pcbEnCPU.get_pid(), pcbEnCPU.get_priority(), pcbEnCPU.get_burst())
        pcb.set_status("running")
        self._scheduler.set_burstPCBInCPU(pcb.get_burst())
        self._dispatcher.load(pcb)



class TimeOut:
    def __init__(self, dispatcher, scheduler, pcbTable, timer):
        self._dispatcher = dispatcher
        self._pcbTable = pcbTable
        self._scheduler = scheduler
        self._timer = timer

    def execute(self, p):
        pidEnCPU = self._dispatcher.get_PidActual()
        pcbEnCPU = self._pcbTable.lookUpPCB(pidEnCPU)
        self._dispatcher.save(pcbEnCPU)
        pcbEnCPU.set_status("ready")
        self._scheduler.add(pidEnCPU, pcbEnCPU.get_priority(), pcbEnCPU.get_burst())
        pidParaAdd = self._scheduler.pop()
        pcbParaAdd = self._pcbTable.lookUpPCB(pidParaAdd)
        pcbParaAdd.set_status("running")
        if self._scheduler.isSchedulerSJF():
            self._scheduler.set_burstPCBInCPU(pcbParaAdd.get_burst())
        self._dispatcher.load(pcbParaAdd)
        self._timer.set_timer()

class CompactMemory:
    def __init__(self, dispatcher, scheduler, pcbTable, memoryManager):
        self._dispatcher = dispatcher
        self._pcbTable = pcbTable
        self._scheduler = scheduler
        self._memoryManager = memoryManager

    def execute(self, p):
        pidEnCPU = self._dispatcher.get_PidActual()
        pcbEnCPU = self._pcbTable.lookUpPCB(pidEnCPU)
        self._dispatcher.save(pcbEnCPU)
        self._memoryManager.toCompact()
        pcb = self._pcbTable.lookUpPCB(pidEnCPU)
        self._dispatcher.load(pcb)
