#!/usr/bin/env python
# -*- coding: utf-8 -*-s

class Timer:
    def __init__(self, scheduler,cpu):
        self._scheduler=scheduler
        self._timer = 0
        self._cpu=cpu 

    def fullTimer(self):
        return self._timer > 3
        
    def set_timer(self):
        self._timer = 0
        
    def sumar_timer(self):
        intruccion=self._cpu.get_ir()
        if(self._scheduler.isSchedulerRoundRobin() and intruccion.isCPU()):
            self._timer += 1