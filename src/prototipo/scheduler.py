#!/usr/bin/env python
# -*- coding: utf-8 -*-s
from prototipo.queue import Queue

# Representa al Scheduler del sistema
# Colaboradores internos dispacher, ready, running, waiting, terminated, pcbTable
# El Scheduler se encarga de manejar de ready, running, waiting, terminated y avisa al dispacher
#  el pcb table a ejecutar
class Scheduler:
    def __init__(self,dispatcher,pcbTablet):
        self._dispatcher=dispatcher
        self._ready=Queue()
        self._running=0
        self._waiting=Queue()
        self._terminated=0
        self._pcbTablet=pcbTablet #preguntar
    
    #Proposito:agrega un elemento<pid> a la lista ready
    #Precondiccion:-
    def encolarEnReady(self, pid):
        self._ready.encolar(pid)

    #Proposito:agrega un elemento<pid> a la lista ready
    #Precondiccion:-
    def desencolarEnReady(self):
        return self._ready.desencolar()
    
    #Proposito:agrega un elemento<pid> a la lista wating
    #Precondiccion:-
    def encolarEnWaiting(self, pid):
        self._waiting.encolar(pid)

    #Proposito:agrega un elemento<pid> a la lista ready
    #Precondiccion:-
    def desencolarEnWaiting(self):
        return self._waiting.desencolar()
    
    #Proposito:agrega un elemento<pid> a la lista terminated
    #Precondiccion:-
    def encolarEnTerminated(self, pid):
        self._ready.encolar(pid)
    
    #Proposito:setea el running
    #Precondiccion:-
    def set_running(self,pid):
        self._running=pid
    
    #Proposito:f Verifica si la lista de ready este vacia, si lo esta no hace nada, 
    #  en caso que si saca un elemento<pid> de la lista ready y lo pasa a la running, 
    #  luego le avisa al dispacher que cargue el pcb de la misma.
    #Precondiccion:- -
    def siguienteRunning(self):
        ##Avisar a alguien que hay un id para mandar al cpu, y verificar que q no sea 
        ##vacia en tal caso poner el cpu en osioso. 
        if(not(self._ready.es_vacia())):
            self._running=self._ready.desencolar()
            pcb=self._pcbTablet.lookUpPCB(self._running)##variable estetica 
            self._dispatcher.load(pcb)  

    #Proposito: setea el pid del terminated
    #Precondiccion:-
    def set_terminated(self, pid):
        self._terminated = pid
    
    #Proposito: retorna pid del running
    #Precondiccion:-
    def get_Running(self):
        return self._running
        
    #Proposito:retorna el pid del terminated
    #Precondiccion:-
    def getTerminated(self):
        return self._terminated
    
    #Proposito: retorna la longitud del waiting
    #Precondiccion:-
    def lenWaiting(self):
        return self._waiting.lenQ()
    
    #Proposito: retorna la longitud del ready
    #Precondiccion:-
    def lenReady(self):
        return self._ready.lenQ()