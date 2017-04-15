#!/usr/bin/env python
# -*- coding: utf-8 -*-s
from prototipo.pcbTable import PCBTable
from prototipo.dispatcher import Dispatcher
from prototipo.loader import Loader
from prototipo.scheduler import Scheduler
from prototipo.pcb import PCB

# Representa al IntManager del sistema
# colaboradores internos nexPid, pcbTable, loader, dispacher y Scheduler
# El IntManager se encarga de iniciar los procedimientos y borrar procedimientos
class IntManager:
    def __init__(self,cpu,memoria,mmu):
        self._nexPid=0
        self._pcbTable=PCBTable()
        self._loader=Loader(memoria)
        self._dispatcher=Dispatcher(mmu,cpu)
        self._Scheduler=Scheduler(self._dispatcher,self._pcbTable)

    #Proposito: crea un pcb, se le pide al loader que le otorga el bd al pcb, lo carga en memoria,
    #  pide al loader el limit para carga al pcb, cambia el estado en ready del pcb, carga al dispacher 
    #  el pcb si es que esta vacio caso contrario lo encola en la cola de ready, por ultimo lo almacena 
    #  al pc tablet, y prepara al proximo pid.
    #Precondiccion: Requiere una lista de instrucciones <p>
    def new(self,p):
        pcb=PCB(self._nexPid)##varible estatica
        pcb.set_bd(self._loader.get_bd)
        self._loader.cargarInMemory(p)
        pcb.set_limit(self._loader.get_limit)
        pcb.set_status("ready")
        
        if(self._dispatcher.isIdle()):
            self._dispatcher.load(pcb)
            
        else:
            self._Scheduler.encolarEnReady(pcb.get_pid())
        
        self._pcbTable.addPCB(pcb)
        self._nexPid+=1
        
    #Proposito: Consigue del dispacher el pid actual del cpu, pide al pcbtable el valor para seteralo,
    #  cambia el status del pcb en terminated, pone al pc del cpu en estado ocioso, libera la memoria
    #  del programa, borra de la pcbtable el pcb, y le pide al Scheduler el siguente pid en ready.
    #Precondiccion: El programa debe estar en el cpu
    def kill(self):
        pid=self._dispatcher.get_PidActual()#variable estetica
        pcb=self._pcbTable.lookUpPCB(pid)#variable estetica
        pcb.set_status("terminated")
        self._dispatcher.pcOsioso()
        self._loader.liberarMemoria(pcb.get_bd, pcb.get_limit) 
        self._pcbTable.removePCB(pid) 
        self._Scheduler.siguienteRunning()