#!/usr/bin/env python
# -*- coding: utf-8 -*-s

class Disco:
    def __init__(self):
        self._files=[]

    #Proposito:Retorna el files.
    #Precondicion:-
    def files(self):
        return self._files

    #Proposito:agrea un file<fila> a la colleccion de file.
    #Precondicion:-
    def add_file(self, file):
        self._files.append(file)

    #Proposito:remueve un file<file> a la colleccion de file
    #Precondicion:-
    def remove_file(self, file):
        self._files.remove(file)

    #Proposito:agrega una colleccion de files<files> a la coleccion de file.
    #Precondicion:
    def add_files(self,files):
        for i in files:
            self._files.append(i)



