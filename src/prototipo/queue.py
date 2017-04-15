# Represeta a una Queue, con colaborador interno items
class Queue:
    def __init__(self):
        # Crea una cola vacía.
        # La cola vacía se representa por una lista vacía
        self.items=[]
        self._len=0
    #Proposito: agrega elementos a la cola
    #Precondiccion:-
    def encolar(self, x):
        # Agrega el elemento x como último de la cola. 
        self.items.append(x)
        self._len+=1
    
    #Proposito:Elimina el primer elemento de la cola y devuelve su valor. Si la cola está vacía, 
    #  levanta ValueError
    #Precondiccion:-
    def desencolar(self):

        try:
            self._len-=1
            return self.items.pop(0)
                
        except:
            raise ValueError("La cola está vacía")
    
    #Proposito: Devuelve True si la cola esta vacía, False si no.
    #Precondiccion:-
    def es_vacia(self):
        return self.items == []

    #Proposito: Devuelve la longitud de la Queue
    #Precondiccion:-
    def lenQ(self):
        return self._len