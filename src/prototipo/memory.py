#!/usr/bin/env python
# -*- coding: utf-8 -*-s
from tabulate import tabulate

# Representa la Memoria, con colaborador interno memory inicializado con una lista vacia 
# La Memoria se encarga de almacenar las instrucciones de los programas
class Memory:
    def __init__(self):
        self._memory = []
        self._procesos = 0

    #Proposito:Carga la instrucciones en la memoria.
    #Precondiccion:- 
    def load(self, intrucciones):
        for i in intrucciones.getLista():
            self._memory.append(i)
            
    #Proposito:seatea el valor<valor> en la posicion<pos> de la memoria
    #precondiccion: Debe existir pos en la memoria     
    def set_pos(self, posicion, valor):
        self._memory[posicion]=valor

    #Proposito: Retorna la instruccion del pc recibido como argumento.
    #Precondiccion: Debe existir dicha posicion en la memoria 
    def get(self, posicion):
        return self._memory[posicion]
    
    #Proposito:devuelve true si los procesos son mayor que 0, caso contrario denota false
    #Precondicion: -
    def hayProcesos(self):
        return self._procesos>0 
    
    #Proposito: suma 1 a procesos
    #Precondicion: -
    def sumarProceso(self):
        self._procesos += 1

    #Proposito: resta 1 a procesos
    #Precondicion: -
    def restarProceso(self):
         self._procesos -= 1

    def __repr__(self):
        return tabulate(enumerate(self._memory), tablefmt='psql') #pretty print. 
      