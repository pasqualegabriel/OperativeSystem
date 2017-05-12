#!/usr/bin/env python
# -*- coding: utf-8 -*-s

class Dispatcher:
    def __init__(self, mmu, cpu,timer):
        self._mmu = mmu
        self._cpu = cpu
        self._timer=timer
        self._current = 0


    # Proposito: retorna verdadero si el cpu esta en estado inactivo
    # Precondiccion:-
    def isIdle(self):
        return self._cpu.get_pc() == -1

    # Proposito: Setea el pc del pcb
    # Precondiccion:-
    def save(self, pcb):
        pcb.set_pc(self._cpu.get_pc())
        self._current = -1
        self._cpu.set_pc(-1)

        # Proposito: guarda el pid actual, setea el cpu en 0 su pc, setea el bd y limit en el mmu

    # Precondiccion:que se le mande por parametro el objeto pcb.
    def load(self, pcb):
        self._current = pcb.get_pid()
        self._cpu.set_pc(pcb.get_pc())
        self._mmu.set_bd(pcb.get_bd())
        self._mmu.set_limit(pcb.get_limit())
        self._timer.set_timer()

    # Proposito: retorna el pid
    # Precondiccion: -
    def get_PidActual(self):
        return self._current

    # Proposito: setea el pc en osiosio
    # Precondiccion:-
    def pcOsioso(self):
        self._cpu.set_pc(-1)
        self._current = -1

    # Proposito: setea el pid 
    # Precondiccion:-
    def set_pid(self,pid):
        self._current=pid


