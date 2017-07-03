#!/usr/bin/env python
# -*- coding: utf-8 -*-s

from Prototipo.Schedulers.queues import QueueFIFO
from Prototipo.Schedulers.scheduler import Scheduler

# Se inicializa con una queue fifo
class SchedulerFCFS(Scheduler):
    def __init__(self):
        self._ready = QueueFIFO()

    # Proposito: Encola el pid del <pcb>
    def add(self, pcb):
        pid = pcb.get_pid()
        self._ready.add(pid)

    # Proposito: Desencola el primer pid y lo retorna
    # Precondicion: La queue no debe ser vacia
    def pop(self):
        return self._ready.pop()

    # Proposito: Retorna la longitud de la queue
    def lenReady(self):
        return self._ready.lenItems()

    # Proposito: Retorna True si la queue no esta vacia, False caso contrario
    def notIsEmpty(self):
        return self._ready.notIsEmpty()

    # Proposito: Retorna una lista con todos los pids de la queue
    def list(self):
        return self._ready.list()