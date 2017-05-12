#!/usr/bin/env python
# -*- coding: utf-8 -*-s

class Instr:
    def __init__(self, count):
        self._count = count

    # Retorna False
    def isExit(self):
        return False

    def isIO(self):
        return False

    def isCPU(self):
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


# CPU, subclase de Instr
class CPU(Instr):

    def isCPU(self):
        return True

    def __repr__(self):
        if self._count:
            return "CPU({count})".format(count=self._count)
            # Retorna un string con el valor del colaborador interno _count
        else:
            return "CPU"

class IO(Instr):
    
    def isIO(self):
        return True

    def __repr__(self):
        if self._count:
            return "IO({count})".format(count=self._count)
        else:
            return "IO"

class IO_1(IO):

    def __repr__(self):
        if self._count:
            return "IO_1({count})".format(count=self._count)
        else:
            return "IO_1"

class IO_2(IO):
    
    def __repr__(self):
        if self._count:
            return "IO_2({count})".format(count=self._count)
        else:
            return "IO_2"

class IO_3(IO):
    def __repr__(self):
        if self._count:
            return "IO_3({count})".format(count=self._count)
        else:
            return "IO_3"


class EXIT(Instr):

    # Retorna False
    def isExit(self):
        return True   

    def __repr__(self):
        return "EXIT"