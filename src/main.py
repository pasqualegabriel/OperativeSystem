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
    p0 = Program("SO.exe", [CPU(3)], 2)
    p1 = Program("Word.exe", [CPU(4)], 1)
    p2 = Program("PC.exe", [CPU(3)], 3)
    p3 = Program("Text.exe", [CPU(5)], 1)

    p4 = Program("paint.exe", [CPU(1)], 2)
    p5 = Program("vlc.exe", [CPU(3), IO_2(3), CPU(4)], 2)
    #######################################################

    disco = Disco()
    ls = [p0, p1, p2, "so.pdf", p3, p4, p5]

    disco.add_files(ls)

    startPrograms = ["SO.exe", "Word.exe", "PC.exe", "Text.exe"]
    programs = [(7, "paint.exe"), (8, "vlc.exe")]

    schedulersFactory = SchedulersFactory()
    kernel = Kernel(disco, schedulersFactory)
    kernel.execPrograms(startPrograms, programs, log)

    '''
    #ejemplo: compactacion con scheduler sjf preemptive, tamanio de la memoria = 32
    p0 = Program("SO.exe", [CPU(2)], 2)
    p1 = Program("Word.exe", [CPU(4)], 1)
    p2 = Program("PC.exe", [CPU(3)], 3)
    p3 = Program("Text.exe", [CPU(5)], 1)

    p4 = Program("paint.exe", [CPU(1)], 2)
    p5 = Program("vlc.exe", [CPU(10), IO_2(3), CPU(2)], 2)
    '''
