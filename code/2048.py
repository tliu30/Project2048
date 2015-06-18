import random
import math

CONST_UP = 0
CONST_RIGHT = 1
CONST_DOWN = 2
CONST_LEFT = 3

def main():
    g = Game(4)
    #g.play()
    g.initialize()
    player = AI()
    player.solveGame(g, output = True)
    #player.findBestEnergyParam()

class AI:
    def __init__(self, energy_param = .12):
        self.energy_param = energy_param

    def rewardFunction(self, grid):
        if type(grid) == type(Game(0)):
            grid = grid.array
        return  AI.decayingSum(grid) - self.energy_param*AI.energy(grid) 

        #uses reward function, (returns final board, max value on board)
    def solveGame(self, board, depth = 2, output = True):
        
        games = [] #list of strings of grids

        outcomes = {"energy" : [], "reward" : [], "energy / sum" : []} #records the change in these over time
        move_count = 0
        masterOptions = [CONST_UP,CONST_RIGHT, CONST_DOWN, CONST_LEFT]


        options = masterOptions[:]
        while len(options) > 0:
            move_count += 1

            if move_count % 100 == 0 and output:
                print(move_count)

            move = self.exploreToDepth(board.array, depth)[1]

            if move == CONST_UP:
                move_made = board.moveUp()
                move_str = 'Up'
            elif move == CONST_RIGHT:
                move_made = board.moveRight()
                move_str = 'Right'
            elif move == CONST_DOWN:
                move_made = board.moveDown()
                move_str = 'Down'
            elif move == CONST_LEFT:
                move_made = board.moveLeft()
                move_str = 'Left'
            elif move == -1:
                options = []
                move_made = False
            
            if not move_made:
                if move in options:
                    options.remove(move)
            else:
                options = masterOptions[:]
            reward = self.rewardFunction(board)
            outcomes["reward"] += [reward]
            outcomes["energy"] += [AI.energy(board)]
            outcomes["energy / sum"] += [1.*AI.energy(board) / AI.sumValues(board)]
            if output:
                state = str(board)
                games += [state + move_str + ": " + str(reward)[:5]]
        if output:
            print(combine(games))
            #print(outcomes)

        return (AI.maxValue(board), move_count)



    def exploreToDepth(self, grid, depth): #returns (average value of best move, best move)
        if type(grid) == type(Game(0)):
            grid = grid.array

        if depth == 0:
            return (self.rewardFunction(grid), -1)
        else:
            n = (depth + 2)
            options = list(range(4))
            values = []
            spawn = depth > 1
            for move in options[:]:
                cum_reward = 0
                remove = False
                for i in range(n):
                    if move == CONST_UP: #up
                        new_grid, changed = Game.shiftUp(grid, spawn)
                    elif move == CONST_RIGHT:#right
                        new_grid, changed = Game.shiftRight(grid, spawn)
                    elif move == CONST_DOWN:#down
                        new_grid, changed = Game.shiftDown(grid, spawn)
                    else:#left
                        new_grid, changed = Game.shiftLeft(grid, spawn)
                    if changed:
                        cum_reward += self.exploreToDepth(new_grid, depth -1)[0]
                    else:
                        remove = True
                if remove:
                    options.remove(move)
                else:
                    values += [1. * cum_reward / n]
            if len(options) == 0:
                return (-1, -1)
            else:
                return (max(values), options[values.index(max(values))])


    #random selection, no return value
    def randomExploreGame(self, g, output = True):
        games = []
        outcomes = {"energy" : [], "reward" : [], "energy / sum" : []} #records the change in these over time
        i = 0
        options = [CONST_UP, CONST_RIGHT, CONST_LEFT]
        while len(options) > 0:
            i += 1
            if i % 100 == 0:
                print(i)
            move = options[random.randint(0, len(options)-1)]
            if move == CONST_UP:
                move_made = g.moveUp()
                move_str = 'Up'
            elif move == CONST_RIGHT:
                move_made = g.moveRight()
                move_str = 'Right'
            elif move == CONST_DOWN:
                move_made = g.moveDown()
                move_str = 'Down'
            else:
                move_made = g.moveLeft()
                move_str = 'Left'
            if not move_made:
                options.remove(move)
            else:
                options = [CONST_UP, CONST_RIGHT, CONST_LEFT]
            reward = self.rewardFunction(g)
            outcomes["reward"] += [reward]
            outcomes["energy"] += [AI.energy(g.array)]
            outcomes["energy / sum"] += [AI.energy(g.array) / AI.sumValues(g.array)]
            if output:
                state = str(g)
                games += [state + move_str + ": " + str(reward)[:5]]
        if output:
            print(combine(games))
            #print(outcomes)

    @staticmethod
    def maxValue(grid):
        if type(grid) == type(Game(0)):
            grid = grid.array
        return max([max(x) for x in grid])

    @staticmethod
    def sumValues(grid):
        if type(grid) == type(Game(0)):
            grid = grid.array
        return sum([sum(x) for x in grid])

    @staticmethod
    def pctEmpty(grid):
        if type(grid) == type(Game(0)):
            grid = grid.array
        num_empty = sum([x.count(0) for x in grid])
        return 1. * num_empty / len(grid)**2

    @staticmethod
    def distribution(grid):
        dist = {}
        if type(grid) == type(Game(0)):
            grid = grid.array
        for row in grid:
            for entry in row:
                if entry in dist:
                    dist[entry] += 1
                else:
                    dist[entry] = 1
        return dist

    @staticmethod
    def decayingSum(grid):
        if type(grid) == type(Game(0)):
            grid = grid.array
        bigList = []
        for row in grid:
            bigList += row
        bigList.sort()
        result = 0
        n = len(bigList)
        for i in range(n):
            result += (1.* i/(n-1))**2 * bigList[i]

        return result

    @staticmethod
    def energy(grid):
        if type(grid) == type(Game(0)):
            grid = grid.array
        totalEnergy = 0
        for i in range(len(grid)):
            for j in range(len(grid)):
                directions = []
                if j < len(grid) - 1:
                    directions += [abs(grid[i][j+1] - grid[i][j])]
                if i < len(grid) - 1:
                    directions += [abs(grid[i+1][j] - grid[i][j])]
                if j > 0:
                    directions += [abs(grid[i][j] - grid[i][j-1])]
                if i > 0:
                    directions += [abs(grid[i][j] - grid[i-1][j])]
                totalEnergy += sum(directions) #+ min(directions)
        return totalEnergy


    def findBestEnergyParam(self):
        prevAvgMax = -100
        prevSteps = -100
        currentAvgSteps = 0
        currentAvgMax = 0
        eps = .5
        param = .075
        step = +.005
        n = 15
        results = []
        while param < .25:

            self.energy_param = param
            cumMax = 0
            cumSteps = 0
            for i in range(n):
                g = Game(4)
                g.initialize()
                m, steps = self.solveGame(g, False)
                cumMax += m
                cumSteps += steps
            currentAvgMax = cumMax / n
            currentAvgSteps = cumSteps / n
            print(param, step , currentAvgMax, currentAvgSteps)
            results += [(param, currentAvgMax)]

            param += step

        results.sort(key = lambda x: x[1])
        return results[-1][0]


