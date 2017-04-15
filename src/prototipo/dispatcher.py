#!/usr/bin/env python
# -*- coding: utf-8 -*-s
from prototipo.cpu import Cpu
from prototipo.mmu import Mmu
# Representa al Dispatcher del sistema
# Colaboradores internos cpu, mmu y pid
# El Dispatcher se encarga de almacenar el pid actual, cargar en el cpu el estado de los procesos
#  y se encarga de interactuar con el MMU
class Dispatcher:
    def __init__(self,mmu,cpu):
        self._mmu= mmu
        self._cpu =cpu
        self._pid=0
        #self._pcDeProgramaEnWaiting=0
    
    #Proposito: retorna verdadero si el cpu esta en estado inactivo
    #Precondiccion:-
    def isIdle(self):
        return self._cpu.get_pc() == -1
    
    #Proposito:-
    #Precondiccion:-    
    def save(self):
        pass 
    
    #Proposito: guarda el pid actual, setea el cpu en 0 su pc, setea el bd y limit en el mmu
    #Precondiccion:que se le mande por parametro el objeto pcb.    
    def load(self, pcb):
        self._pid=pcb.get_pid()
        self._cpu.set_pc(0)  
        self._mmu.set_bd(pcb.get_bd)
        self._mmu.set_limit(pcb.get_limit)
    
    #Proposito: retorna el pid
    #Precondiccion: -
    def get_PidActual(self):
        return self._pid
    
    #Proposito: setea el pc en osiosio
    #Precondiccion:-
    def pcOsioso(self):
        self._cpu.set_pc(-1)