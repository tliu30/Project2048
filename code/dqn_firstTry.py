import theanets
from utils import coinFlip, LimSizeArray, MemorySnapshot
from 2048 import Game as Board
from numpy.random import choice
      
class DeepQNet:
    
    def __init__(self, architecture):
        self.net   = theanets.Experiment(theanets.Regressor, architecture)
        self.trainControl = trainControl

        self.learningRate = initLearningRate
        self.decay = decay
        self.minLearningRate = minLearningRate

        self.time = 1

        self.board = Board(4)
        self.memory = LimSizeArray(sizeMemory)

    # Functions for referencing board

    def getState(self):
        return self.board.array

    def doAction(self, action):
        if action == LEFT:
            self.board.moveLeft()
        elif action == RIGHT
            self.board.moveRight()
        elif action == UP:
            self.board.moveUp()
        elif action == down:
            self.board.moveDown()
        else:
            raise ValueError

    # Functions for computing values
    
    def getValue(state, action):
        return getAllValues(state)[action]
 
    def optimalAction(self, state):
        return argmax(getAllValues(state))
       
    def optimalValue(self, state):
        return max(getAllValues(state))

    def getAllValues(state):
        return self.net.predict(state)

    # Control learning rate

    def updateLearningRate():
        if self.learningRate > self.minLearningRate:
            self.learningRate = self.learningRate - self.decay
        else:
            pass
        return None

    # Choose the next action & examine result
    
    def step(self):
        oldState = self.getState()
        action   = self.chooseAction()
        reward   = self.doAction(action)
        newState = self.getState()
        
        details  = MemorySnap(oldState, action, reward, newState)
        
        self.addToMemory(details)
        return None
    
    def chooseAction(self):
        heads = coinFlip(self.learningRate)
        if heads:
            action = self.randomAction()
        else:
            action = self.optimalAction(self.getState())
           
        return action
        
    def randomAction(self):
        return choice(ALL_ACTIONS, size = 1)
           
    # Do learning on the minibatches

    def learn(self, miniBatchSize):
        samples   = self.getRandomSamplesFromMemory(miniBatchSize)
        curValues = [sample.getValue(sample.curState, sample.action) for sample in samples]
        optValues = [sample.reward + self.optimalValue(sample.nextState) for sample in samples]
        
        x = curValues
        y = optValues
        
        self.net.train(x, y, self.trainControl)
        return None

    # Actions on memory
        
    def addToMemory(self, item):
        self.memory.add(item)
        return None
        
    def getFromMemory(self, ix):
        return self.memory.get(ix)
    
    def getRandomSampleFromMemory(self, miniBatchSize):
        numSamples = min(miniBatchSize, self.memory.length())
        ixs = choice(range(self.memory.length()), size = numSamples, replace = False)
        miniBatch = [self.memory.get(ix) for ix in ixs]
        
        return miniBatch
