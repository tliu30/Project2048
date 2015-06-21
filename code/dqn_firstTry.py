import theanets
from utils import coinFlip, LimSizeArray, MemorySnapshot
from Game import Game
from Game import CONST_LEFT, CONST_RIGHT, CONST_UP, CONST_DOWN
import numpy as np
from numpy.random import choice
     
class DeepQNet:
    
    def __init__(self, game, architecture, trainControl, (initLearningRate, decay, minLearningRate) = (1, 0.000001, 0.1), sizeMemory = 1000000):
        self.net   = theanets.Experiment(theanets.Regressor, layers = architecture)
        self.trainControl = trainControl

        self.learningRate = initLearningRate
        self.decay = decay
        self.minLearningRate = minLearningRate

        self.game = game
        self.memory = LimSizeArray(sizeMemory)
        
        self.game.initialize()

    # The main functions
    def train(self, iterations, miniBatchSize, printInterval = 1):
        for i in range(iterations):
            #for z in range(32):
            self.step()
            self.learn(miniBatchSize)
            
            if i % printInterval == 0:
                print i

    def play(self, game):
        state  = game.getState()
        action = self.optimalAction(state)
        return action

    # Functions for referencing board

    def getState(self):
        return self.game.getState()

    def doAction(self, action):
        self.game.makeMove(action)

    # Functions for computing values
    
    def getValue(self, state, action):
        return self.getAllValues(state)[action]
 
    def optimalAction(self, state):
        return np.argmax(self.getAllValues(state))
       
    def optimalValue(self, state):
        return max(self.getAllValues(state))

    def getAllValues(self, state):
        return self.net.network.predict(state).tolist()[0] # Limit by possible moves?

    # Control learning rate

    def updateLearningRate():
        if self.learningRate > self.minLearningRate:
            self.learningRate = self.learningRate - self.decay
        else:
            pass
        return None
        
    # Reward
    def calcReward(self, oldState, newState):
        return np.square(newState).sum() - np.square(oldState).sum()

    # Choose the next action & examine result
    
    def step(self):
        # Reset game if over
        if self.game.isOver() or self.game.possibleMoves == []:
            self.game.reset()
            self.game.initialize()
            
        oldState = self.getState()
        action   = self.chooseAction()
        self.doAction(action)
        newState = self.getState()
        reward   = self.calcReward(oldState, newState)
        
        details  = MemorySnapshot(oldState, action, reward, newState)
        
        self.addToMemory(details)

        # Reset game if over
        if self.game.isOver():
            self.game.reset()
            self.game.initialize()

    def chooseAction(self):
        heads = coinFlip(self.learningRate)
        if heads:
            action = self.randomAction()
        else:
            action = self.optimalAction(self.getState())
           
        return action
        
    def randomAction(self):
        return choice(self.game.possibleMoves, size = 1)[0]
           
    # Do learning on the minibatches

    def learn(self, miniBatchSize):
        samples   = self.getRandomSamplesFromMemory(miniBatchSize)
        curValues = [self.getAllValues(sample.curState) for sample in samples]
        curStates = [sample.curState.tolist()[0] for sample in samples]

        optValues = [
            sample.reward + np.array(self.getAllValues(sample.nextState))
            for sample in samples
        ]
        #optValues = [sample.reward + self.optimalValue(sample.nextState) for sample in samples]
        #optActions= [self.optimalAction(sample.nextState) for sample in samples]
        
        #correctedValues = [curValues[i][:optActions[i]] + [optValues[i]] + curValues[i][(optActions[i]+1):] for i in range(miniBatchSize)]

        x = np.array(curStates)
        y = np.array(optValues)
        
        #print x.shape, y.shape
        
        train = x,y
        valid = x,y
        
        self.net.train(train, valid, **self.trainControl)
        return None

    # Actions on memory
        
    def addToMemory(self, item):
        self.memory.add(item)
        return None
        
    def getFromMemory(self, ix):
        return self.memory.get(ix)
    
    def getRandomSamplesFromMemory(self, miniBatchSize):
        numSamples = min(miniBatchSize, self.memory.length())
        ixs = choice(range(self.memory.length()), size = numSamples, replace = False)
        miniBatch = [self.memory.get(ix) for ix in ixs]
        
        return miniBatch

if __name__ == "__main__":
    b = Game(4)
    a = DeepQNet(b, (16,4), {"algorithm" : "sgd", "learning_rate" : 1e-4, "momentum" : 0.9}, (1, 0.00001, 0.1))
    for i in range(200): a.step()
    a.train(300, 32)
    
    #a.getState()
    #print(a.getValue(a.getState(), CONST_UP))
    #a.getAllValues(a.getState())
    #a.getFromMemory(0)
    #for i in range(200): a.step()
    #
    #a.getFromMemory(1).curState
    #a.getFromMemory(1).action
    #a.getFromMemory(1).reward
    #a.getFromMemory(1).nextState
    
    #a.learn(10)

def test(net):
    game = Game(4)
    game.initialize()
    while not game.isOver():
        action = net.optimalAction(game.getState())
        game.makeMove(action)
        print game
        
test(a)
