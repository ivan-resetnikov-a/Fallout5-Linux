from lib.file import *
from os import system, listdir
from platform import system as os_name
from datetime import date


# clear terminal command
if os_name() == "Linux" :
	clear = lambda : system("clear")
if os_name() == "Windows" :
	clear = lambda : system("cls")



class Character :
	def __init__ (self, posG, posL, texture) :
		self.posG = posG
		self.posL = posL
		self.texture = texture


class Player (Character) :
	def __init__ (self, posG, posL, texture) :
		Character.__init__(self, posG, posL, texture)
		self.name = "Noname"
		self.hp, self.hp_max = 500, 500
		self.move()


	def load (self, data) :
		self.name   = data["name"]
		self.posG   = data["posG"]
		self.posL   = data["posL"]
		self.hp     = data["hp"]
		self.hp_max = data["hp_max"]


	def save (self, filename) :
		## getting rid of symbols ##
		prohibitedCharacters = ["(", ")", "[", "]", " ", "^", "#", "%", "&", "{", "}", "\"", "\\", "/", "'", "<", ">", "*", "?", "$", "!", ":", "@", "+", "`", "|", "="]
		clearedFilename = ""
		for char in filename :
			if not char in prohibitedCharacters : clearedFilename += char
			else : clearedFilename += "_"
		########## saving ##########
		new(f"saves/{clearedFilename}.json")
		write(f"saves/{clearedFilename}.json",
			data={
				"name" : filename,
				"date" : str(date.today()),
				"data" : {
					"player" : {
						"name"   : self.name  ,
						"posL"   : self.posL  ,
						"posG"   : self.posG  ,
						"hp"     : self.hp    ,
						"hp_max" : self.hp_max
					}
				}
			})


	def move (self) :
		file = get("data/fallout5/world/{}.{}.{}.json".format(self.posG[0], self.posG[1], self.posG[2]))
		self.locationContent   = file["content"]
		self.locationCollision = file["collision"]


class NPC (Character) :
	def __init__ (self, posG, posL, texture) :
		Character.__init__(self, posG, posL, texture)


class Game :
	def __init__ (self, player) :
		self.player = player
		self.render = self.renderMedium
		#############
		self.entities = {"0.0.0": [NPC([0, 0, 0], [4, 4], "$")]}


	def savesManager (self, player, allowCreateNewGame) :
		if allowCreateNewGame : a = " │ 3 - NEW GAME"
		else : a = ""
		while True :
			clear()
			####### render ######
			height, files = 20, listdir("saves/")
			files.remove("initial.json")
			files.remove("runtime.json")
			print("┌{0}┬{1}┐".format("─"*30, "─"*12))
			print("│{0}MY SAVES{0}│{1}DATE{1}│".format(" "*11, " "*4))
			print("├{0}┼{1}┤".format("─"*30, "─"*12))
			if len(files) > height : height = files
			for i in range(height) :
				try :
					saveContent = get("saves/"+files[i])
					print("│ {}. {}{}│ {} │".format(i, saveContent["name"], " "*(27-(len(str(i))+len(saveContent["name"]))), saveContent["date"]))
				except IndexError :
					print("│{}│{}│".format(" "*30, " "*12))
			print("└{0}┴{1}┘".format("─"*30, "─"*12))

			####### input #######
			print("1 - LOAD │ 2 - CANCEL"+a)
			index = input("> ")
			print("─"*45)

			###### process ######
			if   index == "1" :
				if len(files) > 1 :
					try :
						index = int(input("INDEX > "))
						player.load(get("saves/"+files[index], "data")["player"])
					except : pass
				elif len(files) == 1 :
					player.load(get("saves/"+files[0], "data")["player"])
				return "load"
				break
			elif index == "2" :
				return "cancel"
				break
			elif index == "3" and allowCreateNewGame : return "newGame"


	def sideBarInfo (self, i) :
		info = [
			f"│    {self.player.name}", 
			"│ ♥ {self.player.hp}/{self.player.hp_max}"]
		try : return info[i]
		except : return "│"


	def renderMedium (self) :
		y, localEntities = 0, self.entities["{}.{}.{}".format(self.player.posG[0], self.player.posG[1], self.player.posG[2])]
		for line in self.player.locationContent :
			x, output = 0, ""
			for char in line :
				for entity in localEntities :
					if entity.posL[0] == x and entity.posL[1] == y : char = entity.texture
					if self.player.posL[0] == x and self.player.posL[1] == y : char = self.player.texture
				output += char
				x += 1
			print(output+self.sideBarInfo(y))
			y += 1


	def gameLoop (self) :
		while True :
			clear()
			self.render()
			print("─"*len(self.player.locationContent[0])+"┴"+"─"*20)
			print("W - ▲        │ A - ▼    │ S - ◄    │ D - ►")
			print("E - INTERACT │ [ - LOAD │ ] - SAVE │ Q - EXIT")
			index = input("> ")
			print("─"*len(self.player.locationContent[0])+"─"*21)
			#########################
			# move
			if   index == "w" and not self.player.locationContent[self.player.posL[1]-1][self.player.posL[0]:self.player.posL[0]+1:] in self.player.locationCollision : self.player.posL[1] -= 1
			elif index == "s" and not self.player.locationContent[self.player.posL[1]+1][self.player.posL[0]:self.player.posL[0]+1:] in self.player.locationCollision : self.player.posL[1] += 1
			elif index == "a" and not self.player.locationContent[self.player.posL[1]][self.player.posL[0]-1:self.player.posL[0]:]   in self.player.locationCollision : self.player.posL[0] -= 1
			elif index == "d" and not self.player.locationContent[self.player.posL[1]][self.player.posL[0]+1:self.player.posL[0]+2:] in self.player.locationCollision : self.player.posL[0] += 1
			# interacting
			elif index == "e" : pass
			elif index == "]" : self.player.save(input("SAVE NAME > "))
			elif index == "[" : self.savesManager(self.player, False)
			# exit
			elif index == "q" : break