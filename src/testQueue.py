import unittest

from Prototipo.Schedulers.queues import QueuePriority

q = QueuePriority()
q.add(1, 2)
q.add(2, 3)


class testerQueue(unittest.TestCase):
    def test_1(self):
        self.assertEqual(2, q.lenItems())

    def test_4(self):
        q.insert(0, 0)
        self.assertEqual(0, q.pop())
        self.assertEqual(2, q.lenItems())
        self.assertEqual(1, q.pop())
        self.assertEqual(1, q.lenItems())
        self.assertEqual(2, q.pop())


if __name__ == "__main__":
    unittest.main()
