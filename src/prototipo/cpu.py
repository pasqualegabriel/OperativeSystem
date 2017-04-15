#!/usr/bin/env python
# -*- coding: utf-8 -*-s
#from prototipo.intManager import IntManager
from time import sleep
#from clock import Clock

# Representa al Cpu del sistema
# Colaboradores internos memory, pc y ir. 
# La Cpu se encarga de ejecutar los procesos
class Cpu:        
    def __init__(self, mmu):
        self._pc = (-1)
        self._ir = None
        self._mmu = mmu
        self._intManager = None
    
    #Proposito: primer caso: llama los metodos fetch, decode y execute, 
    #segundo caso: intManager.kill()
    #tercer caso: cae en un bucle infinito momentamiamente(hasta que el profe nos de intruciones de seguir). 
    #Precondiccion: -
    def tick(self, log):
        if(not(self._mmu.mePase(self._pc)) and self._mmu.hayIntrucciones()):        
            self._fetch()
            self._decode()
            self._execute(log)
        elif(self._mmu.mePase(self._pc)):
            self._intManager.kill()
        elif(not self._mmu.hayIntrucciones()):
            pass 
        
    #Proposito: Le asigna a ir la insrtuccion traida de la memoria de la direccion del pc
    #  y incrementa el pc en 1.
    #Precondiccion:- 
    def _fetch(self):
        self._ir = self._mmu.fetch(self._pc)
        self._pc += 1

    #Proposito:-
    #Precondiccion:-
    def _decode(self):
        # el decode no hace nada en este emulador
        pass

    #Proposito:imprime en pantalla.
    #Precondiccion:-
    def _execute(self, log):
        log.debug("Exec: {op}, PC={pc}".format(op=self._ir, pc=self._pc))    
        sleep(0.25)
    
    #Proposito:setea al pc.
    #Precondiccion:-
    def set_pc(self,n):
        self._pc=n
        
    #Proposito:retorna pc.
    #Precondiccion:-
    def get_pc(self):
        return self._pc    

    #Proposito:retorna el ir.
    #Precondiccion:-
    def get_ir(self):
        return self._ir
        
    #Proposito: setea al intManager
    #Precondiccion:-
    def set_intManager(self,intManager):
        self._intManager=intManager
    
    #Proposito:imprime en pantalla.
    #Precondiccion:-
    def __repr__(self):
        return "CPU(PC={pc})".format(pc=self._pc)  
    