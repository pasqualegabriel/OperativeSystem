#!/usr/bin/env python
# -*- coding: utf-8 -*-s

from Prototipo.Schedulers.queues import *
from Prototipo.intManager import Irq


class DeviceManager:
    def __init__(self, intManager):
        self._waiting = {1: QueueFIFO(), 2: QueueFIFO(), 3: QueueFIFO()}
        self._counter = 0
        self._intManager = intManager

    def add(self, pid, idIo):
         self._waiting.get(idIo).add((pid, (self._counter + idIo)))

    def update(self):
        for ioId, queue in self._waiting.items():
            for i in queue.list():
                if i[1] <= self._counter:
                    pid = i[0]
                    queue.remove(i)
                    self._intManager.handle(Irq.IO_OUT, pid)

    def tick(self):
        self.update()
        self._counter += 1



    def lenQueueWaiting(self):
        res = 0
        for ioId, queue in self._waiting.items():
            res += queue.lenItems()
        return res

