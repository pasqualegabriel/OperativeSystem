#!/usr/bin/env python
# -*- coding: utf-8 -*-s
from Prototipo.Schedulers.SchedulersFactory import *
from Prototipo.memoryFactory import MemoryFactory
from Prototipo.memoryManagerContinuousAssignment import *
from Prototipo.swap import Swap
from Prototipo.newProgram import NewPrograms
from Prototipo.clock import Clock
from Prototipo.cpu import Cpu
from Prototipo.deviceManager import DeviceManager
from Prototipo.dispatcher import Dispatcher
from Prototipo.intManager import *
from Prototipo.loader import *
from Prototipo.memory import *
from Prototipo.memoryManagerPaging import *
from Prototipo.mmu import *
from Prototipo.pcbTable import PCBTable
from Prototipo.print import *

class Kernel:
    def __init__(self, disco):
        self._disco            = disco
        self._pcbTable         = PCBTable()
        self._schedulerFactory = SchedulersFactory(self._pcbTable)
        self._scheduler        = self._schedulerFactory.getScheduler()
        self._intManager       = IntManager()
        self._memoryFactory    = MemoryFactory(self._pcbTable, self._intManager, disco)
        self._memory           = self._memoryFactory.getMemory()
        self._memoryManager    = self._memoryFactory.getMemoryManager()
        self._mmu              = self._memoryFactory.getMmu()
        self._loader           = self._memoryFactory.getLoader()
        self._timer            = self._schedulerFactory.getTimer(self._intManager)
        self._cpu              = Cpu(self._mmu, self._intManager)
        self._dispatcher       = Dispatcher(self._mmu, self._cpu)
        self._deviceManager    = DeviceManager(self._intManager)
        self._intManager.setInterruptions(self._loader, self._dispatcher, self._scheduler, self._pcbTable, self._deviceManager, self._memoryManager, self._timer)
        self._newPrograms      = NewPrograms(self._intManager)
        self._clock            = Clock(self._cpu, self._deviceManager, self._timer, self._newPrograms)


    #Proposito:
    #Precondicion:
    def initialize(self, programs, log):
        # Imprime la memoria y el memoryManager, y setea para porteriores impresiones
        self._waitTimeAndAverageReturn = WaitTimeAndAverageReturn()
        log.set(self._memoryManager, self._memory, self._dispatcher, self._intManager, self._pcbTable, self._scheduler, self._waitTimeAndAverageReturn)
        self._newPrograms.setPrograms(programs, self._waitTimeAndAverageReturn)
        # Comienza a correr el clock
        self._clock.runCpu(log)
        log.printWaitTimeAndAverageReturn()


class KernelSchedulerRoundRobinQuantum3MemoryPagingSize8SecondChancePageReplacementAlgorithm(Kernel):
    def __init__(self, disco):
        self._disco = disco
        self._memory = Memory(8)
        self._pcbTable = PCBTable()
        self._intManager = IntManager()
        sizeFrame = 4
        pageReplacementAlgorithm = SecondChancePageReplacementAlgorithm()
        self._swap = Swap(sizeFrame)
        self._memoryManager = MemoryManagerPaging(self._memory, sizeFrame, self._pcbTable, self._swap, pageReplacementAlgorithm)
        self._mmu = MmuPages(self._memory, sizeFrame, self._intManager)
        self._loader = LoaderPages(self._memory, self._mmu, self._disco, self._memoryManager, self._swap)
        self._memoryManager.setLoader(self._loader)  # Es para no hacer la interrupcion swapIN (el memoryManager y el loader se conocen mutuamente)
        self._scheduler = SchedulerFCFS()
        self._timer = Timer(self._intManager, 3)
        self._cpu = Cpu(self._mmu, self._intManager)
        self._dispatcher = Dispatcher(self._mmu, self._cpu)
        self._deviceManager = DeviceManager(self._intManager)
        self._intManager.setInterruptions(self._loader, self._dispatcher, self._scheduler, self._pcbTable, self._deviceManager, self._memoryManager, self._timer)
        self._newPrograms = NewPrograms(self._intManager)
        self._clock = Clock(self._cpu, self._deviceManager, self._timer, self._newPrograms)

class KernelSchedulerPriorityMemoryPagingSize8ClockPageReplacementAlgorithm(Kernel):
    def __init__(self, disco):
        self._disco = disco
        self._memory = Memory(8)
        self._pcbTable = PCBTable()
        self._intManager = IntManager()
        sizeFrame = 4
        pageReplacementAlgorithm = SecondChancePageReplacementAlgorithm()
        self._swap = Swap(sizeFrame)
        self._memoryManager = MemoryManagerPaging(self._memory, sizeFrame, self._pcbTable, self._swap, pageReplacementAlgorithm)
        self._mmu = MmuPages(self._memory, sizeFrame, self._intManager)
        self._loader = LoaderPages(self._memory, self._mmu, self._disco, self._memoryManager, self._swap)
        self._memoryManager.setLoader(self._loader)  # Es para no hacer la interrupcion swapIN (el memoryManager y el loader se conocen mutuamente)
        self._scheduler = SchedulerPriorityPreemptive(self._pcbTable, 80)
        self._timer = None
        self._cpu = Cpu(self._mmu, self._intManager)
        self._dispatcher = Dispatcher(self._mmu, self._cpu)
        self._deviceManager = DeviceManager(self._intManager)
        self._intManager.setInterruptions(self._loader, self._dispatcher, self._scheduler, self._pcbTable, self._deviceManager, self._memoryManager, self._timer)
        self._newPrograms = NewPrograms(self._intManager)
        self._clock = Clock(self._cpu, self._deviceManager, self._timer, self._newPrograms)

