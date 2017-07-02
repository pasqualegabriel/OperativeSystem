#!/usr/bin/env python
# -*- coding: utf-8 -*-s

class Frame:
    def __init__(self, bd):
        self._bd                    = bd
        self._pid                   = -1
        self._pageNumber            = -1
        self._referenceBit          =  1
        self._nextFrameClock        = -1
        self._previousFrameClock    = -1

    #Proposito:Retorna el bd
    #Pecondicion:-
    def getBD(self):
        return self._bd

    #Proposito:setea el pid<pid>
    #Pecondicion:-
    def setPid(self, pid):
        self._pid = pid

    #Proposito:retorna el pid
    #Pecondicion:--
    def getPId(self):
        return self._pid

    #Proposito:setea el pageNumber<pageNumber>
    #Pecondicion:-
    def setPageNumber(self, pageNumber):
        self._pageNumber = pageNumber

    #Proposito:retorna el pageNumber
    #Pecondicion:-
    def getPageNumber(self):
        return self._pageNumber

    #Proposito:retorna referenceBit
    #Pecondicion:-
    def getReferenceBit(self):
        return self._referenceBit

    #Proposito:setea el referenceBit<referenceBit>
    #Pecondicion:
    def setReferenceBit(self,referenceBit):
        self._referenceBit=referenceBit

    #Proposito:setea el timeBIt <timeBit>
    #Precondicion:-
    def setTimeBit(self,timeBit):
        self._TimeBit=timeBit

    #Proposito:Retorna el timeBit
    #Precondicion:-
    def getTimeBit(self):
        return self._TimeBit


######Para algoritmo de remplazo reloj
        ##Geterrs
    def getNextFrameClock(self):
        return self._nextFrameClock

    def getPreviousFrameClock(self):
        return self._previousFrameClock

        ##Setters
    def updateNextFrameClock(self, oneFrameClock):
        self._nextFrameClock = oneFrameClock

    def updatePreviousFrameClock(self, oneFrameClock):
        self._previousFrameClock = oneFrameClock

    def __repr__(self):
        return "Pid={pid:2d}   Bd={bd:2d}   pageNumber={pn:2d}".format(pid=self._pid, bd=self._bd, pn=self._pageNumber)
