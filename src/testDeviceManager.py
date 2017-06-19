#!/usr/bin/env python
# -*- coding: utf-8 -*-s

import unittest
import mock

from Prototipo.deviceManager import DeviceManager
from Prototipo.instructions import IO_1, IO_2, IO_3


class tester(unittest.TestCase):

    def setUp(self):
        self._io1 = IO_1(1)
        self._io2 = IO_2(1)
        self._io3 = IO_3(1)
        self._deviceManager = DeviceManager(mock.Mock())

    def sizeWaiting(self):
        totalSizeWaiting = 0
        for ioId, queue in self._deviceManager.getWaiting().items():
            totalSizeWaiting += queue.lenItems()
        return totalSizeWaiting

    #en ves de pedir sizewaitin pedir el waintin y aca utilizar el
    def test000ElDeviceManagerHandleaUnIO_1EnUnTick(self):

        self._deviceManager.add(0, self._io1.getId()) # pid = 0
        self._deviceManager.tick() # este tick no cuenta porque pertenece al tick que fue agregado el pid al deviceManager
        self.assertEqual(1, self.sizeWaiting())
        self._deviceManager.tick()
        self.assertEqual(0, self.sizeWaiting())


    def test001ElDeviceManagerHandleaUnIO_2EnDosTicks(self):

        self._deviceManager.tick()
        self._deviceManager.add(0, self._io2.getId()) # pid = 0
        self._deviceManager.tick() # este tick no cuenta porque pertenece al tick que fue agregado el pid al deviceManager
        self._deviceManager.tick()
        self.assertEqual(1, self.sizeWaiting())
        self._deviceManager.tick()
        self.assertEqual(0, self.sizeWaiting())

    def test002ElDeviceManagerHandleaUnIO_3EnTresTicks(self):

        self._deviceManager.tick()
        self._deviceManager.tick()
        self._deviceManager.add(0, self._io3.getId()) # pid = 0
        self._deviceManager.tick() # este tick no cuenta porque pertenece al tick que fue agregado el pid al deviceManager
        self._deviceManager.tick()
        self._deviceManager.tick()
        self.assertEqual(1, self.sizeWaiting())
        self._deviceManager.tick()
        self.assertEqual(0, self.sizeWaiting())

    def test003ElDeviceManagerHandleaUnIo_1IO_2yIO_3EnElMismoTick(self):

        self._deviceManager.tick()
        self._deviceManager.tick()
        self._deviceManager.add(0, self._io3.getId()) # pid = 0
        self._deviceManager.tick() # este tick no cuenta para el pid 0 porque pertenece al tick que fue agregado al deviceManager
        self._deviceManager.add(1, self._io2.getId()) # pid = 1
        self._deviceManager.tick() # este tick no cuenta para el pid 1 porque pertenece al tick que fue agregado al deviceManager
        self._deviceManager.add(2, self._io1.getId()) # pid = 2
        self._deviceManager.tick() # este tick no cuenta para el pid 2 porque pertenece al tick que fue agregado al deviceManager
        self.assertEqual(3, self.sizeWaiting())
        self._deviceManager.tick()
        self.assertEqual(0, self.sizeWaiting())





