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
    ###########PRogramas a cargar en disco######################3
    p0 = Program("SO.exe", [CPU(2)], 2)
    p1 = Program("Word.exe", [CPU(4)], 1)
    p2 = Program("PC.exe", [CPU(3)], 3)
    p3 = Program("Text.exe", [CPU(5)], 1)

    p4 = Program("paint.exe", [CPU(1)], 2)
    p5 = Program("vlc.exe", [CPU(10), IO_2(3), CPU(2)], 2)
    #################################################
    disco = Disco()
    ls = [p0, p1, p2, "so.pdf", p3, p4, p5]
    disco.add_files(ls)

    programs = ["SO.exe", "Word.exe", "PC.exe", "Text.exe"]

    sf = SchedulersFactory()
    kernel = Kernel(disco, sf)
    kernel.execPrograms(programs, log)

    '''
    #ejemplo: compactacion con scheduler sjf preemptive, tamanio de la memoria = 32
    p0 = program("so.exe", [cpu(2)], 2)
    p1 = program("word.exe", [cpu(4)], 1)
    p2 = program("pc.exe", [cpu(3)], 3)
    p3 = program("text.exe", [cpu(5)], 1)

    p4 = program("paint.exe", [cpu(1)], 2)
    p5 = program("vlc.exe", [cpu(10), io_2(3), cpu(2)], 2)
    '''
