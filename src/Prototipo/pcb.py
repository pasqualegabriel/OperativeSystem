#!/usr/bin/env python
# -*- coding: utf-8 -*-s

# Representa el PCB de un sistema, con colaboradores internos pid, status, pc, bd, limit
# Es el procedimiento que se encarga de guardar el pid
from Prototipo.page import Page
from Prototipo.pageTable import PageTable
from Prototipo.Schedulers.bursts import Bursts



class PCB:
    def __init__(self, pid):
        self._pid    = pid
        self._status = "new"
        self._pc     = 0
        self._bd     = 0
        self._limit  = 0
        #self._priority = None
        #self._burst    = None
        #self._name     = None
        #self._pageTable = []

    #Proposito:inicializa la prioridad, el burst, el name y
    #precondicion:
    def initialize(self, program, requiredPages):
        self._priority = program.get_priority()
        self._burst = Bursts(program)
        self._name = program.name()
        if None!=requiredPages:
            self._pageTable=self.createPageTable(requiredPages)

    def set_pc(self, pc):
        self._pc = pc

    def set_bd(self, bd):
        self._bd = bd

    def set_limit(self, lm):
        self._limit = lm

    def set_status(self, status):
        self._status = status

    def set_priority(self, priority):
        self._priority = priority

    def set_bursts(self, burst):
        self._burst = burst

    def setPages(self,pages):
        self._pageTable = pages

    def addPages(self, pagesFree):
        self._pageTable.append(pagesFree)

    def set_bd_limit(self, bd, limit):
        self.set_bd(bd)
        self.set_limit(limit)

    def get_pid(self):
        return self._pid

    def get_bd(self):
        return self._bd

    def get_limit(self):
        return self._limit

    def get_status(self):
        return self._status

    def get_pc(self):
        return self._pc

    def get_priority(self):
        return self._priority

    def get_bursts(self):
        return self._burst

    def get_burst(self):
        return self._burst.get(self._pc)

    def get_firstBurst(self):
        return self._burst.getHeadBurst()

    def get_name(self):
        return self._name

    def getPageTable(self):
        return self._pageTable

    #Proposito:Inizializa pageTablet
    #Precondicion:-
    def createPageTable(self, requiredPages):
        return PageTable(requiredPages)

    def __repr__(self):
        return "{pageTable}\n".format(pageTable=self._pageTable)