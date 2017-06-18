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

    def __repr__(self):
        res = "QueueReady:"
        for i in self.list():
            res += " " + str(i)
        return res
