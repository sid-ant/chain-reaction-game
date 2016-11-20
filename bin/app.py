import web

urls = (
  '/', 'index','/hello','wow','/form','handle','/game','game'
  )

# what does this do and how does it do it?
app = web.application(urls, globals())
render = web.template.render('templates/')
grid=[[00,00,00,00,00],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]

class game:
    def GET(self):
        #input=[[01,20,30,40,0],[0,0,0,03,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
        return render.game()
    def POST(self):
        orbClicked = web.input(position=None)
        orb=orbClicked.position
        coOrdinates = orb.split(',')
        for i in range(len(coOrdinates)):
            coOrdinates[i]=int(coOrdinates[i])
        x=coOrdinates[0]
        y=coOrdinates[1]
        grid[x][y]=01
        return render.game(input=grid)

class index:
    def GET(self):
        #whatever the form supplies via get in field name
        form = web.input(name=None,travel=None)
        greeting = "Hello  "+str(form.name) + str(form.travel)
        return render.index(greeting=greeting)
        # return render.index()

class wow:
    def GET(self):
        # msg = "nice to meet you"
        # return msg
        return render.duck("wow")

class handle:
    def GET(self):
        return render.hello_form()
    def POST(self):
        form = web.input(name=None,greet=None)
        #greeting = "%s, %s" % (form.greet, form.name)
        msg = "Hello %s and  %s " %(form.name,form.greet)
        return render.index(greeting=msg)

# still doesn't know what this does? duh?
if __name__ == "__main__":
    app.run()
