#!/usr/bin/env python
# -*- coding: utf-8 -*-s

class NewProgram:
    def tick(self, count, log):
        if count == 7:
            log.getIntManager().handle("NEW", "paint.exe")
            log.printNewMemoryAndMemoryManager("paint.exe")
            log.getIntManager().handle("NEW", "vlc.exe")
            log.printNewMemoryAndMemoryManager("vlc.exe")
