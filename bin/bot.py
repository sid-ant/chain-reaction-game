from random import randint
import copy

# global variables

size = 5
grid = []
moves = []
my_orbs = []
opponent_orbs = []
volatile_orbs = []
my_volatile = []
opponent_volatile = []
empty_spaces = []
nextVolatileOrbs = []


def bestMove():
    opponentOrbs = 0
    myOrbs = 0
    emptySpaces = 0
    myOutcomes = []
    #print "in best move"
    # myFuture all possible cases

    for orbs in my_volatile:
        global nextVolatileOrbs
        nextVolatileOrbs = copy.deepcopy(volatile_orbs)
        global nextMoveGrid
        nextMoveGrid = copy.deepcopy(grid)

        # gets outcome when the orb exploded
        lookintofuture(orbs[0], orbs[1])

        for i in nextMoveGrid:
            for j in range(size):
                if i[j] / 10 == player_id:
                    myOrbs += 1
                elif i[j] / 10 != player_id and i[j] != 0:
                    opponentOrbs += 1
                else:
                    emptySpaces += 1

        if opponentOrbs == 0:
            iWin = [orbs[0], orbs[1]]
            return iWin

        myOutcomes.append([orbs, myOrbs, opponentOrbs, emptySpaces])
        nextMoveGrid = grid
        opponentOrbs = 0
        myOrbs = 0
        emptySpaces = 0

    print myOutcomes[0][2]
    print len(opponent_orbs)
    # keep only the outcomes where I am capturing orbs
    for blah in range(len(myOutcomes)):
        uncertanity = 0
        if myOutcomes[uncertanity][2] < len(opponent_orbs) and myOutcomes[uncertanity][1] > len(my_orbs):
            continue
        else:
            del myOutcomes[uncertanity]
            uncertanity -= 1
        uncertanity += 1


    # check if I captured any orbs
    if len(myOutcomes) > 0:
        print "have something to kill"
        myMove = maximumSecureKills(myOutcomes)
        # secure kills: I don't die in next move and I don't lose more in next move then I acquired in this move
        if myMove == -1:  # could not get any such move which doesn't let me capture with net profit :'(
            myMove = safePlay()
        return myMove
    else:
        #print "nothing to kill"
        myMove = safePlay()
        return myMove


def lookintofuture(i, j):
    global nextMoveGrid
    global nextVolatileOrbs

    sourceNode = [i, j]
    nextMoveGrid[i][j] = 0
    sourceNodeIndex = nextVolatileOrbs.index(sourceNode)
    del nextVolatileOrbs[sourceNodeIndex]

    right = [i, j + 1]
    left = [i, j - 1]
    bottom = [i - 1, j]
    top = [i + 1, j]
    directions = [right, left, bottom, top]

    for k in range(4):
        if -1 in directions[k] or 5 in directions[k]:
            continue
        elif directions[k] in nextVolatileOrbs:
            lookintofuture(directions[k][0], directions[k][1])
        else:
            newX = directions[k][0]
            newY = directions[k][1]
            if nextMoveGrid[newX][newY] == 0:
                nextMoveGrid[newX][newY] = player_id * 10
            if nextMoveGrid[newX][newY] / 10 != player_id:
                tmp = nextMoveGrid[newX][newY] % 10
                nextMoveGrid[newX][newY] = player_id * 10 + tmp
            nextMoveGrid[newX][newY] += 1
            if nextMoveGrid[newX][newY] % 10 == surrounding(newX, newY) - 1:
                nextVolatileOrbs.append([newX, newY])

    return


# I've exhausted my attack options, try to find a position where I don't die and develop the game
# try to build near my volatile

def safePlay():
    # since there is no attack to do, give priority to corners
    print "in safe play"
    #print "grid is"
    #print grid
    for i in range(0, 5, 4):
        if grid[i][0] == 0 and isSafe(i, 0) == True:
            x = i
            y = 0
            print "emabrising"
            return [x, y]
        elif grid[i][4] == 0 and isSafe(i, 4) == True:
            x = i
            y = 4
            print "bhfbjwhefbhejf"
            return [x, y]

    if len(my_volatile) > 0:
        nonVolatileOrbs = [orb for orb in moves if orb not in my_volatile]
    else:
        nonVolatileOrbs = moves

    safePositions = []
    for stableOrbs in nonVolatileOrbs:
        i = stableOrbs[0]
        j = stableOrbs[1]
        if isSafe(i, j) is True:
            safePositions.append([i, j])

    for positions in safePositions:
        i = positions[0]
        j = positions[1]
        right = [i, j + 1]
        left = [i, j - 1]
        bottom = [i - 1, j]
        top = [i + 1, j]
        directions = [right, left, bottom, top]
        for k in range(4):
            if -1 in directions[k] or 5 in directions[k]:
                continue
            elif directions[k] in my_volatile:
                return [i, j]

    # if not found near any of my_volatile in safePositons, just pick a random safe position
    stop = len(safePositions)
    position = randint(0, (stop - 1))
    x = safePositions[position][0]
    y = safePositions[position][1]

    return [x, y]


def isSafe(a, b):
    if player_id == 1:
        opponent_id = 2
    else:
        opponent_id = 1


    for orbs in opponent_volatile:
        global nextVolatileOrbs
        nextVolatileOrbs = copy.deepcopy(volatile_orbs)
        global nextMoveGrid

        nextMoveGrid = copy.deepcopy(grid)
        print nextMoveGrid
        # gets outcome when the orb exploded
        lookintofuture(orbs[0], orbs[1])
        print  nextMoveGrid

        print "hello"
        print nextMoveGrid[a][b]
        if nextMoveGrid[a][b] / 10 == opponent_id:
            return False

    return True


