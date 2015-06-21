import pytest
import Game

test_board = [
    [2, 0, 8, 0]
  , [0, 4, 0, 0]
  , [2, 0, 0, 2]
  , [0, 0, 8, 2]
]

end_board = [
    [1, 2, 3, 4]
  , [5, 6, 7, 8]
  , [1, 2, 3, 4]
  , [5, 6, 7, 8]
]

def testGetCell():
    new = Game(4)
    new.array = test_board
    for i in range(4):
        for j in range(4):
            assert new.getCell(i,j) = test_board[i,j]

def testGetState():
    new = Game(4)
    new.array = test_board
    assert new.getState() == [2,0,8,0,0,4,0,0,2,0,0,2,0,0,8,2]

def testIsOver():
    new = Game(4)
    new.array = test_board
    assert !new.isOver()

    new = Game(4)
    new.array = end_board
    assert new.isOver()

def testInitialize():
    new = Game(4)
    new.initialize()
    assert np.array(new.array).sum() == 2

    new.array = end_board
    new.initialize()
    assert np.array(new.array).sum() == 2

test_board = [
    [2, 0, 8, 0]
  , [0, 4, 0, 0]
  , [2, 0, 0, 2]
  , [0, 0, 8, 2]
]

def testMakeMove():
    new = Game(4)
    new.array = test_board
    new.makeMove(Game.CONST_UP)
    assert (new.array[0] == [4,4,16,4]) and
        (np.array(new.array).sum() <= 32) and
        (np.array(new.array).sum() >= 28)

    new.array = test_board
    new.makeMove(Game.CONST_DOWN)
    assert (new.array[0] == [4,4,16,4]) and
        (np.array(new.array[1:3]).sum() <= 4)


    new.array = test_board
    new.makeMove(Game.CONST_RIGHT)
    assert ([row[0] for row in new.array] == [2,4,4,8]) and
        (np.array([row[1:3] for row in new.array]).sum() <= 14) and
        (np.array([row[1:3] for row in new.array]).sum() >= 10)

    new.array = test_board
    new.makeMove(Game.CONST_LEFT)
    assert ([row[3] for row in new.array] == [8,4,4,2]) and
        (np.array([row[0:2] for row in new.array]).sum() <= 14) and
        (np.array([row[0:2] for row in new.array]).sum() >= 10)

def testPossibleMoves():
    pass
