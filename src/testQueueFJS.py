import unittest

from Prototipo.Schedulers.queues import QueueSJF


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self._queue = QueueSJF()
        self._queue.add(0, 5)
        self._queue.add(1, 2)
        self._queue.add(2, 7)

    def test0001TheFirstPidWhenPopIs1(self):
        self.assertEqual(1, self._queue.pop())

    def test0002TheSecondPidWhenPopIs0(self):
        self._queue.pop()
        pid2Test = self._queue.pop()
        self.assertEqual(0, pid2Test)

if __name__ == '__main__':
    unittest.main()
