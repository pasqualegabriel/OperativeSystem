#!/usr/bin/env python
# -*- coding: utf-8 -*-s
from prototipo.instructions import Instr,CPU,IO,EXIT

#Colaboradores internos: _name y _insructions
class Program:
    def __init__(self, name, instructions):
        self._name = name
        self._instructions = self.expand(instructions)

# Getter de _name
    @property
    def name(self):
        return self._name

# Getter de _instructions
    def instructions(self):
        return self._instructions

    def getLista(self):
        return self._instructions

# Ej: expand([CPU(3),IO(2)]) retorna [CPU,CPU,CPU,IO,IO,EXIT]
    def expand(self, instructions):
        expanded = []
        for instr in instructions:
            expanded.extend(instr.expand())
        if not expanded[-1].isExit(): #Si la instruccion final no es EXIT, agrega el Exit.
            expanded.append(EXIT(0))
        return expanded

    def longitud(self):
        l = 0
        for i in self._instructions:
            l += 1
        return l

    def __repr__(self):
        return "Program({name}, {instructions})".format(name=self._name, instructions=self._instructions)