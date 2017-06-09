#!/usr/bin/env python
# -*- coding: utf-8 -*-s

from Prototipo.Schedulers.queues import QueuePriority
from Prototipo.Schedulers.scheduler import Scheduler

class SchedulerPriorityNonPreemptive(Scheduler):
    def __init__(self, pcbTable, aging):
        self._priority = {1: QueuePriority(), 2: QueuePriority(), 3: QueuePriority()}
        self._accountant = 0
        self._time = aging
        self._PCBTable = pcbTable

    def add(self, pid, priority, burst):
        waitingTime = self._accountant + self._time
        self._priority.get(priority).add(pid, waitingTime)

    def pop(self):
        self._accountant += 1
        self.timeOut()
        for key, valor in self._priority.items():
            if valor.notIsEmpty():
               return valor.pop()

    def isTimeOut(self, waitingTime):
        return self._accountant >= waitingTime

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