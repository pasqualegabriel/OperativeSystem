#!/usr/bin/env python
# -*- coding: utf-8 -*-s
from prototipo.memory import Memory
from prototipo.intManager import IntManager
from prototipo.mmu import Mmu
from prototipo.cpu import Cpu
from prototipo.clock import Clock

# Representa al Kernel
# Colaboradores internos memory, mmu, cpu y intManager
# El Kernel es el encargado de ejecutar los programas
class Kernel:
    def __init__(self):
        self._memory=Memory()
        self._mmu = Mmu(self._memory)
        self._cpu=Cpu(self._mmu) 
        self._intmanager=IntManager(self._cpu,self._memory, self._mmu)
        self._clock=Clock(self._cpu)
        
        
    #Proposito:Crea los procedimiento, y luego llama al metodo exec
    #Precondiccion:-
    def execPrograms(self, ps, log):
        for p in ps:
            self._intmanager.new(p)
            print()#separa la impresion de los programas
            print(p.name)
            log.debug(self)
        self._cpu.set_intManager(self._intmanager)
        self.exec(log) 
              
    
    #Proposito:Pone a correr el clock.
    #Precondiccion:-
    def exec(self,log):
        self._clock.runCpu(log)
    
    #Proposito:imprimir en pantalla.
    #Precondiccion:-
    def __repr__(self):
        return "{cpu}\n{mem}".format(cpu=self._cpu, mem=self._memory) 