class KernelSchedulerSJFMemoryContinuousAssignmentBestFitSize32(Kernel):
    def __init__(self, disco):
        self._disco = disco
        self._memory = Memory(32)
        self._pcbTable = PCBTable()
        self._intManager = IntManager()
        self._memoryManager = MemoryManagerContinuousAssignmentBestFit(self._memory, self._pcbTable, self._intManager, 1)
        self._mmu = Mmu(self._memory)
        self._loader = LoaderBlocks(self._memory, self._mmu, disco, self._memoryManager)
        self._scheduler = SchedulerSJFPreemptive()
        self._timer = None
        self._cpu = Cpu(self._mmu, self._intManager)
        self._dispatcher = Dispatcher(self._mmu, self._cpu)
        self._deviceManager = DeviceManager(self._intManager)
        self._intManager.setInterruptions(self._loader, self._dispatcher, self._scheduler, self._pcbTable, self._deviceManager, self._memoryManager, self._timer)
        self._newPrograms = NewPrograms(self._intManager)
        self._clock = Clock(self._cpu, self._deviceManager, self._timer, self._newPrograms)

class KernelSchedulerSJFMemoryPagingSize8ClockPageReplacementAlgorithm(Kernel):
    def __init__(self, disco):
        self._disco = disco
        self._memory = Memory(8)
        self._pcbTable = PCBTable()
        self._intManager = IntManager()
        sizeFrame = 4
        pageReplacementAlgorithm = ClockPageReplacementAlgorithm()
        self._swap = Swap(sizeFrame)
        self._memoryManager = MemoryManagerPaging(self._memory, sizeFrame, self._pcbTable, self._swap, pageReplacementAlgorithm)
        self._mmu = MmuPages(self._memory, sizeFrame, self._intManager)
        self._loader = LoaderPages(self._memory, self._mmu, self._disco, self._memoryManager, self._swap)
        self._memoryManager.setLoader(self._loader)  # Es para no hacer la interrupcion swapIN (el memoryManager y el loader se conocen mutuamente)
        self._scheduler = SchedulerSJFPreemptive()
        self._timer = None
        self._cpu = Cpu(self._mmu, self._intManager)
        self._dispatcher = Dispatcher(self._mmu, self._cpu)
        self._deviceManager = DeviceManager(self._intManager)
        self._intManager.setInterruptions(self._loader, self._dispatcher, self._scheduler, self._pcbTable, self._deviceManager, self._memoryManager, self._timer)
        self._newPrograms = NewPrograms(self._intManager)
        self._clock = Clock(self._cpu, self._deviceManager, self._timer, self._newPrograms)

class KernelSchedulerFCFSMemoryPagingSize8FIFOPageReplacementAlgorithm(Kernel):
    def __init__(self, disco):
        self._disco = disco
        self._memory = Memory(8)
        self._pcbTable = PCBTable()
        self._intManager = IntManager()
        sizeFrame = 4
        pageReplacementAlgorithm = FirstInFirstOutPageReplacementAlgorithm()
        self._swap = Swap(sizeFrame)
        self._memoryManager = MemoryManagerPaging(self._memory, sizeFrame, self._pcbTable, self._swap, pageReplacementAlgorithm)
        self._mmu = MmuPages(self._memory, sizeFrame, self._intManager)
        self._loader = LoaderPages(self._memory, self._mmu, self._disco, self._memoryManager, self._swap)
        self._memoryManager.setLoader(self._loader)  # Es para no hacer la interrupcion swapIN (el memoryManager y el loader se conocen mutuamente)
        self._scheduler = SchedulerFCFS()
        self._timer = None
        self._cpu = Cpu(self._mmu, self._intManager)
        self._dispatcher = Dispatcher(self._mmu, self._cpu)
        self._deviceManager = DeviceManager(self._intManager)
        self._intManager.setInterruptions(self._loader, self._dispatcher, self._scheduler, self._pcbTable, self._deviceManager, self._memoryManager, self._timer)
        self._newPrograms = NewPrograms(self._intManager)
        self._clock = Clock(self._cpu, self._deviceManager, self._timer, self._newPrograms)

class KernelFactoty:
    def __init__(self, disco):
        self._idKernel = int(input("Choise Kernel: \n1 Memory: Continuous Assignment Best Fit,                    SizeMemory = 32, Scheduler: Shortest Job First\n"
                                   "2 Memory: Paging, Page Replacement Algorithm: FIFO,          SizeMemory =  8, Scheduler: First Come First Served\n"
                                   "3 Memory: Paging, Page Replacement Algorithm: Second Chance, SizeMemory =  8, Scheduler: Round Robin, Quantum = 3\n"
                                   "4 Memory: Paging, Page Replacement Algorithm: Clock,         SizeMemory =  8, Scheduler: Priority\n"
                                   "5 Memory: Paging, Page Replacement Algorithm: Clock,         SizeMemory =  8, Scheduler: Shortest Job First \n"
                                   "6 Configure\n"))
        if self._idKernel == 6:
            self._kernelConfiguration = Kernel(disco)
        else:
            self._kernelConfiguration = None
        self._kernel = {1: KernelSchedulerSJFMemoryContinuousAssignmentBestFitSize32(disco),
                        2: KernelSchedulerFCFSMemoryPagingSize8FIFOPageReplacementAlgorithm(disco),
                        3: KernelSchedulerRoundRobinQuantum3MemoryPagingSize8SecondChancePageReplacementAlgorithm(disco),
                        4: KernelSchedulerPriorityMemoryPagingSize8ClockPageReplacementAlgorithm(disco),
                        5: KernelSchedulerSJFMemoryPagingSize8ClockPageReplacementAlgorithm(disco),
                        6: self._kernelConfiguration}

    def initialize(self):
        return self._kernel.get(self._idKernel)
