#!/usr/bin/env python
# -*- coding: utf-8 -*-s

class Frame:
    def __init__(self, bd):
        self._bd   = bd
        self._used = False
        self._pid  = -1

    def getBD(self):
        return self._bd

    def isUsed(self):
        return self._used

    def setUsed(self, valid):
        self._used = valid

    def setPid(self, pid):
        self._pid = pid

    def getPId(self):
        return self._pid

    def __repr__(self):
        return "Pid={pid:2d}   Bd={bd:2d}   Used={used:1}".format(pid=self._pid, bd=self._bd, used=self._used)