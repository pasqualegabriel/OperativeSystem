#!/usr/bin/env python
# -*- coding: utf-8 -*-s

class Timer:
    def __init__(self, scheduler, intManager, quantum):
        self._scheduler = scheduler
        self._timer = 1
        self._quantum = quantum
        self._intManager = intManager

    def tick(self):
        if not self._scheduler.isSchedulerRoundRobin():
            return
        if self.fullTimer() and self._scheduler.notIsEmpty():
            self._intManager.handle("TIME_OUT", None)
        self._timer += 1

    def fullTimer(self):
        return self._timer == self._quantum

    def set_timer(self):
        self._timer = 0




