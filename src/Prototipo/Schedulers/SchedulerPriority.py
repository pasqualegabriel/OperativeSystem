#!/usr/bin/env python
# -*- coding: utf-8 -*-s

from Prototipo.Schedulers.queues import *
from Prototipo.Schedulers.scheduler import Scheduler

class SchedulerPriorityPreemptive(Scheduler):
    def __init__(self, pcbTable):
        self._priority = {1: QueueFIFO(), 2: QueueFIFO(), 3: QueueFIFO(), 4: QueueFIFO(), 5: QueueFIFO()}
        self._accountant = 0
        self._PCBTable = pcbTable


    def update(self):
        self._aging = int(input("Aging?\n"))

    def add(self, pcb):
        tupleWithPidAndWaitingTime = (pcb.get_pid(), self._accountant + self._aging)
        self._priority.get(pcb.get_priority()).add(tupleWithPidAndWaitingTime)

    def pop(self):
        self._accountant += 1
        self.updatePriorities()
        for priority, queue in self._priority.items():
            if queue.notIsEmpty():
               return queue.pop()[0]

    def isChange(self, pcbInCPU, newPCB):
        return newPCB.get_priority() < pcbInCPU.get_priority()

    def updatePriorities(self):
        for priority, queue in self._priority.items():
            if queue.notIsEmpty() and (priority != 1 and self._accountant >= queue.head()[1]):
            	newPriority = priority - 1
            	pid = queue.pop()[0]
            	waitingTime = self._accountant + self._aging
            	pcb = self._PCBTable.lookUpPCB(pid)
            	self.add(pcb)
            	pcb.set_priority(newPriority)

    def notIsEmpty(self):
        for key, valor in self._priority.items():
            if (valor.notIsEmpty()):
                return True
        return False

    def list(self):
        res = []
        for priority, queue in self._priority.items():
            for q in queue.list():
                res.append(q[0])
        return res

    def isPreemptive(self):
        return True



class SchedulerPriorityNonPreemptive(SchedulerPriorityPreemptive):
    def isPreemptive(self):
        return False

