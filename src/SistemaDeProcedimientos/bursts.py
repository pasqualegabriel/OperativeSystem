#!/usr/bin/env python
# -*- coding: utf-8 -*-s
class Bursts:
    def __init__(self,program):
        self._counterOne=0
        self._lent = 0
        self._head = None
        self._items=self.toCalculateBurst(program)

    # Devuelve la lista de rafagas del programa sin la primer rafaga
    # Guardando la primer rafaga en el colaborador interno self._head
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
        element=items.pop(0)
        self._head= element
        return items

    def get(self,pc):
        if  self.toDiscountOne(pc) >= self._head and len(self._items)!=0:
            newBurst=self._items.pop(0)
            self._head=newBurst
            self.set_counterOne(pc)
            return newBurst

        else:
            newBurst =self._head - self.toDiscountOne(pc)
            self.set_counterOne(pc)
            self._head = newBurst
            return newBurst

    def get_items(self):
        return self._items

    def get_head(self):
        return self._head

    def toDiscountOne(self,pc):
        return pc-self._counterOne

    def set_counterOne(self, pc):
        self._counterOne = pc