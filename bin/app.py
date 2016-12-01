import web
import logic
import copy
import os

urls = (
  '/','game','/home','home'
  )

# what does this do and how does it do it?
app = web.application(urls, globals())
render = web.template.render('templates/')

grid=[[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
player_id=1
old=[]

class home:
    def GET(self):
        return render.home();

class game:
    def GET(self):
        gird=[[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
        return render.game(input=grid,player=player_id,winner=0)
    def POST(self):
        global grid
        global old
        orbClicked = web.input(position=None,playerid=None)
        orb=orbClicked.position
        pID=orbClicked.playerid
        coOrdinates = orb.split(',')
        for i in range(len(coOrdinates)):
            coOrdinates[i]=int(coOrdinates[i])
        x=coOrdinates[0]
        y=coOrdinates[1]
        old = copy.deepcopy(grid)
        print ":::::::LOG:::::::"
        print "OLD GRID IS: ",old
        # need to add server side check to ensure user clicked on their node only

        #player_id = player_id.split(',')
        player_id = int(pID)
        grid=logic.move(x,y,player_id,grid)
        if player_id==1:
            player_id=2
        else:
            player_id=1
        # x and y are input co-ordinates for the z to work on
        old1=0
        old2=0
        new1=0
        new2=0
        win=0
        print "OLD GRID IS: ",old
        for i in range(5):
            for j in range(5):
                if old[i][j]/10==1:
                    old1+=1
                if old[i][j]/10==2:
                    old2+=1
                if grid[i][j]/10==1:
                    new1+=1
                if grid[i][j]/10==2:
                    new2+=1

        if old1!=0 and new1==0:
            win=2
        elif old2!=0 and new2==0:
            win=1
        print "OLD 1s",old1
        print "New 1s",new1
        print "OLD 2s",old2
        print "New 2s",new2
        print "NEW GRID is",grid
        print "WINNER IS",win
        print ":::::::FINISH:::::::"
        return render.game(input=grid,player=player_id,winner=win)

# still doesn't know what this does? duh?
if __name__ == "__main__":
    app.run()
