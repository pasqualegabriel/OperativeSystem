#!/usr/bin/env python
# -*- coding: utf-8 -*-s

from SistemaDeScheduler.queues import *


class Scheduler:
    def isSchedulerPriority(self):
        return False

    def maxPriority(self, priority, priorityDelPCBEnCPU):
        return False

    def isSchedulerRoundRobin(self):
        return False

    def isSchedulerSJF(self):
        return False

    def set_burstPCBInCPU(self,burst):
        pass





class SchedulerFIFO(Scheduler):
    def __init__(self):
        self._ready = QueueFIFO()


    def add(self, pid, priority, burst):
        self._ready.add(pid)


    def pop(self):
        return self._ready.pop()


    def lenReady(self):
        return self._ready.lenItems()

    def notIsEmpty(self):
        return self._ready.notIsEmpty()


class SchedulerPriorityPreventive(Scheduler):
    def __init__(self, pcbTable):
        self._priority = {1: QueuePriority(), 2: QueuePriority(), 3: QueuePriority()}
        self._accountant = 0
        self._time=2
        self._PCBTable = pcbTable


    def add(self, pid, priority, burst):
        waitingTime=self._accountant + self._time
        self._priority.get(priority).add(pid,waitingTime)
        self._accountant += 1


    def pop(self):
        self._accountant += 1
        self.timeOut()
        for key, valor in self._priority.items():
            if valor.notIsEmpty():
               return valor.pop()

    def maxPriority(self, priority, priorityDelPCBEnCPU):
        if priority <= priorityDelPCBEnCPU:
            return True
        else:
            return False

    def isSchedulerPriority(self):
        return True

    def isTimeOut(self, waitingTime):
        return  self._accountant >= waitingTime

    def insert(self, priority, index, tuple):
        cola = self._priority.get(priority)
        cola.insert(index, tuple)


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

class SchedulerRoundRobin(Scheduler):
    def __init__(self):
        self._ready = QueueFIFO()



    def add(self, pid, priority, burst):
        self._ready.add(pid)


    def pop(self):
        return self._ready.pop()


    def lenReady(self):
        return self._ready.lenItems()

    def list(self):
        return self._ready.list()

    def notIsEmpty(self):
        return self._ready.notIsEmpty()

    def isSchedulerRoundRobin(self):
        return True


class SchedulerSJF(Scheduler):
    def __init__(self):
        self._ready = QueueSJF()
        self._burstInCPU = None


    def add(self, pid, priority, burst):
        self._ready.add(pid,burst)

    def pop(self):
        return self._ready.pop()

    def lenReady(self):
        return self._ready.lenItems()

    def notIsEmpty(self):
        return self._ready.notIsEmpty()

    def isSchedulerSJF(self):
        return True

    def isMinBurst(self,IncomingBurst):
        if  IncomingBurst < self._burstInCPU:
            return True
        else:
            return False

    def set_burstPCBInCPU(self,burstInCPU):
        self._burstInCPU=burstInCPU


