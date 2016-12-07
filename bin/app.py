import web
import logic
import copy
import os
import bot
from pymongo import MongoClient

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
client = MongoClient('localhost', 27017)
db = client.chainreaction #create or open chainreaction database
games = db.games # create or open document (table) games
NameP1 = ""
NameP2 = ""
gameid=0
gType=""

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
        global matchType,NameP1,NameP2,gameid,gType
        # connect to database here and store player names
        # take game type input from here and pass it to game
        nameType = web.input()
        matchType = nameType.match

        if nameType.player1 is not None:
            p1Name = str(nameType.player1)
        if int(matchType)==1:
            if nameType.player2 is not None:
                p2Name = str(nameType.player2)

        if int(matchType)==1:
            gType='HvH'
            row = {'p1':p1Name,'p2':p2Name,'win':0,'gameType':gType}
        elif int(matchType)==2:
            gType='HvC'
            row = {'p1':p1Name,'p2':'Skynet 0.1','win':0,'gameType':gType}

        gameid = games.insert_one(row).inserted_id

        results = games.find_one({'_id':gameid})
        NameP1 = results['p1']
        NameP2 = results['p2']
        #NameP1 = NameP1+"";
        # gets called only once per match
        return render.game(input=grid,player=player_id,winner=0,Mtype=matchType,p1=NameP1,p2=NameP2)

class game:
    def GET(self):
        # this no longer gets called but too scared to remove it now!
        grid=[[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
        return render.game(input=grid,player=player_id,winner=0,Mtype=matchType,p1=NameP1,p2=NameP2)

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

        if win!=0:
            games.update({'_id':gameid},{'$set':{"win":win}})

        return render.game(input=grid,player=player_id,winner=win,Mtype=matchType,p1=NameP1,p2=NameP2)

class ai:
    def GET(self):
        global grid
        global player_id
       # print "AI MOVES BITCHES!!!"
        win=0
        validity = web.input(valid=None)
        if int(validity.valid)==1:
            #print "HELL YEAH"
           # print "Player id? is "+str(player_id)
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

            if win!=0:
                games.update({'_id':gameid},{'$set':{"win":win}})

        return render.game(input=grid,player=player_id,winner=win,Mtype=matchType,p1=NameP1,p2=NameP2)


# still doesn't know what this does? duh?
if __name__ == "__main__":
    app.run()
