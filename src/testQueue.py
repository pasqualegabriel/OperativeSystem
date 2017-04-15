import unittest
from prototipo.queue import Queue

# Queue con 4 elementos q=[0,1,2,3]
q=Queue()
for i in range(4):
    q.encolar(i)

class testerQueue(unittest.TestCase):
	# la longitud de q es 4
    def test_1(self):
        self.assertEqual(4, q.lenQ())

    # q no es vacia
    def test_2(self):
        self.assertEqual(False, q.es_vacia())
    
    # el primer elemento a desencolar de q es 0
    # y la longitud ahora es de 3 
    def test_3(self):
        self.assertEqual(0, q.desencolar())
        self.assertEqual(3, q.lenQ())

if __name__ == "__main__":
    unittest.main()