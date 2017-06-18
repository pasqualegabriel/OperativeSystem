#!/usr/bin/env python
# -*- coding: utf-8 -*-s

class Dispatcher:
    def __init__(self, mmu, cpu, timer):
        self._mmu = mmu
        self._cpu = cpu
        self._timer=timer
        self._current = 0

    # Proposito: retorna verdadero si el cpu esta en estado inactivo
    # Precondiccion:-
    def isIdle(self):
        return self._cpu.get_pc() == -1

    # Proposito:actualiza el Program counter del pcb
    # Precondiccion:-
    def save(self, pcb):
        pcb.set_pc(self._cpu.get_pc())


    # Proposito: guarda el pid actual, setea el cpu en 0 su pc, setea el bd y limit en el mmu
    # Precondiccion:
    def load(self, pcb):
        self.setCurrent(pcb.get_pid())
        self._cpu.set_pc(pcb.get_pc())
        self._mmu.setPosition(pcb)

    # Proposito: retorna el pid
    # Precondiccion: -
    def getPidActual(self):
        return self._current

    # Proposito: setea el pc en osiosio
    # Precondiccion:-
    def idlePc(self):
        self._cpu.set_pc(-1)
        self.setCurrent(-1)

    # Proposito: setea el current
    # Precondiccion:-
    def setCurrent(self, pid):
        self._current = pid


