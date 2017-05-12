#!/usr/bin/env python
# -*- coding: utf-8 -*-s

class Tuple:
    def __init__(self, primer, segundo):
        self._primerElement = primer
        self._segundoElement = segundo

    def get_primer(self):
        return self._primerElement

    def get_segundo(self):
        return self._segundoElement
