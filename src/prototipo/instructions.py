#!/usr/bin/env python
# -*- coding: utf-8 -*-s

# Clase instruccion
# colaborador interno count
class Instr:
    def __init__(self, count):
        self._count = count

# Retorna False
    def isExit(self): 
        return False

# Getter del colaborador interno _count
    @property
    def count(self):
        return self._count

# Crea un array con la cantidad de CPU o IO correspondiente
# Ej: expand(CPU(3)), retorna [CPU,CPU,CPU]
# self.__class crea una array de la clase de instruccion que recibe.
    def expand(self):
        expanded = []
        for _ in range(self._count):
            expanded.append(self.__class__(0))
        return expanded

#CPU, subclase de Instr
class CPU(Instr): 
    def __repr__(self):
        if self._count:
            return "CPU({count})".format(count=self._count) 
            #Retorna un string con el valor del colaborador interno _count
        else:
            return "CPU"

class IO(Instr):
    def __repr__(self):
        if self._count:
            return "IO({count})".format(count=self._count) 
        else:
            return "IO"

class EXIT(Instr):
    def isExit(self): #Modifica el metodo de isExit definido el la superclase Instr, haciendo que retorne True   
        return True
    def __repr__(self):
        return "EXIT"