#!/usr/bin/env python
# -*- coding: utf-8 -*-s

# Representa al PCNTable del sistema, con un colabordor interno map.
# La PCBTable se encarga de almacenar el pid y el pcb de dicho pid.
class PCBTable:
    def __init__(self):
        self._map = {}

    # Proposito:Inserta un elemento en el mapa de clave:valor.
    # Precondiccion: la clave no debe existir en el mapa.
    def addPCB(self, pcb):
        self._map[pcb.get_pid()] = pcb

    # Proposito:devuelve el valor dado una clave.
    # Precondiccion:debe existir dicha clave.
    def lookUpPCB(self, pid):
        try:

            return self._map.get(pid)

        except:

            raise ValueError("El PCBTABLET esta vacio")



            # return self._map.get(pid)

    # Proposito:remueve del mapa la clave y valor.
    # Precondiccion:debe existir dicha clave.
    def removePCB(self, pid):
        del self._map[pid]

    # Proposito:verifica que el map este vacio, si lo esta devuelve true caso contrario false
    # Precondiccion: -
    def pcbTabletIsNill(self):
        return self._map == {}
