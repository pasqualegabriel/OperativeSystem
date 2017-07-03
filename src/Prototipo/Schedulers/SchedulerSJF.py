#!/usr/bin/env python
# -*- coding: utf-8 -*-s

from Prototipo.Schedulers.queues import QueueSJF
from Prototipo.Schedulers.scheduler import Scheduler


class SchedulerSJFPreemptive(Scheduler):
    def __init__(self):
        self._ready      = QueueSJF()
        self._burstInCPU = None

    # Proposito: Agrega un pid y su burst a la Queue
    def add(self, pcb):
        pid = pcb.get_pid()
        burst = pcb.get_burst()
        self._ready.add(pid, burst)

    # Proposito: Retorna el primer pid de la Queue.
    # Precondicion: Debe haber al menos un elemnto
    def pop(self):
        return self._ready.pop()

    # Proposito: Retorna la cantidad de elementos que tiene la queue.
    def lenReady(self):
        return self._ready.lenItems()

    # Proposito: Retorna true si la queue no esta vacia.
    def notIsEmpty(self):
        return self._ready.notIsEmpty()

    # Proposito: Retorna true si el burst que esta entrando es menor al que esta en el cpu.
    def isChange(self, pcbInCPU, newPCB):
        return newPCB.get_burst() < pcbInCPU.get_burst()

    # Proposito: Setea el campo del bust acual en el cpu
    def set_burstPCBInCPU(self, burstInCPU):
        self._burstInCPU = burstInCPU

    # Proposito: Retorna una lista con todos los pids de la queue
    def list(self):
        return self._ready.list()

    # Proposito: Retorna true si es preemptive
    def isPreemptive(self):
        return True


class SchedulerSJFNonPreemptive(SchedulerSJFPreemptive):
    # Proposito: Retorna true si es preemptive
    def isPreemptive(self):
        return False
