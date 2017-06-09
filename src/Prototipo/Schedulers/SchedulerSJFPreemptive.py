#!/usr/bin/env python
# -*- coding: utf-8 -*-s

from Prototipo.Schedulers.queues import QueueSJF
from Prototipo.Schedulers.scheduler import Scheduler


class SchedulerSJFPreemptive(Scheduler):
    def __init__(self):
        self._ready = QueueSJF()
        self._burstInCPU = None

    # Proposito:Agrega un pid y su burst a la Queue
    # Precondicion:-
    def add(self, pid, priority, burst):
        self._ready.add(pid, burst)

    # Proposito:retorna el primer pid de la Queue.
    # Precondicion:Debe haber al menos un elemnto
    def pop(self):
        return self._ready.pop()

    # Proposito:Denota la cantidad de elementos que tiene la queue.
    # Precondicion:-
    def lenReady(self):
        return self._ready.lenItems()

    # Proposito:Denota true si la queue esta vacia.
    # Precondicion:-
    def notIsEmpty(self):
        return self._ready.notIsEmpty()

    # Proposito:verificador de scjedulerSJF
    # Precondicion:
    def isSchedulerSJF(self):
        return True

    # Proposito:denota true si el burst que esta entrando es menor al que esta en el cpu.
    # Precondicion:-
    def isChange(self, pcbINCPU, newPCB):
        return newPCB.get_burst() < pcbINCPU.get_burst()

    # Proposito:setea el campo del bust acual en el cpu
    # Precondicion:-
    def set_burstPCBInCPU(self, burstInCPU):
        self._burstInCPU = burstInCPU

    def isPreemptive(self):
        return True