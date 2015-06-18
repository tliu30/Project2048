from numpy.random import binomial

def coinFlip(p):
    flip  = binomial(1, p, 1)
    return (flip == 1)

class LimSizeArray:
    
    def __init__(self, maxSize):
        self.maxSize = maxSize
        self.array   = [None for i in range(maxSize)]
        self.curIx   = 0
        self.full    = False
        
    def add(self, item):
        ix = self.curIx % self.maxSize
        self.array[ix] = item
        self.curIx = self.curIx + 1
        return None
        
    def length(self):
        if self.full:
            length = self.maxSize
        else:
            length = self.curIx
        return length
        
class MemorySnapshot:
    
    def __init__(self, curState, action, reward, nextState):
        self.curState  = curState
        self.action    = action
        self.reward    = reward
        self.nextState = nextState
 
