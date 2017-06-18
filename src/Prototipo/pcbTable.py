#!/usr/bin/env python
# -*- coding: utf-8 -*-s

# Representa al PCNTable del sistema, con un colabordor interno map.
# La PCBTable se encarga de almacenar el pid y el pcb de dicho pid.
from tabulate import tabulate


class PCBTable:
    def __init__(self):
        self._pcbs = {}

    # Proposito:Inserta un elemento en el mapa de clave:valor.
    # Precondiccion: la clave no debe existir en el mapa.
    def addPCB(self, pcb):
        self._pcbs[pcb.get_pid()] = pcb

    # Proposito:devuelve el valor dado una clave.
    # Precondiccion:debe existir dicha clave.
    def lookUpPCB(self, pid):
        try:
            return self._pcbs.get(pid)
        except:
            raise ValueError("El PCBTable esta vacio")


    # Proposito:remueve del mapa la clave y valor.
    # Precondiccion:debe existir dicha clave.
    def removePCB(self, pid):
        del self._pcbs[pid]

    # Proposito:verifica que el map este vacio, si lo esta devuelve true caso contrario false
    # Precondiccion: -
    def pcbTabletIsNill(self):
        return self._pcbs == {}

    def getPcbs(self):
        return self._pcbs
