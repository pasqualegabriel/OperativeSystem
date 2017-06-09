#!/usr/bin/env python
# -*- coding: utf-8 -*-s

from Prototipo.Schedulers.queues import QueuePriority
from Prototipo.Schedulers.scheduler import Scheduler

class SchedulerPriorityPreemptive(Scheduler):
    def __init__(self, pcbTable, aging):
        self._priority = {1: QueuePriority(), 2: QueuePriority(), 3: QueuePriority()}
        self._accountant = 0
        self._aging = aging
        self._PCBTable = pcbTable

    def add(self, pid, priority, burst):
        waitingTime=self._accountant + self._aging
        self._priority.get(priority).add(pid,waitingTime)

    def pop(self):
        self._accountant += 1
        self.timeOut()
        for key, valor in self._priority.items():
            if valor.notIsEmpty():
               return valor.pop()

    def isChange(self, pcbInCPU, newPCB):
        return newPCB.get_priority() < pcbInCPU.get_priority()

    def isSchedulerPriority(self):
        return True

    def isTimeOut(self, waitingTime):
        return  self._accountant >= waitingTime

    def get_aging(self):
        return self._aging

    def timeOut(self):
        for key, valor in self._priority.items():
            if valor.notIsEmpty():
                if key != 1 and self.isTimeOut(valor.get_WaitingTimeForTheHead()):
                    priority = key - 1
                    pid = valor.pop()
                    self.add(pid, priority,None)
                    pcb = self._PCBTable.lookUpPCB(pid)
                    pcb.set_priority(priority)

    def notIsEmpty(self):
        for key, valor in self._priority.items():
            if (valor.notIsEmpty()):
                return True
        return False

    def isPreemptive(self):
        return False