#!/usr/bin/env python
# -*- coding: utf-8 -*-s

class Disco:
    def __init__(self):
        self._files=[]

    def files(self):
        return self._files

    def add_file(self, file):
        self._files.append(file)

    def remove_file(self, file):
        self._files.remove(file)

    def add_files(self,files):
        for i in files:
            self._files.append(i)



