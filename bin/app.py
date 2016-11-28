import web
import logic

urls = (
  '/','game'
  )

# what does this do and how does it do it?
app = web.application(urls, globals())
render = web.template.render('templates/')

grid=[[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
player_id=1

class game:
    def GET(self):
        gird=[[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
        return render.game(input=grid,player=player_id)
    def POST(self):
        global grid
        orbClicked = web.input(position=None,playerid=None)
        orb=orbClicked.position
        pID=orbClicked.playerid
        coOrdinates = orb.split(',')
        for i in range(len(coOrdinates)):
            coOrdinates[i]=int(coOrdinates[i])
        x=coOrdinates[0]
        y=coOrdinates[1]
        # need to add server side check to ensure user clicked on their node only

        #player_id = player_id.split(',')
        player_id = int(pID)
        grid=logic.move(x,y,player_id,grid)
        if player_id==1:
            player_id=2
        else:
            player_id=1
        # x and y are input co-ordinates for the z to work on
        return render.game(input=grid,player=player_id)


# still doesn't know what this does? duh?
if __name__ == "__main__":
    app.run()
