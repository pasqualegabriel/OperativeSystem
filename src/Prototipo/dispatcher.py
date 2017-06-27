#!/usr/bin/env python
# -*- coding: utf-8 -*-s

class Dispatcher:
    def __init__(self, mmu, cpu):
        self._mmu       = mmu
        self._cpu       = cpu
        self._current   = 0

    # Proposito: Retorna True si el cpu esta en estado inactivo.
    # Precondiccion:-
    def isIdle(self):
        return self._cpu.get_pc() == -1

    # Proposito:Actualiza el Program counter del pcb actual en cpu.
    # Precondiccion:-
    def save(self, pcb):
        pcb.set_pc(self._cpu.get_pc())


    # Proposito:Guarda el pid actual en cpu, pone el program conter del cpu en 0, envia el pcb al mmm
    #           para que sepa donde fechear.
    # Precondiccion:-
    def load(self, pcb):
        self.setCurrent(pcb.get_pid())
        self._cpu.set_pc(pcb.get_pc())
        self._mmu.setPosition(pcb)

    # Proposito: Retorna el pid que esta en cpu.
    # Precondiccion: -
    def getPidInCpu(self):
        return self._current

    # Proposito: Setea el pc en osiosio
    # Precondiccion:-
    def idlePc(self):
        self._cpu.set_pc(-1)
        self.setCurrent(-1)

    # Proposito: Setea el current
    # Precondiccion:-
    def setCurrent(self, pid):
        self._current = pid


