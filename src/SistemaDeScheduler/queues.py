from SistemaDeScheduler.Tuple import Tuple


class Queue:
    def __init__(self):
        self._items = []
        self._len = 0

    def notIsEmpty(self):
        return len(self._items) != 0

    def lenItems(self):
        return len(self._items)

    def list(self):
        return self._items

    def insert(self, index, x):
        return self._items.insert(index, x)

class QueueFIFO(Queue):
    def add(self,pid):
        self._items.append(pid)

    def pop(self):
        try:

            return self._items.pop(0)

        except:
            raise ValueError("Queue is None")

class QueuePriority(Queue):
    def add(self, element,time):

        tuple=Tuple(element,time)
        self.set_WaitingTimeForTheHeadInAdd(time)
        self._items.append(tuple)

    def pop(self):

        try:
            element = self._items.pop(0)
            self.set_WaitingTimeForTheHeadInPop()
            return element.get_primer()

        except:
            raise ValueError("Queue is None")

    def set_WaitingTimeForTheHeadInAdd(self,time):
        if not self.notIsEmpty():
            self._WaitingTimeForTheHead = time

    def set_WaitingTimeForTheHeadInPop(self):
        if self.notIsEmpty():
            element=self._items.pop(0)
            self._WaitingTimeForTheHead=element.get_segundo()
            self.insert(0,element)

    def get_WaitingTimeForTheHead(self):
        return self._WaitingTimeForTheHead


class QueueSJF(Queue):
    def add(self,pid,burst):

        self._items.append(Tuple(pid,burst))
        self.ordering()

    def pop(self):

        try:
            element = self._items.pop(0)
            return element.get_primer()

        except:
            raise ValueError("Queue is None")

    def ordering(self):
        for i in range(1, self.lenItems()):
            for j in range(0, self.lenItems() - i):
                if self._items[j].get_segundo() > self._items[j + 1].get_segundo():
                    k = self._items[j + 1]
                    self._items[j + 1] = self._items[j]
                    self._items[j] = k
