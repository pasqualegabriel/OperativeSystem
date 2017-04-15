#!/usr/bin/env python
# -*- coding: utf-8 -*-s
import logging
from prototipo.kernel import Kernel
from prototipo.program import Program
from prototipo.instructions import Instr,CPU,IO,EXIT

if __name__ == '__main__':
    ## Configure Logger
    logger = logging.getLogger()
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    logger.info('Starting emulator')

    p1 = Program("Pycharm.exe", [CPU(5), IO(3)])
    p2 = Program("Word.exe", [CPU(3), CPU(2)])
    p3 = Program("Exel.exe", [CPU(1), IO(1)])
    p4 = Program("Text.exe", [CPU(1), IO(1), CPU(1)])
    ls = [p1,p2,p3,p4]
    k = Kernel()
    k.execPrograms(ls, logger)