import tkinter
import random
#import tkMessageBox

'''
This game is made so that two people can play a game of baseball
via rolls of dice and choices.
'''

'''
Eventually this will have a part to draft or insert players stats
'''
stdroll = 6

class NewGame(tkinter.Tk):
	def __init__(self,parent):
		tkinter.Tk.__init__(self,parent)
		self.parent 	= parent
		self.initialize()

		
	def initialize(self):
		self.lab = tkinter.Label(self,text='Who do we have Playing?')
		self.lab.pack()
		
		self.frame 		= tkinter.LabelFrame(self)
		self.frame.pack()
		
		self.ent1 		= tkinter.StringVar()
		self.labname1	= tkinter.Label(self.frame,text='Player One:')
		self.ent1 		= tkinter.Entry(self.frame,textvariable=self.ent1)
		
		self.labname1.grid(row=0,column=0)
		self.ent1.grid(row=0,column=1)
		
		self.ent2		= tkinter.StringVar()
		self.labname2 	= tkinter.Label(self.frame,text='Player Two:')
		self.ent2 		= tkinter.Entry(self.frame,textvariable=self.ent2)
		
		self.labname2.grid(row=1,column=0)
		self.ent2.grid(row=1,column=1)
		
		self.b1 		= tkinter.Button(self.frame,text='Play',command=self.newplayers)
		self.b2 		= tkinter.Button(self.frame,text='Quit',command=self.quit)
		
		self.b1.grid(row=2,column=0)
		self.b2.grid(row=2,column=1)
		
	def newplayers(self):	
		self.player1 	= self.ent1.get()
		self.player1 	= NewPlayer(self.player1)
		self.player2 	= self.ent2.get()
		self.player2 	= NewPlayer(self.player2)
		
		self.start = StartGame(None,self.player1,self.player2)

class NewPlayer:
	def __init__(self,name):
		self.name = name
		self.score = 0
		self.roll = stdroll
		
class StartGame(NewGame, tkinter.Tk):
	def __init__(self,parent,player1,player2):
		tkinter.Tk.__init__(self,parent)
		self.parent = parent
		self.player1 = player1
		self.player2 = player2
		self.inning 	= 1
		self.top 		= True
		self.outs 		= 0
		self.balls		= 0
		self.strikes	= 0
		self.bases 		= [0,0,0]
		self.seebases	= self.bases[0:3]
		self.player2.roll	= 200
		self.initialize()
		
	def initialize(self):
		self.atbat()
		
		self.lab = tkinter.Label(self,text='Play Ball!')
		self.lab.pack()
		
		self.frame = tkinter.LabelFrame(self)
		self.frame.pack()
		
		self.score = tkinter.Label(self.frame,text='%s: %s VS %s: %s' % 
		(self.player1.name,self.player1.score,self.player2.name,self.player2.score))
		self.score.grid(row=0,column=0)
		
		self.frame_board = tkinter.LabelFrame(self)
		self.frame_board.pack()
		
		self.board1 = tkinter.Label(self.frame_board,text=str(self.inning) + ' Inning')
		self.board1.grid(row=0,column=0)
		
		self.board2 = tkinter.Label(self.frame_board,text='Top' if self.top==True else 'Bottom')
		self.board2.grid(row=1,column=0)
		
		self.board3 = tkinter.Label(self.frame_board,text=
		'Balls: %s /// Strikes: %s /// Outs: %s' % (self.balls,self.strikes,self.outs))
		self.board3.grid(row=2,column=0)
		
		self.basesview = tkinter.Label(self.frame_board,text=str(self.bases))
		self.basesview.grid(row=3,column=0)
		
		self.bbat = tkinter.Button(self.frame_board,text='Pitch/Bat',command=self.bat)
		self.bbat.grid(row=4,column=0)
		
	
	def atbat(self):
		if self.top == True:
			self.playerA = self.player1
			self.playerB = self.player2
		else:
			self.playerA = self.player2
			self.playerB = self.player1	
	
	def upkeep(self):
		if self.balls == 4:
			self.run()
			self.newbat()
		elif self.strikes == 3:
			self.outs += 1
			self.newbat()
			if self.outs == 3:
				self.newinn()
		else:
			pass
		self.updatetext()
	
	def updatetext(self):
		self.score.config(text='%s: %s VS %s: %s' % 
		(self.player1.name,self.player1.score,self.player2.name,self.player2.score))
		self.basesview.config(text=str(self.bases))
		self.board1.config(text=str(self.inning) + ' Inning')
		self.board2.config(text='Top' if self.top==True else 'Bottom')
		self.board3.config(text=
		'Balls: %s /// Strikes: %s /// Outs: %s' % (self.balls,self.strikes,self.outs))
		self.basesview.config(text=str(self.bases))
		
	def run(self):
		self.bases.insert(0,1)
		HB = self.bases.pop(-1)
		if HB == 1:
			self.player1.score += 1
		self.updatetext()
		print(self.bases)
		
	def move(self):
		self.bases.insert(0,0)
		HB = self.bases.pop(-1)
		if HB == 1:
			self.playerA.score += 1
		self.updatetext()
		print(self.bases)
	
	def roll(self):
		self.atbat()
		roll1 = random.choice(range(self.playerA.roll))
		roll2 = random.choice(range(self.playerB.roll))		
		print(roll1, roll2)
		if roll1 < roll2:
			return -1
		elif roll1 == roll2:
			return 0
		else:
			return 1
		
	def bat(self):
		self.mark = self.roll()
		if self.mark == -1:
			self.strikes += 1
		elif self.mark == 0:
			self.balls += 1
		elif self.mark == 1:
			self.contact()
		else:
			print('Something went wrong')
		self.updatetext()
		self.upkeep()
			
	def contact(self):
		self.mark = self.roll()
		if self.mark == -1:
			self.outs += 1
		elif self.mark == 0:
			self.run()
		elif self.mark == 1:
			self.run()
			self.onbase()
		self.updatetext()
		self.upkeep()

	def onbase(self):
		self.main 	= tkinter.LabelFrame(self)
		
		self.lab 	= tkinter.Label(self.main,text='Stay or Go')
		self.lab.grid(row=0,column=0)
		
		self.b1	= tkinter.Button(self.main,text='Stay',command=self.main.destroy)
		self.b2	= tkinter.Button(self.main,text='Go',command=self.main.destroy)
		
		self.b1.grid(row=1,column=0)
		self.b2.grid(row=1,column=1)
	
	def newbat(self):
		self.balls 		= 0
		self.strikes	= 0
		
	def newinn(self):
		self.outs = 0
		self.bases = [0,0,0]
		if self.top == False:
			self.inning +=1
		self.top = not self.top
		self.updatetext()
		self.atbat()
		
class App(tkinter.Tk):
	def __init__(self,parent):
		tkinter.Tk.__init__(self,parent)
		self.parent = parent
		self.initialize()
		
	def initialize(self):
		self.lab = tkinter.Label(self,text='Welcome to Baseball')
		self.lab.pack()

		self.frame = tkinter.LabelFrame(self)
		self.frame.pack()
		
		self.b1 = tkinter.Button(self.frame,text='New Game',command=self.newgame)
		self.b2 = tkinter.Button(self.frame,text='Quit',command=self.quit)
		self.b1.grid(row=1,column=0)
		self.b2.grid(row=1,column=1)
		
	def newgame(self):
		self.game = NewGame(None)
		
if __name__=='__main__':
	app = App(None)
	app.mainloop()
	
'''
Questions?
- How to make a button do multiple things?
- How to make a button auto quit after doing a few things?
'''
