#!/usr/bin/env python
# -*- coding: utf-8 -*-s

# Representa el PCB de un sistema, con colaboradores internos pid, status, pc, bd, limit
# Es el procedimiento que se encarga de guardar el pid
from SistemaDeProcedimientos.bursts import Bursts


class PCB:
    def __init__(self, pid, program):
        self._pid = pid
        self._status = "new"
        self._pc = 0
        self._bd = 0
        self._limit = 0
        self._priority = program.get_priority()
        self._burst = Bursts(program)
        self._name = program.name()

    def set_pc(self, pc):
        self._pc = pc

    def set_bd(self, bd):
        self._bd = bd

    def set_limit(self, lm):
        self._limit = lm

    def set_status(self, status):
        self._status = status

    def set_priority(self, priority):
        self._priority = priority

    def set_bursts(self, burst):
        self._burst = burst

    def get_pid(self):
        return self._pid

    def get_bd(self):
        return self._bd

    def get_limit(self):
        return self._limit

    def get_status(self):
        return self._status

    def get_pc(self):
        return self._pc

    def get_priority(self):
        return self._priority

    def get_bursts(self):
        return self._burst

    def get_burst(self):
        return self._burst.get(self._pc)

    def get_firstBurst(self):
        return self._burst.get_head()

    def get_name(self):
        return self._name