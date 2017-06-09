import unittest

from Prototipo.Schedulers.queues import QueueSJF


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self._queue = QueueSJF()
        self._queue.add(0,5)
        self._queue.add(1,2)

    def test0000TheMinBustIs2(self):
            self.assertEqual(1,self._queue.pop())


    def test0001TheMinBUstIs5(self):
            self._queue.pop()
            self.assertEqual(5,self._queue.get_minBurst())

    def test0002TheFirstPidWhenPopIs1(self):
        pid1Test= self._queue.pop()
        self.assertEqual(1,pid1Test)


    def test0003TheFirstPidWhenPopIs0(self):
        self._queue.pop()
        pid2Test = self._queue.pop()
        self.assertEqual(0,pid2Test)

if __name__ == '__main__':
    unittest.main()
