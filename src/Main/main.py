#!/usr/bin/env python
# -*- coding: utf-8 -*-s
import logging

from Kernel.kernel import Kernel
from SistemaDeProgramas.instructions import *
from SistemaDeProgramas.program import Program
from hardwareAndCollaborators.disco import Disco

if __name__ == '__main__':

    logger = logging.getLogger()
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    logger.info('Starting emulator')

    p1 = Program("SO.exe", [IO(2)],2)
    p2 = Program("Word.exe", [CPU(4)],1)
    p3 = Program("PC.exe", [CPU(3)],3)
    p4 = Program("Text.exe", [CPU(5)],1)

    ls = [p1,p2,"aa",p3,p4]

    d = Disco()
    d.add_files(ls)

    lsp = ["SO.exe","Word.exe","PC.exe","Text.exe"]

    k = Kernel(d)
    k.execPrograms(lsp, logger)
