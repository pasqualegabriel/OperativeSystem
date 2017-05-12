#!/usr/bin/env python
# -*- coding: utf-8 -*-s

from SistemaDeScheduler.queues import *


class DeviceManager:
    def __init__(self, intManager, Scheduler):
        self._queue = QueueFIFO()
        self._intManager = intManager
        self._Scheduler = Scheduler

    def add(self, pid):
        self._queue.add(pid)

    def pop(self):
        return self._queue.pop()

    def tickDM(self):
        self._decode()

    def notIsEmpty(self):
        return self._queue.notIsEmpty()

    def lenQueueDM(self):
        return self._queue.lenItems()

    def _decode(self):
        if self.notIsEmpty():
            pid = self._queue.pop()
            self._intManager.handle("IO_OUT", pid)
