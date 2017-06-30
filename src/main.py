#!/usr/bin/env python
# -*- coding: utf-8 -*-s

from Prototipo.disco import Disco
from Prototipo.instructions import *
from Prototipo.kernel import Kernel, Kernel2
from Prototipo.program import Program
from Prototipo.print import Print

if __name__ == '__main__':

    '''
    log = Print()

    ################# Programs ############################
    p0 = Program("SO.exe",    [CPU(7)], 4)
    p1 = Program("Word.exe",  [CPU(1)], 2)
    p2 = Program("paint.exe", [CPU(3)], 1)
    p3 = Program("vlc.exe",   [CPU(4)], 3)
    #######################################################

    disco = Disco()
    ls = [p0, p1, p2, "so.pdf", p3]

    disco.add_files(ls)

    programs = [(0, "SO.exe"), (1, "Word.exe"), (2, "paint.exe"), (3, "vlc.exe")]

    kernel = Kernel(disco)
    kernel.execPrograms(programs, log)

    '''
    log = Print()

    ################# Programs ############################
    p0 = Program("SO.exe",    [CPU(9)], 3)
    p1 = Program("Word.exe",  [CPU(4)], 2)
    p2 = Program("PC.exe",    [CPU(2)], 4)
    p3 = Program("Text.exe",  [CPU(7)], 5)
    p4 = Program("Paint.exe", [CPU(3)], 1)
    #######################################################

    disco = Disco()
    ls = [p0, p1, p2, "so.pdf", p3, p4]

    disco.add_files(ls)

    programs = [(0, "SO.exe"), (1, "Word.exe"), (3, "PC.exe"), (5, "Text.exe"), (7, "Paint.exe")]

    kernel = Kernel(disco)
    kernel.execPrograms(programs, log)



    '''
    #ejemplo: compactacion con scheduler sjf preemptive, tamanio de la memoria = 32
    
    log = Print()
    
    ################# Programs ############################
    p0 = Program("SO.exe",    [CPU(2)], 2)
    p1 = Program("Word.exe",  [CPU(4)], 1)
    p2 = Program("PC.exe",    [CPU(3)], 3)
    p3 = Program("Text.exe",  [CPU(5)], 1)
    p4 = Program("Paint.exe", [CPU(1)], 2)
    p5 = Program("Vlc.exe",   [CPU(10), IO_2(3), CPU(2)], 2)
    #######################################################
    
    disco = Disco()
    ls = [p0, p1, p2, "so.pdf", p3, p4, p5]

    disco.add_files(ls)

    programs = [(0, "SO.exe"), (1, "Word.exe"), (2, "PC.exe"), (3, "Text.exe"), (7, "Paint.exe"), (8, "Vlc.exe")]

    kernel = Kernel(disco)
    kernel.execPrograms(programs, log)
    '''
