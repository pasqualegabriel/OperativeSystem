#!/usr/bin/env python
# -*- coding: utf-8 -*-s

class IntManager:
    def __init__(self):
        self._irq={}

    def register(self, instructionName,routine):
        self._irq[instructionName]=routine

    def handle(self,instructionName,program):
        self._irq.get(instructionName).execute(program)

                
    