# secure kills: I don't die in next move and I don't lose more in next move then I acquired in this move
def maximumSecureKills(outcomes):
    #print "arrived in securekills here"
    myOutcomes = outcomes
    # get the move where I reduce the opponenet to least number of orbs : take that bitch!
    # opponentLow contains bestMove co-ordinates and the index to find that on myOutcomes
    opponentLow = leastOpponentOrbs(myOutcomes)
    # no such move exists :(
    if len(outcomes) <= 0:
        return -1
    if nextMoveILose(opponentLow, myOutcomes) == False:
        return opponentLow[0]
    else:
        del myOutcomes[opponentLow[1]]
        maximumSecureKills(myOutcomes)


def leastOpponentOrbs(outcomes):
    myOutcomes = outcomes
    leastOpponent = 1000  # random impossibe largest value

    for judge in range(len(myOutcomes)):
        if myOutcomes[judge][2] < leastOpponent:
            leastOpponent = myOutcomes[judge][2]
            bestmove = myOutcomes[judge][0]
            bestmoveindex = judge

    return [bestmove, bestmoveindex]


# from the perspectieve of opponent
def nextMoveILose(afterMyMove, previousMoveOutComes):

    global nextVolatileOrbs
    nextVolatileOrbs = copy.deepcopy(volatile_orbs)
    global nextMoveGrid
    nextMoveGrid = copy.deepcopy(grid)
    lookintofuture(afterMyMove[0][0], afterMyMove[0][1])

   #print afterMyMove[0][0],afterMyMove[0][1]
    stateAfterMyMove = copy.deepcopy(nextMoveGrid)



    bestMoveIndex = afterMyMove[1]
    # number of orbs that was acquired by me in the last move
    myOrbsAcquired = previousMoveOutComes[bestMoveIndex][1] - len(my_orbs)
    opponentOrbs = 0
    myOrbs = 0
    emptySpaces = 0
    opponentOutcomes = []
    if player_id == 1:
        opponent_id = 2
    else:
        opponent_id = 1

    newopponent_volatile=[]
    newvolatile_orbs = []

    #print stateAfterMyMove

    for i in range(size):
        for j in range(size):
            if nextMoveGrid[i][j] % 10 == surrounding(i, j) - 1 and nextMoveGrid[i][j] / 10 != player_id:
                newopponent_volatile.append([i, j])
            if nextMoveGrid[i][j] % 10 == surrounding(i, j) - 1:
                newvolatile_orbs.append([i, j])

    #print newopponent_volatile

    # opponentFuture so he doesn't kill me in next move
    for orbs in newopponent_volatile:

        nextVolatileOrbs = copy.deepcopy(newvolatile_orbs)
        nextMoveGrid = copy.deepcopy(stateAfterMyMove)
        lookintofuture(orbs[0], orbs[1])

        for i in nextMoveGrid:
            for j in range(size):
                if i[j] / 10 == opponent_id:
                    myOrbs += 1
                elif i[j] / 10 != opponent_id and i[j] != 0:
                    opponentOrbs += 1
                else:
                    emptySpaces += 1

        if opponentOrbs == 0:  # myDeath >.<
            return True

        opponentOutcomes.append([orbs, myOrbs, opponentOrbs, emptySpaces])
        nextMoveGrid = grid
        opponentOrbs = 0
        myOrbs = 0
        emptySpaces = 0


    for kp in range(len(opponentOutcomes)):
        #print opponentOutcomes[kp][1]
        orbsGained = opponentOutcomes[kp][1] - len(opponent_orbs)
        #print "orbs lost: ",orbsGained
        if orbsGained > myOrbsAcquired:
            return True

    return False


# counts the no of surrounding squares
def surrounding(i, j):
    count = 4
    right = [i, j + 1]
    left = [i, j - 1]
    bottom = [i - 1, j]
    top = [i + 1, j]
    directions = [right, left, bottom, top]
    for k in range(4):
        if -1 in directions[k] or 5 in directions[k]:
            count -= 1
    return count


def main():
    # deducing positions
    for i in range(size):
        for j in range(size):
            if grid[i][j] == 0 or grid[i][j] / 10 == player_id:
                moves.append([i, j])
            if grid[i][j] / 10 == player_id:
                my_orbs.append([i, j])
            if grid[i][j] != 0 and grid[i][j] / 10 != player_id:
                opponent_orbs.append([i, j])
            if grid[i][j] % 10 == surrounding(i, j) - 1:
                volatile_orbs.append([i, j])
            if grid[i][j] % 10 == surrounding(i, j) - 1 and grid[i][j] / 10 == player_id:
                my_volatile.append([i, j])
            elif grid[i][j] % 10 == surrounding(i, j) - 1 and grid[i][j] / 10 != player_id:
                opponent_volatile.append([i, j])

    # fill atleast one corner
    if len(my_volatile) == 0:
        for i in range(0, 5, 4):
            if grid[i][0] == 0:
                x = i
                y = 0
                return [x, y]
            elif grid[i][4] == 0:
                x = i
                y = 4
                return [x, y]
        move = safePlay()
        return move

    if len(my_volatile) != 0:
        #print "in non volatile"
        move = bestMove()
        return move



# taking input
for i in range(size):
    temp = raw_input("").split()
    for j in range(len(temp)):
        temp[j] = int(temp[j])
    grid.append(temp)

nextMoveGrid = copy.deepcopy(grid)
#print grid
player_id = input("")
output = main()
print output[0], output[1]
