#!/usr/bin/env python
# -*- coding: utf-8 -*-s
from Prototipo.intManager import Irq


class Timer:

    def __init__(self, intManager, quantum):
        self._timer = 1
        self._quantum = quantum
        self._intManager = intManager


    def tick(self):
        if self.fullTimer():
            self._intManager.handle(Irq.TIME_OUT, None)
            self.set_timer()
        self._timer += 1


    def fullTimer(self):
        return self._timer == self._quantum

    def set_timer(self):
        self._timer = 0




