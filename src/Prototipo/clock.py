#!/usr/bin/env python
# -*- coding: utf-8 -*-s

class Clock:
    def __init__(self, cpu, deviceManager, timer, newProgram):
        self._cpu = cpu
        self._deviceManager = deviceManager
        self._timer = timer
        self._newProgram = newProgram
        self._estate = True

    def runCpu(self, log):
        count = 0
        while self._estate:

            self._newProgram.tick(count, log)
            self._cpu.tick(log)
            self._deviceManager.tick()
            if not self._timer is None:
                self._timer.tick()

            count += 1
            if count > 100:
                self.offClock()

    def offClock(self):
        self._estate = False