class Game:

    def __init__(self, size):
        self.size = size
        self.array = [[0 for i in range(size)] for i in range(size)]
        self.full = False

    def getCell(self, x, y):
        return self.array[x][y]

    #have to start the game with one tile in it
    def initialize(self):
        x = random.randint(0, self.size-1)
        y = random.randint(0, self.size-1)
        self.array[x][y] = 2

    def copy(self):
        result = Game(self.size)
        result.array = self.array
        result.full = self.full
        return result

    #this might not work anymore
    def play(self):
        self.initialize()
        while not self.full:
            print(self)
            notValid = True
            while notValid:
                move = input("")
                notValid = False
                if move.lower() in ['u', 'up', '2']:
                    self.moveUp()
                elif move.lower() in ['d', 'down', '4']:
                    self.moveDown()
                elif move.lower() in ['r', 'right', '3']:
                    self.moveRight()
                elif move.lower() in ['l','left', '1']:
                    self.moveLeft()
                else:
                    notValid = True
        print(self)

    def moveLeft(self):
        newArray, changed = Game.shiftLeft(self.array, True)
        self.array = newArray
        return changed

    def moveRight(self):
        newArray, changed = Game.shiftRight(self.array, True)
        self.array = newArray
        return changed

    def moveUp(self):
        newArray, changed = Game.shiftUp(self.array, True)
        self.array = newArray
        return changed

    def moveDown(self):
        newArray, changed = Game.shiftDown(self.array, True)
        self.array = newArray
        return changed

    @staticmethod
    def pickRandomEmptyLoc(grid):
        emptyLocs = [(x,y) for x in range(len(grid)) for y in range(len(grid)) if grid[x][y] == 0 ]
        if len(emptyLocs) > 0:
            return emptyLocs[int(random.random()*len(emptyLocs))]
        else:
            return (-1,-1)

    @staticmethod
    def shiftLeft(grid, spawn = True):
        resultArray = []
        size = len(grid)
        for i in range(size):
            row = grid[i]
            reduced_row = []
            for entry in row:
                if not entry == 0:
                    reduced_row += [entry]
            final_row = []
            for j in range(len(reduced_row)):
                if j < len(reduced_row) -1 and reduced_row[j] == reduced_row[j+1]:
                    final_row += [2*reduced_row[j]]
                    reduced_row[j+1] = 0
                elif reduced_row[j] > 0:
                    final_row += [reduced_row[j]]
            
            final_row += [0]*(size-len(final_row))
            resultArray += [final_row]

        changed = not all([all([grid[i][j] == resultArray[i][j] for i in range(size)]) for j in range(size)])


        if spawn and changed:
            spawn_loc = Game.pickRandomEmptyLoc(resultArray)
            if spawn_loc[0] != -1:
                
                rand_double = random.random()
                if rand_double < .9:
                    new = 2
                else:
                    new = 4
                resultArray[spawn_loc[0]][spawn_loc[1]] = new

        return (resultArray, changed)

    @staticmethod
    def shiftRight(grid, spawn = True):
        resultArray = []
        size = len(grid)
        for i in range(size):
            row = grid[i]
            reduced_row = []
            for entry in row:
                if not entry == 0:
                    reduced_row += [entry]
            final_row = []
            reduced_row.reverse()
            for j in range(len(reduced_row)):
                if j < len(reduced_row) -1 and reduced_row[j] == reduced_row[j+1]:
                    final_row += [2*reduced_row[j]]
                    reduced_row[j+1] = 0
                elif reduced_row[j] > 0:
                    final_row += [reduced_row[j]]
            
            final_row += [0]*(size-len(final_row))
            final_row.reverse()
            resultArray += [final_row]

        changed = not all([all([grid[i][j] == resultArray[i][j] for i in range(size)]) for j in range(size)])


        if spawn and changed:
            spawn_loc = Game.pickRandomEmptyLoc(resultArray)
            if spawn_loc[0] != -1:
                
                rand_double = random.random()
                if rand_double < .9:
                    new = 2
                else:
                    new = 4
                resultArray[spawn_loc[0]][spawn_loc[1]] = new

        return (resultArray, changed)

    @staticmethod
    def shiftUp(grid, spawn = True):
        resultArray = []
        size = len(grid)
        for i in range(size):
            col = [grid[x][i] for x in range(size)]
            reduced_col = []
            for entry in col:
                if not entry == 0:
                    reduced_col += [entry]
            final_col = []
            for j in range(len(reduced_col)):
                if j < len(reduced_col) -1 and reduced_col[j] == reduced_col[j+1]:
                    final_col += [2*reduced_col[j]]
                    reduced_col[j+1] = 0
                elif reduced_col[j] > 0:
                    final_col += [reduced_col[j]]
            
            final_col += [0]*(size-len(final_col))
            resultArray += [final_col]
        resultArray = [[resultArray[i][j] for i in range(size)] for j in range(size)]

        changed = not all([all([grid[i][j] == resultArray[i][j] for i in range(size)]) for j in range(size)])

        if spawn and changed:
            spawn_loc = Game.pickRandomEmptyLoc(resultArray)
            if spawn_loc[0] != -1:
                
                rand_double = random.random()
                if rand_double < .9:
                    new = 2
                else:
                    new = 4
                resultArray[spawn_loc[0]][spawn_loc[1]] = new

        return (resultArray, changed)

    @staticmethod
    def shiftDown(grid, spawn = True):
        resultArray = []
        size = len(grid)
        for i in range(size):
            col = [grid[x][i] for x in range(size)]
            reduced_col = []
            for entry in col:
                if not entry == 0:
                    reduced_col += [entry]
            reduced_col.reverse()
            final_col = []
            for j in range(len(reduced_col)):
                if j < len(reduced_col) -1 and reduced_col[j] == reduced_col[j+1]:
                    final_col += [2*reduced_col[j]]
                    reduced_col[j+1] = 0
                elif reduced_col[j] > 0:
                    final_col += [reduced_col[j]]
            
            final_col += [0]*(size-len(final_col))
            final_col.reverse()
            resultArray += [final_col]

        resultArray = [[resultArray[i][j] for i in range(size)] for j in range(size)]

        changed = not all([all([grid[i][j] == resultArray[i][j] for i in range(size)]) for j in range(size)])


        if spawn and changed:
            spawn_loc = Game.pickRandomEmptyLoc(resultArray)
            if spawn_loc[0] != -1:
                
                rand_double = random.random()
                if rand_double < .9:
                    new = 2
                else:
                    new = 4
                resultArray[spawn_loc[0]][spawn_loc[1]] = new

        return (resultArray, changed)


    def __str__(self):
        rows  = []
        maxLength = 0
        for i in range(self.size):
            for j in range(self.size):
                length = len(str(self.getCell(i,j)))
                if length > maxLength:
                    maxLength = length
        width = maxLength * self.size + 3*(self.size -1) + 4
        fmt = "{:>" + str(maxLength) + "}"

        bar = "-"*width + "\n"
        filler = "| " + (" "*maxLength + " | ") * self.size + "\n"
        result = "" + bar
        for i in range(self.size):
            result += filler + "|"
            for j in range(self.size):
                num = self.getCell(i,j)
                if num != 0:
                    s = str(num)
                else:
                    s = ""
                result += " " + fmt.format(s) + " |"
            result += "\n" + filler + bar

        return result

