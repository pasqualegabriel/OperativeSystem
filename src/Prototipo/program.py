#!/usr/bin/env python
# -*- coding: utf-8 -*-s

from Prototipo.instructions import *

class Program:
    def __init__(self, name, instructions, prioridad):
        self._name = name
        self._instructions = self.expand(instructions)
        self._priority = prioridad

    # Getter de _name
    def name(self):
        return self._name

    # Getter de _instructions
    def instructions(self):
        return self._instructions

    def getLista(self):
        return self._instructions

    def get_priority(self):
        return self._priority

    # Ej: expand([CPU(3),IO(2)]) retorna [CPU,CPU,CPU,IO,IO,EXIT]
    @staticmethod
    def expand(instructions):
        expanded = []
        for instr in instructions:
            expanded.extend(instr.expand())
        if not expanded[-1].isExit():  # Si la instruccion final no es EXIT, agrega el Exit.
            expanded.append(EXIT(0))
        return expanded

    def longitud(self):
        return len(self._instructions)

    @staticmethod
    def isProgram():
        return True

    def getSubInstructions(self,index,indexLimit):
        if indexLimit > self.longitud():
            return self._instructions[index:]
        else:
            return self._instructions[index:indexLimit]


    def __repr__(self):
        return "Program({name}, {instructions})".format(name=self._name, instructions=self._instructions)
