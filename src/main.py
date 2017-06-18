#!/usr/bin/env python
# -*- coding: utf-8 -*-s
from Prototipo.Schedulers.SchedulersFactory import SchedulersFactory
from Prototipo.disco import Disco
from Prototipo.instructions import *
from Prototipo.kernel import Kernel
from Prototipo.program import Program
from Prototipo.print import Print

if __name__ == '__main__':

    log = Print()

    ################# Programs ############################
    p0 = Program("SO.exe",    [CPU(7)], 4)
    p1 = Program("Word.exe",  [CPU(1)], 2)
    p2 = Program("paint.exe", [CPU(3)], 1)
    p3 = Program("vlc.exe",   [CPU(4)], 3)
    #0 = Program("SO.exe", [IO_2(3)], 4)
    #p1 = Program("Word.exe", [IO_2(1)], 2)
    #p2 = Program("paint.exe", [IO_2(3)], 1)
    #p3 = Program("vlc.exe", [IO_2(3)], 3)
    #######################################################

    disco = Disco()
    ls = [p0, p1, p2, "so.pdf", p3]

    disco.add_files(ls)

    programs = [(0, "SO.exe"), (1, "Word.exe"), (2, "paint.exe"), (3, "vlc.exe")]

    #schedulersFactory = SchedulersFactory()
    kernel = Kernel(disco)
    kernel.execPrograms(programs, log)

    '''
    #ejemplo: compactacion con scheduler sjf preemptive, tamanio de la memoria = 32
    p0 = Program("SO.exe", [CPU(2)], 2)
    p1 = Program("Word.exe", [CPU(4)], 1)
    p2 = Program("PC.exe", [CPU(3)], 3)
    p3 = Program("Text.exe", [CPU(5)], 1)

    p4 = Program("paint.exe", [CPU(1)], 2)
    p5 = Program("vlc.exe", [CPU(10), IO_2(3), CPU(2)], 2)
    '''
