#!/usr/bin/env python
# -*- coding: utf-8 -*-s

# Representa el PCB de un sistema, con colaboradores internos pid, status, pc, bd, limit
# Es el procedimiento que se encarga de guardar el pid
from tabulate import tabulate

from Prototipo.pageTable import PageTable
from Prototipo.Schedulers.bursts import Bursts



class PCB:
    def __init__(self, pid):
        self._pid           = pid
        self._status        = "new"
        self._pc            = 0
        self._bd            = 0
        self._limit         = 0


    #Proposito:inicializa la prioridad, el burst, el name y
    #precondicion:-
    def initialize(self, program, requiredPages):
        self._priority = program.get_priority()
        self._burst = Bursts(program)
        self._name = program.name()
        if None!=requiredPages:
            self._pageTable=self.createPageTable(requiredPages)

    #Proposito:setea el pc<pc>
    #Precondicion:-
    def set_pc(self, pc):
        self._pc = pc

    #Proposito:setea el bd<bc>
    #Precondicion:-
    def set_bd(self, bd):
        self._bd = bd

    #Proposito:sete el limit <limit>
    #Precondicion:
    def set_limit(self, lm):
        self._limit = lm

    #Proposito:setea el status<status>
    #Precondicion:
    def set_status(self, status):
        self._status = status

    #Proposito:setea el priority<priority>
    #Precondicion:-
    def set_priority(self, priority):
        self._priority = priority

    #Proposito:setea el burst<burst>
    #Precondicion:
    def set_bursts(self, burst):
        self._burst = burst

    #Proposito:setea el pageTablet<pages>
    #Precondicion:
    def setPages(self, pages):
        self._pageTable = pages

    #Proposito: agrega paginas al pageTablet
    #Precondicion:
    def addPages(self, pagesFree):
        self._pageTable.append(pagesFree)

    #Proposito: setea el limit<limit> y el bd<bd>
    #Precondicion:-
    def set_bd_limit(self, bd, limit):
        self.set_bd(bd)
        self.set_limit(limit)

    #Proposito:retorna el pid
    #Precondicion:-
    def get_pid(self):
        return self._pid

    #Proposito:retorna el bd
    #Precondicion:-
    def get_bd(self):
        return self._bd

    #Proposito:retorna el limit
    #Precondicion:-
    def get_limit(self):
        return self._limit

    #Proposito:retorna el status
    #Precondicion:-
    def get_status(self):
        return self._status

    #Proposito:retorna el pc
    #Precondicion:-
    def get_pc(self):
        return self._pc

    #Proposito:retona la priority
    #Precondicion:-
    def get_priority(self):
        return self._priority

    #Proposito:retorna el bursts
    #Precondicion:-
    def get_bursts(self):
        return self._burst

    #Proposito:retorna un burst.
    #Precondicion:
    def get_burst(self):
        return self._burst.get(self._pc)

    #Proposito:retorna la cabeza de un burst.
    #Precondicion:
    def get_firstBurst(self):
        return self._burst.getHeadBurst()

    #Proposito:retorna el name
    #Precondicion:-
    def get_name(self):
        return self._name

    #Proposito:retorna el pageTablet.
    #Precondicion:
    def getPageTable(self):
        return self._pageTable

    #Proposito:Inizializa pageTablet
    #Precondicion:-
    def createPageTable(self, requiredPages):
        return PageTable(requiredPages)

    def __repr__(self):
        #return tabulate(enumerate(self._pages), tablefmt='psql')
        res = []
        pageNumber = 0
        for page in self._pageTable.getPages():
            res.append(["Page: " + str(pageNumber) + "  {p}".format(p=page)])
            pageNumber += 1
        return tabulate(res, headers=["PCB  Pid={nro:2d}  Page Table:".format(nro=self._pid)], tablefmt='psql')

