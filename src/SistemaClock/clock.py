#!/usr/bin/env python
# -*- coding: utf-8 -*-s




class Clock:
    def __init__(self, cpu, deviceManager,timer,intManager):
        self._cpu = cpu
        self._deviceManager = deviceManager
        self._timer=timer
        self._intManager=intManager

    def runCpu(self, log):
        cortar=0
        while True:
            if cortar<50 and not self._timer.fullTimer():
                self._cpu.tick(log)
                self._deviceManager.tickDM()
                self._timer.sumar_timer()
                cortar+=1
                
            elif self._timer.fullTimer():
                self._intManager.handle("TIME_OUT", None)
              

            else:
                break
