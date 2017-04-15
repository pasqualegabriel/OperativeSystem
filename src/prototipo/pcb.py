#!/usr/bin/env python
# -*- coding: utf-8 -*-s

# Representa el PCB de un sistema, con colaboradores internos pid, status, pc, bd, limit
# Es el procedimiento que se encarga de guardar el pid
class PCB:
    def __init__(self, pid):
        self._pid=pid
        self._status="new"
        self._pc=0
        self._bd= None #esta en none porque todabia el loader no le asigno el espacio en memoria
        self._limit=None #esta en none porque todabia el loader no le asigno el espacio en memoria

    #Proposito: Setea el bd
    #Precondiccion: -
    def set_bd(self, bd):
        self._bd=bd
    
    #Proposito: setea el limit
    #Precondiccion: --
    def set_limit(self,lm):
        self._limit=lm
    
    #Proposito: Retorna el pid
    #Precondiccion: -
    def get_pid(self):
        return self._pid
    
    #Proposito:setea el status
    #Precondiccion:-
    def set_status(self, status):
        self._status=status
    
    #Proposito: retorna el bd
    #Precondiccion: -
    @property
    def get_bd(self):
        return self._bd
    
    #Proposito: retorna el limit
    #Precondiccion: -
    @property
    def get_limit(self):
        return self._limit