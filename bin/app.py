import web
import logic
import copy
import os
import bot

urls = (
  '/','game','/home','home','/menu','menu','/name','getname','/ai','ai'
  )

# what does this do and how does it do it?
app = web.application(urls, globals())
render = web.template.render('templates/')

grid=[[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
player_id=1
old=[]
matchType=0


class home:
    def GET(self):
        return render.home()

class menu:
    def GET(self):
        global grid
        global player_id
        quit=web.input()
        if quit.clear is not None:
            grid=[[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
            player_id=1
        return render.menu()


class getname:
    def GET(self):
        ty = web.input()
        # determining if its is pvp or pvc
        players = int(ty.type)
        return render.playername(type=players)
    def POST(self):
        global matchType
        # connect to database here and store player names
        # take game type input from here and pass it to game
        nameType = web.input()
        matchType = nameType.match
        # gets called only once
        return render.game(input=grid,player=player_id,winner=0,Mtype=matchType)

class game:
    def GET(self):
        # this no longer gets called I guess!
        grid=[[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
        return render.game(input=grid,player=player_id,winner=0,Mtype=matchType)

    def POST(self):

        # this gets called for the subsequent times whenever an cell is clicked upon
        global grid
        global old
        global player_id

        # here orbClicked gets the input about which cell was clicked
        orbClicked = web.input(position=None,playerid=None)
        orb=orbClicked.position
        pID=orbClicked.playerid
        coOrdinates = orb.split(',')
        for i in range(len(coOrdinates)):
            coOrdinates[i]=int(coOrdinates[i])
        x=coOrdinates[0]
        y=coOrdinates[1]

        # need this to determine winner
        old = copy.deepcopy(grid)

        player_id = int(pID)
        grid=logic.move(x,y,player_id,grid)


        if player_id==1:
            player_id=2
        else:
            player_id=1

        # determining if someone won or not?
        old1=0
        old2=0
        new1=0
        new2=0
        win=0

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

        print matchType
        print player_id
        return render.game(input=grid,player=player_id,winner=win,Mtype=matchType)

class ai:
    def GET(self):
        global grid
        global player_id
        print "AI MOVES BITCHES!!!"
        win=0
        validity = web.input(valid=None)
        if int(validity.valid)==1:
            print "HELL YEAH"
            print "Player id? is "+str(player_id)
            postion = bot.main(grid,player_id)
            x=postion[0]
            y=postion[1]

            # need this to determine winner
            old = copy.deepcopy(grid)
            grid=logic.move(x,y,player_id,grid)

            if player_id==1:
                player_id=2
            else:
                player_id=1

            # determining if someone won or not?
            old1=0
            old2=0
            new1=0
            new2=0


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
        return render.game(input=grid,player=player_id,winner=win,Mtype=matchType)


# still doesn't know what this does? duh?
if __name__ == "__main__":
    app.run()
