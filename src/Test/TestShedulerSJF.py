import unittest

from SistemaDeProcedimientos.pcb import PCB
from SistemaDeScheduler.scheduler import *


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self._PCBTest=PCB(0)
        self._PCBTest.set_bursts([1,2])
        self._shedulerTest=SchedulerSJF()
        self._shedulerTest.add(0, 1, 5)
        self._shedulerTest.add(1, 1, 2)
        self._shedulerTest.set_burstPCBInCPU(2)



    def test0000TheIncomingBurstIsGreaterThanBurstInCPU(self):
        burst=self._PCBTest.get_headBurst()
        self.assertTrue(self._shedulerTest.isMinBurst(burst))


if __name__ == '__main__':
    unittest.main()
