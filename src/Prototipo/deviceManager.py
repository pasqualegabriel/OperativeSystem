#!/usr/bin/env python
# -*- coding: utf-8 -*-s

from Prototipo.Schedulers.queues import *
from Prototipo.intManager import Irq

# Utiliza un map donde las claves son los tipos de IO, y los valores una queue
# cada queue guarda una tupla con el pid y el tiempo para pasar a ready
class DeviceManager:
    def __init__(self, intManager):
        self._waiting    = {1: QueueFIFO(), 2: QueueFIFO(), 3: QueueFIFO()}
        self._counter    = 0
        self._intManager = intManager

    #Proposito: Agrega en la cola del idIo el pid y el tiempo para pasar a ready
    def add(self, pid, idIo):
        pidAndTimeIO = (pid, (self._counter + idIo))
        self._waiting.get(idIo).add(pidAndTimeIO)

    # Proposito: Recorre todas las queues y si algun pid ya cumplio con el tiempo de espera
    #  se ejecuta la interrupcion IO_OUT.
    def update(self):
        for ioId, queue in self._waiting.items():
            for i in queue.list():
                if i[1] <= self._counter:
                    pid = i[0]
                    queue.remove(i)
                    self._intManager.handle(Irq.IO_OUT, pid)

    # Proposito: Actualiza las queues y le suma 1 al contador
    def tick(self):
        self.update()
        self._counter += 1

    # Proposito: Retorna el map waiting.
    def getWaiting(self):
        return self._waiting


