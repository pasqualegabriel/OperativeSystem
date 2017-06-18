#!/usr/bin/env python
# -*- coding: utf-8 -*-s

from Prototipo.Schedulers.SchedulerFCFS import SchedulerFCFS

class SchedulerRoundRobin(SchedulerFCFS):
    def isSchedulerRoundRobin(self):
        return True
