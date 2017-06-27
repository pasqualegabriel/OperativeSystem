#!/usr/bin/env python
# -*- coding: utf-8 -*-s

from Prototipo.instructions import *

class Program:
    def __init__(self, name, instructions, prioridad):
        self._name = name
        self._instructions = self.expand(instructions)
        self._priority = prioridad

    #Proposito:Retorna el name.
    #Precondicion:
    def name(self):
        return self._name

    #Proposito:retorna la intruccion
    #Precondicion:-
    def instructions(self):
        return self._instructions

    #Proposito:retorna las intrucciones.
    #Precondicion:
    def getInstructions(self):
        return self._instructions

    #Proposito:retorna la prioridad
    #Precondicion:--
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

    #Proposito:Retorna la longitud de las intrucciones
    #Precondicion:-
    def longitud(self):
        return len(self._instructions)

    #Proposito:Retonra true, sirve de indentificador.
    #Precondicion:-
    @staticmethod
    def isProgram():
        return True

    #Proposito:Retorna una sub lista dependiendo indexLimit y el index.
    #Precondicion:-
    def getSubInstructions(self,index,indexLimit):
        if indexLimit > self.longitud():
            return self._instructions[index:]
        else:
            return self._instructions[index:indexLimit]


    def __repr__(self):
        return "Program({name}, {instructions})".format(name=self._name, instructions=self._instructions)
