#!/usr/bin/env python
# -*- coding: utf-8 -*-s
from tabulate import tabulate
from time import sleep
import logging


# Clase instruccion
# colaborador interno count
class Instr():
    def __init__(self, count):
        self._count = count

# Retorna False
    def isExit(self): 
        return False

# Getter del colaborador interno _count
    @property
    def count(self):
        return self._count

# Crea un array con la cantidad de CPU o IO correspondiente
# Ej: expand(CPU(3)), retorna [CPU,CPU,CPU]
# self.__class crea una array de la clase de instruccion que recibe.
    def expand(self):
        expanded = []
        for _ in range(self._count):
            expanded.append(self.__class__(0))
        return expanded

#CPU, subclase de Instr
class CPU(Instr): 
    def __repr__(self):
        if self._count:
            return "CPU({count})".format(count=self._count) 
            #Retorna un string con el valor del colaborador interno _count
        else:
            return "CPU"

class IO(Instr):
    def __repr__(self):
        if self._count:
            return "IO({count})".format(count=self._count) 
        else:
            return "IO"

class EXIT(Instr):
    def isExit(self): #Modifica el metodo de isExit definido el la superclase Instr, haciendo que retorne True   
        return True
    def __repr__(self):
        return "EXIT"

#Colaboradores internos: _name y _insructions
class Program():
    def __init__(self, name, instructions):
        self._name = name
        self._instructions = self.expand(instructions)

# Getter de _name
    @property
    def name(self):
        return self._name

# Getter de _instructions
    def instructions(self):
        return self._instructions

    def getLista(self):
        return self._instructions

# Ej: expand([CPU(3),IO(2)]) retorna [CPU,CPU,CPU,IO,IO,EXIT]
    def expand(self, instructions):
        expanded = []
        for instr in instructions:
            expanded.extend(instr.expand())
        if not expanded[-1].isExit(): #Si la instruccion final no es EXIT, agrega el Exit.
            expanded.append(EXIT(0))
        return expanded

    def longitud(self):
        l = 0
        for i in self._instructions:
            l += 1
        return l

    def __repr__(self):
        return "Program({name}, {instructions})".format(name=self._name, instructions=self._instructions)


# Representa la Memoria, con colaborador interno memory inicializado con una lista vacia 
# La Memoria se encarga de almacenar las instrucciones de los programas
class Memory():
    def __init__(self):
        self._memory = []

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
    #Precondiccion: Debe existir pos en la memoria 
    def fetch(self, posicion):
        return self._memory[posicion] 

    def __repr__(self):
        return tabulate(enumerate(self._memory), tablefmt='psql') #pretty print. 

# Representa al loader, con colaboradores internos memory, el bd  y limit
# El Loader maneja la memoria
class Loader():
    def __init__(self, memoria):
        self._memory=memoria
        self._bd = 0
        self._limit = (-1)

    #Proposito: carga una lista de intrrucciones en la memoria;guarda el bd y el limit
    #Precondiccion:-
    def cargarInMemory(self, instrucciones):
        self._limit += instrucciones.longitud()
        self._bd += instrucciones.longitud()
        self._memory.load(instrucciones)
    
    #Proposito: retorna el bd
    #Precondiccion: -
    @property
    def get_bd(self):
        return self._bd
    
    #Proposito:retorna el limit
    #Precondiccion:-
    @property
    def get_limit(self):
        return self._limit
    
    #Proposito:setea las posiciones de la memoria del programa y la pone en null
    #Precondiccion: Existen las posiciones en la memoria
    def liberarMemoria(self, bd,limit):
        for i in range(bd,limit+1):
            self._memory.set_pos(i,None)                                                  

# Representa el PCB de un sistema, con colaboradores internos pid, status, pc, bd, limit
# Es el procedimiento que se encarga de guardar el pid
class PCB():
    def __init__(self, pid):
        self._pid=pid
        self._status="new"
        self._pc=0
        self._bd= None #esta en none porque todabia el loader no le asigno el espacio en memoria
        self._limit=None #esta en none porque todabia el loader no le asigno el espacio en memoria

    #Proposito: Setea el bd
    #Precondiccion: -
    def set_bd(self, bd):
        self._bd=bd
    
    #Proposito: setea el limit
    #Precondiccion: --
    def set_limit(self,lm):
        self._limit=lm
    
    #Proposito: Retorna el pid
    #Precondiccion: -
    def get_pid(self):
        return self._pid
    
    #Proposito:setea el status
    #Precondiccion:-
    def set_status(self, status):
        self._status=status
    
    #Proposito: retorna el bd
    #Precondiccion: -
    @property
    def get_bd(self):
        return self._bd
    
    #Proposito: retorna el limit
    #Precondiccion: -
    @property
    def get_limit(self):
        return self._limit

