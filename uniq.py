registry = {}
class Data:
    def __repr__(self): return str(self.val)
    def __init__(self,V):
        # lookup for existant object
        if V in registry: self = registry[V] 
        else:
            self.val = V
            registry[V] = self # register created object
            
print registry,Data(0)
print registry,Data(0)
print registry,Data(1)
print registry,Data(1)
