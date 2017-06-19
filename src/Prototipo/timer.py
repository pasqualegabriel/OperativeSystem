#!/usr/bin/env python
# -*- coding: utf-8 -*-s
from Prototipo.intManager import Irq

class Timer:
    # Se inicializa con un quantum, el intManager, y un contador
    def __init__(self, intManager, quantum):
        self._timer      = 1
        self._quantum    = quantum
        self._intManager = intManager

    # Proposito: Si es full timer, ejecuta la interrupcion TIME_OUT y resetea el contador
    # luego aumenta en uno el contador
    def tick(self):
        if self.fullTimer():
            self._intManager.handle(Irq.TIME_OUT, None)
            self.resetTimer()
        self._timer += 1

    # Proposito: Retorna true si el contador es igual al quantum
    def fullTimer(self):
        return self._timer == self._quantum

    # Proposito: Setea al contador en 0
    def resetTimer(self):
        self._timer = 0




