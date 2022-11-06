import lib.core as core

logo = r"""
  ______    _ _             _     _____ 
 │  ____│  │ │ │           │ │   │ ____│
 │ │__ __ _│ │ │ ___  _   _│ │_  │ │__  
 │  __/ _` │ │ │/ _ \│ │ │ │ __│ │___ \ 
 │ │ │ (_│ │ │ │ (_) │ │_│ │ │_   ___) │
 │_│  \__,_│_│_│\___/ \__,_│\__│ │____/"""



def renderMainMenu (logo, var) :
	print(logo)
	print(" Fallout 5 (c) 2022  TheUnknownDev")
	var = list(var.items())
	for i in range(len(var)) : print("{}{} - {}".format(" "*30, var[i][0], var[i][1]))


while True :
	core.clear()
	renderMainMenu(logo, {"1":"PLAY", "2":"SETTINGS", "3":"EXIT"})
	index = input("> ")
	###################
	if index == "1" :
		player = core.Player([0, 0, 0], [1, 1], "@")
		game   = core.Game(player)
		choosen = game.savesManager(player, True)
		if choosen != "cancel" : game.gameLoop()
	elif index == "2" : pass
	elif index == "3" : break