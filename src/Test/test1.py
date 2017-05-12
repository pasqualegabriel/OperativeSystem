#!/usr/bin/env python
# -*- coding: utf-8 -*-s
import unittest


# Se crea un Scheduler s
# Con 4 elementos en la Queue de ready y waiting,
# el pid 3 en running y el pid 1 en terminated
from SistemaDeProcedimientos.pcb import PCB
from SistemaDeProcedimientos.pcbTable import PCBTable
from SistemaDeScheduler.scheduler import SchedulerPriorityPreventive

pcb1=PCB(0)
pcb2=PCB(1)
pcb3=PCB(2)

pcb1.set_priority(1)
pcb2.set_priority(2)
pcb3.set_priority(3)

pcbTable=PCBTable()
pcbTable.addPCB(pcb1)
pcbTable.addPCB(pcb2)
pcbTable.addPCB(pcb3)

s = SchedulerPriorityPreventive(pcbTable)
s.add(0, 1)#2
s.add(1, 2)#tiempo de espera 3
s.add(2, 3)#timepo de espera 4
#contador=3
    
class tester(unittest.TestCase):
    
    def test_1(self):
        pid=s.pop()
        pid2=s.pop()
        pcbTest1=pcbTable.lookUpPCB(pid2)
        pid3=s.pop()
        pcbTest2=pcbTable.lookUpPCB(pid3)
        self.assertEqual(1,pcbTest1.get_priority())
        self.assertEqual(2,pcbTest2.get_priority())
    
if __name__ == "__main__":
    unittest.main()