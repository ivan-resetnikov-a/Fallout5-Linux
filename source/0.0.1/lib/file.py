from json import load, dump



def get (filename=None, key=None) :
	with open(filename, "r", encoding="utf-8") as file :
		content = load(file)
		if key == None : return content
		else :           return content[key]


def write (filename=None, key=None, data=None) :
	content = get(filename)
	if key == None : content = data
	else : content[key] = data
	with open(filename, "w", encoding="utf-8") as file : dump(content, file, indent=4)


def new (filename) :
	file = open(filename, "w")
	file.write(r"{}")
	file.close()