# Representa al PCNTable del sistema, con un colabordor interno map.
# La PCBTable se encarga de almacenar el pid y el pcb de dicho pid.
class PCBTable():
    def __init__(self):
        self._map={}

    #Proposito:Inserta un elemento en el mapa de clave:valor.
    #Precondiccion: la clave no debe existir en el mapa.
    def addPCB(self, pcb):
        self._map[pcb.get_pid()]=pcb
    
    #Proposito:devuelve el valor dado una clave.
    #Precondiccion:debe existir dicha clave.
    def lookUpPCB(self, pid):
        return self._map.get(pid)

    #Proposito:remueve del mapa la clave y valor.
    #Precondiccion:debe existir dicha clave.
    def removePCB(self, pid):
        del self._map[pid]

# Representa al IntManager del sistema
# colaboradores internos nexPid, pcbTable, loader, dispacher y Scheduler
# El IntManager se encarga de iniciar los procedimientos y borrar procedimientos
class IntManager():
    def __init__(self,cpu,memoria,mmu):
        self._nexPid=0
        self._pcbTable=PCBTable()
        self._loader=Loader(memoria)
        self._dispacher=Dispacher(cpu,mmu)
        self._Scheduler=Scheduler(self._dispacher,self._pcbTable)

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
        
        if(self._dispacher.isIdle()):
            self._dispacher.load(pcb)
            
        else:
            self._Scheduler.encolarEnReady(pcb.get_pid())
        
        self._pcbTable.addPCB(pcb)
        self._nexPid+=1
        
    #Proposito: Consigue del dispacher el pid actual del cpu, pide al pcbtable el valor para seteralo,
    #  cambia el status del pcb en terminated, pone al pc del cpu en estado ocioso, libera la memoria
    #  del programa, borra de la pcbtable el pcb, y le pide al Scheduler el siguente pid en ready.
    #Precondiccion: El programa debe estar en el cpu
    def kill(self):
        pid=self._dispacher.get_PidActual()#variable estetica
        pcb=self._pcbTable.lookUpPCB(pid)#variable estetica
        pcb.set_status("terminated")
        self._dispacher.pcOsioso()
        self._loader.liberarMemoria(pcb.get_bd, pcb.get_limit) 
        self._pcbTable.removePCB(pid) 
        self._Scheduler.siguienteRunning()

# Representa al Scheduler del sistema
# Colaboradores internos dispacher, ready, running, waiting, terminated, pcbTable
# El Scheduler se encarga de manejar de ready, running, waiting, terminated y avisa al dispacher
#  el pcb table a ejecutar
class Scheduler():
    def __init__(self,dispacher,pcbTablet):
        self._dispacher=dispacher
        self._ready=Cola()
        self._running=0
        self._waiting=Cola()
        self._terminated=0
        self._pcbTablet=pcbTablet #preguntar
    
    #Proposito:agrega un elemento<pid> a la lista ready
    #Precondiccion:-
    def encolarEnReady(self, pid):
        self._ready.encolar(pid)
    
    #Proposito:agrega un elemento<pid> a la lista wating
    #Precondiccion:-
    def encolarEnWaiting(self, pid):
        self._ready.encolar(pid)
    
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
            self._dispacher.load(pcb)  

# Representa al Dispacher del sistema
# Colaboradores internos cpu, mmu y pid
# El Dispacher se encarga de almacenar el pid actual, cargar en el cpu el estado de los procesos
#  y se encarga de interactuar con el MMU
class Dispacher():
    def __init__(self,cpu,mmu):
        self._cpu = cpu
        self._mmu= mmu
        self._pid=0
        #self._pcDeProgramaEnWaiting=0
    
    #Proposito: retorna verdadero si el cpu esta en estado inactivo
    #Precondiccion:-
    def isIdle(self):
        return self._cpu.get_pc() == -1
    
    #Proposito:-
    #Precondiccion:-    
    def save(self):
        pass 
    
    #Proposito: guarda el pid actual, setea el cpu en 0 su pc, setea el bd y limit en el mmu
    #Precondiccion:que se le mande por parametro el objeto pcb.    
    def load(self, pcb):
        self._pid=pcb.get_pid()
        self._cpu.set_pc(0)  
        self._mmu.set_bd(pcb.get_bd)
        self._mmu.set_limit(pcb.get_limit)
    
    #Proposito: retorna el pid
    #Precondiccion: -
    def get_PidActual(self):
        return self._pid
    
    #Proposito: setea el pc en osiosio
    #Precondiccion:-
    def pcOsioso(self):
        self._cpu.set_pc(-1)