class FeatureBuilder:

    def makeFeatureFromGrid(array):
        feature = []
        for row in array:
            feature += [math.log(x,2) for x in row]
        return feature

    def makeGridFromFeature(feature):
        grid = []
        size = len(feature)**(1./2)
        for row in range(size):
            row_grid = []
            for col in range(size):
                row_grid += [2**feature(row*size + col)]
            grid += [row_grid]
        return grid

    def findEquivalentGrid(feature):
        grid = makeGridFromFeature(feature)
        size = len(grid)
        move_list = [CONST_UP, CONST_RIGHT, CONST_DOWN, CONST_LEFT]
        result = [] #list of feature, move_list pairs
        #reflexive
        result += [(feature[:], move_list[:])]

        #flip horiz
        transformed_grid = [[grid[row][size-col] for col in range(size)] for row in range(size)]
        transformed_moves = [CONST_UP, CONST_LEFT, CONST_DOWN, CONST_RIGHT]
        result += [(makeFeatureFromGrid(transformed_grid), transformed_moves)]

        #flip vert
        transformed_grid = [[grid[size - row][col] for col in range(size)] for row in range(size)]
        transformed_moves = [CONST_DOWN, CONST_RIGHT, CONST_UP, CONST_LEFT]
        result += [(makeFeatureFromGrid(transformed_grid), transformed_moves)]

        #rotate 90  cw
        transformed_grid = [[grid[size - row][col] for col in range(size)] for row in range(size)]
        transformed_moves = [CONST_RIGHT, CONST_DOWN, CONST_LEFT, CONST_UP]
        result += [(makeFeatureFromGrid(transformed_grid), transformed_moves)]

        #rotate 180 cw
        transformed_grid = [[grid[size - row][size - col] for col in range(size)] for row in range(size)]
        transformed_moves = [CONST_DOWN, CONST_LEFT, CONST_UP, CONST_RIGHT]
        result += [(makeFeatureFromGrid(transformed_grid), transformed_moves)]

        #rotate 90 ccw
        transformed_grid = [[grid[row][size - col] for col in range(size)] for row in range(size)]
        transformed_moves = [CONST_LEFT, CONST_UP, CONST_RIGHT, CONST_DOWN]
        result += [(makeFeatureFromGrid(transformed_grid), transformed_moves)]

        #flip diag top left to bottom right
        transformed_grid = [[grid[col][row] for col in range(size)] for row in range(size)]
        transformed_moves = [CONST_LEFT, CONST_DOWN, CONST_RIGHT, CONST_UP]
        result += [(makeFeatureFromGrid(transformed_grid), transformed_moves)]

        #flip diag top right to bottom left
        transformed_grid = [[grid[size-col][size-row] for col in range(size)] for row in range(size)]
        transformed_moves = [CONST_RIGHT, CONST_UP, CONST_LEFT, CONST_DOWN]
        result += [(makeFeatureFromGrid(transformed_grid), transformed_moves)]

        return result


#module level functions for manipulating strings
def combine(games):
    result = ""
    width = 4
    current = ""
    for i in range(len(games)):
        if i % width == 0:
            current = games[i]
        else:
            current = horizontalAdd(current, games[i])
        if (i+1) % width == 0:
            result += "\n" + current
            current = ""
    if not current == "":
        result += "\n" + current
    return result

#add multi-line strings
def horizontalAdd(a, b):
    a_lines = a.split("\n")
    b_lines = b.split("\n")
    maxLen = max([len(x) for x in a_lines])
    fmt = "{:<" + str(maxLen) + "}"
    tab = " "*4
    result = ""
    for i in range(max(len(a_lines), len(b_lines))):
        a_str = ""
        if i < len(a_lines):
            a_str = a_lines[i]
        b_str = ""
        if i < len(b_lines):
            b_str = b_lines[i]
        result += fmt.format(a_str) + tab + b_str + "\n"
    return result

main()
