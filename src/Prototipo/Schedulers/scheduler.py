#!/usr/bin/env python
# -*- coding: utf-8 -*-s

class Scheduler:
    def isSchedulerPriority(self):
        return False

    def isChange(self, pcbInCPU, newPCB):
        return False

    def isSchedulerRoundRobin(self):
        return False

    def isSchedulerSJF(self):
        return False

    def set_burstPCBInCPU(self,burst):
        pass

    def isPreemptive(self):
        return False

    def update(self):
        pass
    def __repr__(self):
        res = "QueueReady:"
        if len(self.list()) == 0:
            return res + " -"
        for i in self.list():
            res += " " + str(i)
        return res
