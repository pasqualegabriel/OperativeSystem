#!/usr/bin/env python
# -*- coding: utf-8 -*-s
from SistemaDeProgramas.program import Program  # Para imprimir
from SistemaDeProgramas.instructions import *  # Para imprimir

class Clock:
    def __init__(self, cpu, deviceManager, timer):
        self._cpu = cpu
        self._deviceManager = deviceManager
        self._timer = timer

        self.kernel = None # Para imprimir

    def set_kernel(self, kernel):  # Para imprimir
        self.kernel = kernel  # Para imprimir

    def runCpu(self, log):
        cortar = 0
        while True:
            if cortar == 7: # Para hacer un new (agregar un nuevo programa) en el medio de una ejecucion
                p = Program("paint.exe", [CPU(1)], 2) # El programa
                self.kernel.new(p, log) # Para imprimir
                p = Program("vlc.exe", [CPU(5)], 2) # El programa
                self.kernel.new(p, log) # Para imprimir

            if cortar < 100:
                self._cpu.tick(log)
                self._deviceManager.tickDM()
                self._timer.tick()
                cortar += 1

            else:
                break
