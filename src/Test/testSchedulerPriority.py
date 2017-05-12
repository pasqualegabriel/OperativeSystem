import unittest

from SistemaDeScheduler.scheduler import *


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self._shedulerTest=SchedulerPriorityPreventive()
        self._shedulerTest.add(0, 1, 5)
        self._shedulerTest.add(1, 1, 2)



    def test_something(self):
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
