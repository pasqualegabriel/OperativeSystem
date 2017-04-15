#!/usr/bin/env python
# -*- coding: utf-8 -*-s
from prototipo.cpu import Cpu

# Representa al Clock del sistema
# Colaboradores internos 
# 
class Clock:
    def __init__(self,cpu):
        self._cpu=cpu
    
    def runCpu(self,log):
        while(True):
            self._cpu.tick(log)
            