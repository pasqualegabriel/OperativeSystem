#!/usr/bin/env python
# -*- coding: utf-8 -*-s

from Prototipo.Schedulers.queues import QueueFIFO
from Prototipo.Schedulers.scheduler import Scheduler

class SchedulerFCFS(Scheduler):
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