'''
class SchedulerPriorityPreemptive(Scheduler):
    def __init__(self, pcbTable, aging):
        self._priority = {1: QueuePriority(), 2: QueuePriority(), 3: QueuePriority()}
        self._accountant = 0
        self._aging = aging
        self._PCBTable = pcbTable

    def add(self, pid, priority, burst):
        waitingTime=self._accountant + self._aging
        self._priority.get(priority).add(pid,waitingTime)

    def pop(self):
        self._accountant += 1
        self.timeOut()
        for key, valor in self._priority.items():
            if valor.notIsEmpty():
               return valor.pop()

    def isChange(self, pcbInCPU, newPCB):
        return newPCB.get_priority() < pcbInCPU.get_priority()

    def isSchedulerPriority(self):
        return True

    def isTimeOut(self, waitingTime):
        return self._accountant >= waitingTime

    def get_aging(self):
        return self._aging

    def timeOut(self):
        for key, valor in self._priority.items():
            if valor.notIsEmpty():
                if key != 1 and self.isTimeOut(valor.get_WaitingTimeForTheHead()):
                    priority = key - 1
                    pid = valor.pop()
                    self.add(pid, priority,None)
                    pcb = self._PCBTable.lookUpPCB(pid)
                    pcb.set_priority(priority)

    def notIsEmpty(self):
        for key, valor in self._priority.items():
            if (valor.notIsEmpty()):
                return True
        return False

    def isPreemptive(self):
        return True
        
        

############ SchedulerPriorityPreemptive by gabriel version 1 ########################################

#!/usr/bin/env python
# -*- coding: utf-8 -*-s

from Prototipo.Schedulers.queues import *
from Prototipo.Schedulers.scheduler import Scheduler

class SchedulerPriorityPreemptive(Scheduler):
    def __init__(self, pcbTable, aging):
        self._priority = {1: QueueFIFO(), 2: QueueFIFO(), 3: QueueFIFO()}
        self._accountant = 0
        self._aging = aging
        self._PCBTable = pcbTable

    def add(self, pid, priority, burst):
        tupleWithPidAndWaitingTime = (pid, self._accountant + self._aging)
        self._priority.get(priority).add(tupleWithPidAndWaitingTime)

    def pop(self):
        self._accountant += 1
        self.updatePriorities()
        for priority, queue in self._priority.items():
            if queue.notIsEmpty():
               return queue.pop()[0]

    def isChange(self, pcbInCPU, newPCB):
        return newPCB.get_priority() < pcbInCPU.get_priority()

    def updatePriorities(self):
        for priority, queue in self._priority.items():
            if queue.notIsEmpty() and (priority != 1 and self._accountant >= queue.head()[1]):
            	newPriority = priority - 1
            	pid = queue.pop()[0]
            	waitingTime = self._accountant + self._aging
            	self.add(pid, newPriority, None)
            	pcb = self._PCBTable.lookUpPCB(pid)
            	pcb.set_priority(newPriority)

    def notIsEmpty(self):
        for key, valor in self._priority.items():
            if (valor.notIsEmpty()):
                return True
        return False

    def isPreemptive(self):
        return True

############# recibiendo PCBs y encolando PIDs ###############################################
#!/usr/bin/env python
# -*- coding: utf-8 -*-s

from Prototipo.Schedulers.queues import *
from Prototipo.Schedulers.scheduler import Scheduler

class SchedulerPriorityPreemptive(Scheduler):
    def __init__(self, pcbTable, aging):
        self._priority = {1: QueueFIFO(), 2: QueueFIFO(), 3: QueueFIFO()}
        self._accountant = 0
        self._aging = aging
        self._PCBTable = pcbTable

    def add(self, pcb):
        tupleWithPidAndWaitingTime = (pcb.get_pid(), self._accountant + self._aging)
        self._priority.get(pcb.get_priority()).add(tupleWithPidAndWaitingTime)

    def pop(self):
        self._accountant += 1
        self.updatePriorities()
        for priority, queue in self._priority.items():
            if queue.notIsEmpty():
               return queue.pop()[0]

    def isChange(self, pcbInCPU, newPCB):
        return newPCB.get_priority() < pcbInCPU.get_priority()

    def updatePriorities(self):
        for priority, queue in self._priority.items():
            if queue.notIsEmpty() and (priority != 1 and self._accountant >= queue.head()[1]):
            	newPriority = priority - 1
            	pid = queue.pop()[0]
            	waitingTime = self._accountant + self._aging
            	pcb = self._PCBTable.lookUpPCB(pid)
            	self.add(pcb)
            	pcb.set_priority(newPriority)

    def notIsEmpty(self):
        for key, valor in self._priority.items():
            if (valor.notIsEmpty()):
                return True
        return False

    def isPreemptive(self):
        return True


################  encolando PCBs, sin que el scheduler conozca al pcb table ##########
#!/usr/bin/env python
# -*- coding: utf-8 -*-s

from Prototipo.Schedulers.queues import *
from Prototipo.Schedulers.scheduler import Scheduler

class SchedulerPriorityPreemptive(Scheduler):
    def __init__(self, pcbTable, aging):
        self._priority = {1: QueueFIFO(), 2: QueueFIFO(), 3: QueueFIFO()}
        self._accountant = 0
        self._aging = aging
        self._PCBTable = pcbTable

    def add(self, pcb):
        tupleWithPidAndWaitingTime = (pcb, self._accountant + self._aging)
        self._priority.get(pcb.get_priority()).add(tupleWithPidAndWaitingTime)

    def pop(self):
        self._accountant += 1
        self.updatePriorities()
        for priority, queue in self._priority.items():
            if queue.notIsEmpty():
               return queue.pop()[0].get_pid()

    def isChange(self, pcbInCPU, newPCB):
        return newPCB.get_priority() < pcbInCPU.get_priority()

    def updatePriorities(self):
        for priority, queue in self._priority.items():
            if queue.notIsEmpty() and (priority != 1 and self._accountant >= queue.head()[1]):
            	newPriority = priority - 1
            	pcb = queue.pop()[0]
            	waitingTime = self._accountant + self._aging
            	pcb.set_priority(newPriority)
            	self.add(pcb)


    def notIsEmpty(self):
        for key, valor in self._priority.items():
            if (valor.notIsEmpty()):
                return True
        return False

    def isPreemptive(self):
        return True
'''
