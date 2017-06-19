#!/usr/bin/env python
# -*- coding: utf-8 -*-s

from Prototipo.Schedulers.queues import *
from Prototipo.Schedulers.scheduler import Scheduler

class SchedulerPriorityPreemptive(Scheduler):
    # Se inicializa con un map donde las claves son las prioridades, y los valores es una queue,
    # el pcbTable, el aging y el contador
    # Aclaracion: La prioridad 1 es mejor que la 2
    def __init__(self, pcbTable, aging):
        self._priority = {1: QueueFIFO(), 2: QueueFIFO(), 3: QueueFIFO(), 4: QueueFIFO(), 5: QueueFIFO()}
        self._accountant = 0
        self._PCBTable = pcbTable
        self._aging = aging

    # Proposito: Se encola en la queue de la prioridad del <pcb>, una tupla con el pid y el tiempo de mejora de prioridad
    def add(self, pcb):
        tupleWithPidAndWaitingTime = (pcb.get_pid(), self._accountant + self._aging)
        self._priority.get(pcb.get_priority()).add(tupleWithPidAndWaitingTime)

    # Proposito: Aumenta el contador en uno, actualiza las prioridades y retorna el pid con mejor prioridad a desencolar
    # Precondicion: Al menos una queue no debe ser vacia
    def pop(self):
        self._accountant += 1
        self.updatePriorities()
        for priority, queue in self._priority.items():
            if queue.notIsEmpty():
               return queue.pop()[0]

    # Proposito: Retorna True si la prioridad de <pcbInCPU> es menor a la prioridad de <newPCB>
    def isChange(self, pcbInCPU, newPCB):
        return newPCB.get_priority() < pcbInCPU.get_priority()

    # Proposito: Recorre las queue, si el pid de la cabeza de las queues debe mejorar la prioridad,
    #  se actualiza la prioridad en el pcb y se cambia a la queue de su nueva prioridad
    def updatePriorities(self):
        for priority, queue in self._priority.items():
            if queue.notIsEmpty() and (priority != 1 and self._accountant >= queue.head()[1]):
                newPriority = priority - 1
                pid = queue.pop()[0]
                pcb = self._PCBTable.lookUpPCB(pid)
                self.add(pcb)
                pcb.set_priority(newPriority)

    # Proposito: Retorna True si hay al menos una queue que no este vacia
    #  y False en caso contrario
    def notIsEmpty(self):
        for key, valor in self._priority.items():
            if valor.notIsEmpty():
                return True
        return False

    # Proposito: Retorna una lista con todos los pids de las queue
    # Aclaracion: Este metodo se utiliza para la impresion
    def list(self):
        res = []
        for priority, queue in self._priority.items():
            for q in queue.list():
                res.append(q[0])
        return res

    # Proposito: Retorna True
    def isPreemptive(self):
        return True



class SchedulerPriorityNonPreemptive(SchedulerPriorityPreemptive):
    # Proposito: Retorna False
    def isPreemptive(self):
        return False

