#!/usr/bin/env python
# -*- coding: utf-8 -*-s

from Prototipo.Schedulers.queues import QueueSJF
from Prototipo.Schedulers.scheduler import Scheduler

class SchedulerSJFNonPreemptive(Scheduler):
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

    def isMinBurst(self,IncomingBurst):
        return IncomingBurst < self._burstInCPU

    def set_burstPCBInCPU(self,burstInCPU):
        self._burstInCPU=burstInCPU