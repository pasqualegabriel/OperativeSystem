# !/usr/bin/env python
# -*- coding: utf-8 -*-s

from Prototipo.pcb import PCB


class New:
    def __init__(self, loader, dispatcher, scheduler, pcbTable):
        self._nexPid = 0
        self._loader = loader
        self._scheduler = scheduler
        self._dispatcher = dispatcher
        self._pcbTable = pcbTable

    def execute(self, nameProgram):
        #program = self._loader.search_program(nameProgram)
        #pcb = PCB(self._nexPid, program)
        pcb = PCB(self._nexPid)
        self._loader.load(pcb, nameProgram)
        #pcb.set_priority(program.get_priority())
        self._pcbTable.addPCB(pcb)

        if self._dispatcher.isIdle():
            pcb.set_status("running")
            self._dispatcher.load(pcb)

        elif self.isSchedulerPriorityOrIsSchedulerSJF(pcb):
            self.changeOfPCBInCPU(pcb)

        else:
            pcb.set_status("ready")
            self._scheduler.add(pcb.get_pid(), pcb.get_priority(), pcb.get_burst())

        self._nexPid += 1

    def isSchedulerPriorityOrIsSchedulerSJF(self,pcb):
        return self._scheduler.isPreemptive() and self._scheduler.isChange(self.get_PCBInCPU(), pcb)

    def get_PCBInCPU(self):
        return self._pcbTable.lookUpPCB(self._dispatcher.get_PidActual())


    def changeOfPCBInCPU(self,pcb):
        pcbEnCPU = self.get_PCBInCPU()
        self._dispatcher.save(pcbEnCPU)
        pcbEnCPU.set_status("ready")
        self._scheduler.add(pcbEnCPU.get_pid(), pcbEnCPU.get_priority(), pcbEnCPU.get_burst())
        pcb.set_status("running")
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
        self._loader.freeMemory(pcb)
        self._pcbTable.removePCB(pid)
        self.contextSwitch()
        self._timer.set_timer()

    def contextSwitch(self):
        if self._scheduler.notIsEmpty():
            pid = self._scheduler.pop()
            pcb = self._pcbTable.lookUpPCB(pid)
            pcb.set_status("running")
            self._dispatcher.load(pcb)


class IoIn:
    def __init__(self, dispatcher, pcbTable, deviceManager, scheduler, timer):
        self._dispatcher = dispatcher
        self._pcbTable = pcbTable
        self._deviceManager = deviceManager
        self._scheduler = scheduler
        self._timer = timer

    def execute(self, idIo):
        pidEnCPU = self._dispatcher.get_PidActual()
        pcbEnCPU = self._pcbTable.lookUpPCB(pidEnCPU)
        self._dispatcher.save(pcbEnCPU)
        pcbEnCPU.set_status("waiting")
        self._deviceManager.add(pidEnCPU, idIo)
        self.contextSwitch()
        self._timer.set_timer()

    def contextSwitch(self):
        if self._scheduler.notIsEmpty():
            pid = self._scheduler.pop()
            pcb = self._pcbTable.lookUpPCB(pid)
            pcb.set_status("running")
            self._dispatcher.load(pcb)



class IoOut:
    def __init__(self, dispatcher, scheduler, pcbTable):
        self._dispatcher = dispatcher
        self._pcbTable = pcbTable
        self._scheduler = scheduler

    def execute(self, pid):
        pcb = self._pcbTable.lookUpPCB(pid)

        if self._dispatcher.isIdle():
            pcb.set_status("running")

            self._dispatcher.load(pcb)

        elif self.isSchedulerPriorityOrIsSchedulerSJF(pcb):
            self.changeOfPCBInCPU(pcb)

        else:
            pcb.set_status("ready")
            self._scheduler.add(pcb.get_pid(), pcb.get_priority(), pcb.get_burst())

    def isSchedulerPriorityOrIsSchedulerSJF(self,pcb):
        return self._scheduler.isPreemptive() and self._scheduler.isChange(self.get_PCBInCPU(), pcb)

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
        self._dispatcher.load(pcbParaAdd)
        self._timer.set_timer()

class CompactMemory:
    def __init__(self, dispatcher, pcbTable, memoryManager):
        self._dispatcher = dispatcher
        self._pcbTable = pcbTable
        self._memoryManager = memoryManager

    def execute(self, p):
        pidEnCPU = self._dispatcher.get_PidActual()
        pcbEnCPU = self._pcbTable.lookUpPCB(pidEnCPU)
        self._dispatcher.save(pcbEnCPU)
        self._memoryManager.toCompact()
        pcb = self._pcbTable.lookUpPCB(pidEnCPU)
        self._dispatcher.load(pcb)
