#!/usr/bin/env python
# -*- coding: utf-8 -*-s
from Prototipo.Schedulers.SchedulerFCFS import SchedulerFCFS
from Prototipo.Schedulers.SchedulerPriority import SchedulerPriorityPreemptive, SchedulerPriorityNonPreemptive
from Prototipo.Schedulers.SchedulerRoundRobin import SchedulerRoundRobin
from Prototipo.Schedulers.SchedulerSJF import SchedulerSJFPreemptive, SchedulerSJFNonPreemptive
from Prototipo.timer import Timer


class SchedulersFactory:
    def __init__(self,pcbTable):
        self._id = int(input("Choise Scheduler:\n1 First Come First Served\n2 Priority Preemptive\n3 Priority Non Preemptive\n4 Round Robin\n5 Shortest Job First Preemptive\n6 Shortest Job First Non Preemptive\n".format()))
        self._quantum = 3
        self._aging = None

        if self._id == 2 or self._id == 3:
            self._aging = int(input("Aging?\n"))

        self._schedulers={1:SchedulerFCFS(),
                          2:SchedulerPriorityPreemptive(pcbTable, self._aging),
                          3:SchedulerPriorityNonPreemptive(pcbTable, self._aging),
                          4:SchedulerRoundRobin(),
                          5:SchedulerSJFPreemptive(),
                          6:SchedulerSJFNonPreemptive()}

    def getScheduler(self):
        scheduler = self._schedulers.get(self._id)

        if self._id == 4:

            self._quantum = input("Quantum?\n")

        return scheduler


    def getTimer(self, intManager):
        if self._id == 4:
            return Timer(intManager, int(self._quantum))
        return None

