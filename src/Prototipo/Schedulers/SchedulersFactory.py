#!/usr/bin/env python
# -*- coding: utf-8 -*-s
from Prototipo.Schedulers.SchedulerFCFS import SchedulerFCFS
from Prototipo.Schedulers.SchedulerPriorityNonPreemptive import SchedulerPriorityNonPreemptive
from Prototipo.Schedulers.SchedulerPriorityPreemptive import SchedulerPriorityPreemptive
from Prototipo.Schedulers.SchedulerRoundRobin import SchedulerRoundRobin
from Prototipo.Schedulers.SchedulerSJFNonPreemptive import SchedulerSJFNonPreemptive
from Prototipo.Schedulers.SchedulerSJFPreemptive import SchedulerSJFPreemptive


class SchedulersFactory:
    def __init__(self):
        self._id = int(input("Elegir Scheduler:\n1 SchedulerFCFS\n2 SchedulerPriorityPreemptive\n3 SchedulerPriorityNonPreemptive\n4 SchedulerRoundRobin\n5 SchedulerSJFPreemptive\n6 SchedulerSJFNonPreemptive\n".format()))
        self._quantum = 3

    def getScheduler(self, pcbTable):
        if self._id == 1:
            self._scheduler = SchedulerFCFS()
        elif self._id == 2:
            aging = input("Aging?\n")
            self._scheduler = SchedulerPriorityPreemptive(pcbTable, int(aging))
        elif self._id == 3:
            aging = input("Aging?\n")
            self._scheduler = SchedulerPriorityNonPreemptive(pcbTable, int(aging))
        elif self._id == 4:
            self._quantum = input("Quantum?\n")
            self._scheduler = SchedulerRoundRobin()
        elif self._id == 5:
            self._scheduler = SchedulerSJFPreemptive()
        elif self._id == 6:
            self._scheduler = SchedulerSJFNonPreemptive()
        return self._scheduler

    def getQuantum(self):
        return int(self._quantum)
