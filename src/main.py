#!/usr/bin/env python
# -*- coding: utf-8 -*-s

from Prototipo.disco import Disco
from Prototipo.instructions import *
from Prototipo.kernel import *
from Prototipo.program import Program
from Prototipo.print import Print

if __name__ == '__main__':

    log = Print()

    ################# Programs ############################
    p0 = Program("SO.exe",    [CPU(3)], 5)
    p1 = Program("Word.exe",  [CPU(2)], 2)
    p2 = Program("PC.exe",    [CPU(2)], 3)
    p3 = Program("Text.exe",  [CPU(1)], 1)
    p4 = Program("Paint.exe", [CPU(4)], 4)
    #######################################################

    disco = Disco()
    ls = [p0, p1, p2, "historiaSO.pdf", p3, p4]

    disco.add_files(ls)

    programs = [(0, "SO.exe"), (1, "Word.exe"), (3, "PC.exe"), (4, "Text.exe"), (7, "Paint.exe")]

    kernelFactoty = KernelFactoty(disco)
    kernel = kernelFactoty.initialize()
    kernel.initialize(programs, log)



    '''
    #ejemplo: compactacion con scheduler sjf preemptive, tamanio de la memoria = 32

    log = Print()
    
    ################# Programs ############################
    p0 = Program("SO.exe",    [CPU(4)], 2)
    p1 = Program("Word.exe",  [CPU(6)], 1)
    p2 = Program("PC.exe",    [CPU(5)], 3)
    p3 = Program("Text.exe",  [CPU(7)], 1)
    p4 = Program("Paint.exe", [CPU(3)], 2)
    p5 = Program("Vlc.exe",   [CPU(5), IO_2(2)], 2)
    #######################################################
    
    disco = Disco()
    ls = [p0, p1, p2, "so.pdf", p3, p4, p5]

    disco.add_files(ls)

    programs = [(0, "SO.exe"), (1, "Word.exe"), (2, "PC.exe"), (3, "Text.exe"), (7, "Paint.exe"), (11, "Vlc.exe")]

    kernelFactoty = KernelFactoty(disco)
    kernel = kernelFactoty.initialize()
    kernel.initialize(programs, log)
    '''
