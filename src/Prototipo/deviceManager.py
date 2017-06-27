#!/usr/bin/env python
# -*- coding: utf-8 -*-s

from Prototipo.Schedulers.queues import *
from Prototipo.intManager import Irq

# Utiliza un map donde las claves son los tipos de IO, y los valores una queue
# cada queue guarda una tupla con el pid y el tiempo para pasar a ready
class DeviceManager:
    def __init__(self, intManager):
        self._waiting       = {1: QueueFIFO(), 2: QueueFIFO(), 3: QueueFIFO()}
        self._counter       = 0
        self._intManager    = intManager

    #Proposito: Agrega en la cola del idIo el pid y el tiempo para pasar a ready
    #Precondicion: -
    def add(self, pid, idIo):
        pidAndTimeIO = (pid, (self._counter + idIo))
        self._waiting.get(idIo).add(pidAndTimeIO)

    # Proposito:recorre todas las queues y si algun pid ya cumplio con el tiempo de espera
    #           se ejecuta la interrupcion IO_OUT.
    # Precondicion: -
    def update(self):
        for ioId, queue in self._waiting.items():
            for i in queue.list():
                if i[1] <= self._counter:
                    pid = i[0]
                    queue.remove(i)
                    self._intManager.handle(Irq.IO_OUT, pid)

    # Proposito:recorre todas las queues y si algun pid ya cumplio con el tiempo de espera
    #           se ejecuta la interrupcion IO_OUT y aumenta uno el contador
    # Precondicion: -
    def tick(self):
        self.update()
        self._counter += 1

    # Proposito:Retorna el diccionario waiting.
    # Precondicion: -
    def getWaiting(self):
        return self._waiting


