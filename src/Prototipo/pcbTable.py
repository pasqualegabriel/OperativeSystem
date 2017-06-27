#!/usr/bin/env python
# -*- coding: utf-8 -*-s


class PCBTable:
    def __init__(self):
        self._pcb = {}

    # Proposito:Inserta un elemento en la clave<pid> con valor <pcb>
    # Precondiccion: la clave no debe existir.
    def addPCB(self, pcb):
        self._pcb[pcb.get_pid()] = pcb

    # Proposito:devuelve el valor dado una clave.
    # Precondiccion:debe existir dicha clave.
    def lookUpPCB(self, pid):
        try:
            return self._pcb.get(pid)
        except:
            raise ValueError("The PCBTable is empty")


    # Proposito:Remueve la clave<pid> y el valor que almacena.
    # Precondiccion:debe existir dicha clave.
    def removePCB(self, pid):
        del self._pcb[pid]

    # Proposito:Denota true si hay al menos un elemento.
    # Precondiccion: -
    def pcbTabletIsEmpty(self):
        return self._pcb == {}

    #Proposito:retorna el diccionario de pcb
    #Precondicion:-
    def getPCB(self):
        return self._pcb
