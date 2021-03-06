#!/usr/bin/env python
# -*- coding: utf-8 -*-s

class Instr:
    def __init__(self, count):
        self._count = count


    #Proposito:Retorna false, uso de identificador
    #Precondicion:-
    def isExit(self):
        return False
    #Proposito:Retorna false, uso de identificador
    #Precondicion:
    def isIO(self):
        return False

    #Proposito:Retorna false, uso de identificador
    #Precondicion:-
    def isCPU(self):
        return False 

    #Proposito:Retorna el count
    #Precondicion:-
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

    #Proposito:Retorna true, uso de identificador
    #Precondicion:
    def isCPU(self):
        return True

    def __repr__(self):
        if self._count:
            return "CPU({count})".format(count=self._count)
            # Retorna un string con el valor del colaborador interno _count
        else:
            return "CPU "

class IO(Instr):

    #Proposito:Retorna el id
    #Precondicion:-
    def getId(self):
        return 1
    #Proposito:Retorna true, uso de identifiador.
    #Precondicion:-
    def isIO(self):
        return True

    def __repr__(self):
        if self._count:
            return "IO({count})".format(count=self._count)
        else:
            return " IO "

class IO_1(IO):

    def __repr__(self):
        if self._count:
            return "IO_1({count})".format(count=self._count)
        else:
            return "IO_1"

class IO_2(IO):

    #Proposito:Retorna el id.
    #Precondicion:-
    def getId(self):
        return 2
    
    def __repr__(self):
        if self._count:
            return "IO_2({count})".format(count=self._count)
        else:
            return "IO_2"

class IO_3(IO):

    #Proposito:Retorna el id.
    #Precondicion:-
    def getId(self):
        return 3

    def __repr__(self):
        if self._count:
            return "IO_3({count})".format(count=self._count)
        else:
            return "IO_3"


class EXIT(Instr):

    #Proposito:Retorna true, uso de identificador.
    #Precondicion:-
    def isExit(self):
        return True   

    def __repr__(self):
        return "EXIT"