#!/usr/bin/env python
# -*- coding: utf-8 -*-s

class Bursts:
    def __init__(self,program):
        self._currentPc=0
        self._lent = 0
        self._head = None
        self._bursts=self.toCalculateBurst(program)

    # Proposito: Calcula la cantidad de rafagas que teiene el programa, la primera la guarda aparte<head>.
    def toCalculateBurst(self, program):
        burst=0
        items=[]
        instructions=program.instructions()
        for oneInstructions in instructions:
            if oneInstructions.isCPU():
                burst += 1
            else:
                burst += 1
                items.append(burst)
                self._lent += 1
                burst=0
        headBurst=items.pop(0)
        self._head= headBurst
        return items

    # Proposito: Retorna un burst dependiendo el pc actual.
    def get(self,pc):
        return self.updateBurst(pc)

    # Proposito: Retorna los burst
    def getBursts(self):
        return self._bursts

    # Precondicion: Retorna la cabeza de la lista de burst
    def getHeadBurst(self):
        return self._head

    # Proposito:
    def toDiscountOne(self, pc):
        return pc - self._currentPc

    # Proposito: Actualiza el pc actual
    def setCurrentPc(self, pc):
        self._currentPc = pc

    # Proposito: Actualiza el busrt actual o cambia al proximo.
    def updateBurst(self, pc):
        if  self.toDiscountOne(pc) >= self._head and len(self._bursts)!=0:
            newBurst = self._bursts.pop(0)
            self._head = newBurst
            self.setCurrentPc(pc)
            return newBurst

        else:
            newBurst = self._head - self.toDiscountOne(pc)
            self.setCurrentPc(pc)
            self._head = newBurst
            return newBurst