# Representa al MMU del sistema
# Colaboradores internos bd y limit
# El MMU se ecarga de proporcionar al cpu el bd y el limit del proceso actual 
class Mmu():
    def __init__(self):
        self._bd = 0
        self._limit = 0

    #Proposito: retorna el bd
    #Precondiccion: -
    def get_bd(self):
        return self._bd
    
    #Proposito: retorna el limit
    #Precondiccion: -
    def get_limit(self):
        return self._limit
    
    #Proposito: setea el bd
    #Precondiccion: -
    def set_bd(self,bd):
        self._bd=bd
    
    #Proposito: setea el limit
    #Precondiccion: -
    def set_limit(self,limit):
        self._limit=limit

# Representa al Cpu del sistema
# Colaboradores internos memory, pc y ir. 
# La Cpu se encarga de ejecutar los procesos
class Cpu():        
    def __init__(self, mem, mmu):
        self._memory = mem
        self._pc = (-1)
        self._ir = None
        self._mmu = mmu
    
    #Proposito: Llama a los metodos fetch, decode y execute.
    #Precondiccion: -
    def tick(self):
        self._fetch()
        self._decode()
        self._execute()

    #Proposito: Le asigna a ir la insrtuccion traida de la memoria de la direccion del pc
    #  y incrementa el pc en 1.
    #Precondiccion: que exista en memoria.
    def _fetch(self):
        self._ir = self._memory.fetch(self._pc + self._mmu.get_bd())
        self._pc += 1

    #Proposito:-
    #Precondiccion:-
    def _decode(self):
        # el decode no hace nada en este emulador
        pass

    #Proposito:imprime en pantalla.
    #Precondiccion:-
    def _execute(self):
        logger.debug("Exec: {op}, PC={pc}".format(op=self._ir, pc=self._pc))    
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

    #Proposito:imprime en pantalla.
    #Precondiccion:-
    def __repr__(self):
        return "CPU(PC={pc})".format(pc=self._pc)        

# Representa al Kernel
# Colaboradores internos memory, mmu, cpu y intManager
# El Kernel es el encargado de ejecutar los programas
class Kernel():
    def __init__(self):
        self._memory=Memory()
        self._mmu = Mmu()
        self._cpu=Cpu(self._memory, self._mmu) 
        self._intmanager=IntManager(self._cpu,self._memory, self._mmu)
        
    #Proposito: Ejecuta un programa.
    #Precondiccion:-
    def exec(self, prog):
        self._intmanager.new(prog)
        print()#separa la impresion de los programas
        print(prog.name)
        logger.debug(self)
        #por cada instruccion, la cpu ejecuta tick(fetch,decode,execute).
        for _ in prog.instructions():
            self._cpu.tick()
        self._intmanager.kill()
        
    #Proposito: Ejecuta una lista de programas
    #Precondiccion:-
    def execPrograms(self, ps):
        for p in ps:
            self.exec(p)
    
    #Proposito:imprimir en pantalla.
    #Precondiccion:-
    def __repr__(self):
        return "{cpu}\n{mem}".format(cpu=self._cpu, mem=self._memory) 

# Represeta a una Queue, con colaborador interno items
class Cola():
    def __init__(self):
        # Crea una cola vacía.
        # La cola vacía se representa por una lista vacía
        self.items=[]
  
    #Proposito: agrega elementos a la cola
    #Precondiccion:-
    def encolar(self, x):
        # Agrega el elemento x como último de la cola. 
        self.items.append(x)
    
    #Proposito:Elimina el primer elemento de la cola y devuelve su valor. Si la cola está vacía, 
    #  levanta ValueError
    #Precondiccion:-
    def desencolar(self):

        try:
            return self.items.pop(0)
        except:
            raise ValueError("La cola está vacía")
    
    #Proposito: Devuelve True si la cola esta vacía, False si no.
    #Precondiccion:-
    def es_vacia(self):
        return self.items == []

if __name__ == '__main__':
    ## Configure Logger
    logger = logging.getLogger()
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    logger.info('Starting emulator')

    p1 = Program("Pycharm.exe", [CPU(5), CPU(3)])
    p2 = Program("Word.exe", [CPU(3), CPU(2)])
    p3 = Program("Exel.exe", [CPU(1), IO(1)])
    p4 = Program("Text.exe", [CPU(1), IO(1), CPU(1)])
    ls = [p1,p2,p3,p4]
    k = Kernel()
    k.execPrograms(ls)
    



