size=5
volatile_orbs=[]
my_volatile=[]
grid=[]
my_orbs=[]
player_id=5

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

def move(x,y,player,inputGrid):
    global grid
    global player_id
    global volatile_orbs,my_volatile,my_orbs
    grid=inputGrid
    player_id=player
    my_orbs=[]
    my_volatile=[]
    volatile_orbs=[]
    for i in range(size):
        for j in range(size):
            if grid[i][j] / 10 == player_id:
                my_orbs.append([i, j])
            if grid[i][j] % 10 == surrounding(i, j) - 1:
                volatile_orbs.append([i, j])
            if grid[i][j] % 10 == surrounding(i, j) - 1 and grid[i][j] / 10 == player_id:
                my_volatile.append([i, j])

    # print ":::::::OUTPUT:::::"
    # print "My Volatile is: ",my_volatile
    # print "Grid is:",grid
    # print "Volatile is",volatile_orbs
    # print "::::::END:::::::::"
    if [x,y] in my_volatile:
        result(x,y)
    else:
        if grid[x][y]==0:
            grid[x][y]+=player_id*10
        grid[x][y]+=1

    return grid

# call this function only for volatile orbs noob
def result(i,j):
    global grid
    global volatile_orbs

    sourceNode = [i, j]
    grid[i][j]=0
    sourceNodeIndex = volatile_orbs.index(sourceNode)
    del volatile_orbs[sourceNodeIndex]

    right = [i, j + 1]
    left = [i, j - 1]
    bottom = [i - 1, j]
    top = [i + 1, j]
    directions = [right, left, bottom, top]

    for k in range(4):
        if -1 in directions[k] or 5 in directions[k]:
            continue
        elif directions[k] in volatile_orbs:
            result(directions[k][0], directions[k][1])
        else:
            newX = directions[k][0]
            newY = directions[k][1]
            if grid[newX][newY] == 0:
                grid[newX][newY] = player_id * 10
            if grid[newX][newY] / 10 != player_id:
                tmp = grid[newX][newY] % 10
                grid[newX][newY] = player_id * 10 + tmp
            grid[newX][newY] += 1
            if grid[newX][newY] % 10 == surrounding(newX, newY) - 1:
                volatile_orbs.append([newX, newY])

    return
