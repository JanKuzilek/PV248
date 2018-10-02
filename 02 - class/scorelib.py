class Person:
	def __init__(self, name, born, died):
		self.name = name
		self.born = born
		self.died = died
	
	def toString(self):
		if(self.name == None or self.name == ""):
			return ""
		elif(self.born == None and self.died == None):
			return self.name
		elif(self.born == None):
			return self.name + " (--" + str(self.died) + ")"
		elif(self.died == None):
			return self.name + " (" + str(self.born) + "--)"
		else:
			return self.name + " (" + str(self.born) + "--" + str(self.died) + ")"
		
class Voice:
	def __init__(self, name, range):
		self.name = name
		self.range = range
		
	def toString(self):
		if(self.range == None and self.name == None):
			return ""
		elif(self.range == None and self.name != None):
			return self.name
		elif(self.range != None and self.name == None):
			return self.range
		else:
			return self.range + ", " + self.name
			
class Composition:
	def __init__(self, name, incipit, key, genre, year, voices, authors):
		self.name = name
		self.incipit = incipit
		self.key = key
		self.genre = genre
		self.year = year
		self.voices = voices
		self.authors = authors
		
class Edition:
	def __init__(self, name, composition, authors):
		self.name = name
		self.composition = composition
		self.authors = authors
		
class Print:
	def __init__(self, edition, print_id, partiture):
		self.edition = edition
		self.print_id = print_id
		self.partiture = partiture
	
	def format(self):
		voiceNumber = 1
		composerToPrint = ""
		editorToPrint = ""
		
		firstComp = True
		for composer in self.edition.composition.authors:
			if(firstComp):
				composerToPrint = composer.toString()
				firstComp = False
			else:
				composerToPrint = composerToPrint + "; " + composer.toString()
				
		firstEditor = True
		for editor in self.edition.authors:
			if(firstEditor):
				editorToPrint = editor.toString()
				firstEditor = False
			else:
				editorToPrint = editorToPrint + ", " + editor.toString()

			
		print("Print Number: " + str(self.print_id))
		if(composerToPrint != ""):
			print("Composer: " + composerToPrint)
		if(self.edition.composition.name != None):
			print("Title: " + self.edition.composition.name)
		if(self.edition.composition.genre != None):
			print("Genre: " + self.edition.composition.genre)
		if(self.edition.composition.key != None):
			print("Key: " + self.edition.composition.key)
		if(self.edition.composition.year != None):
			print("Composition Year: " + str(self.edition.composition.year))
		if(self.edition.name != None):
			print("Edition: " + self.edition.name)
		if(editorToPrint != ""):
			print("Editor: " + editorToPrint)
		for voice in self.edition.composition.voices:
			if(voice.toString() != None):
				print("Voice " + str(voiceNumber) + ": " + voice.toString())
				voiceNumber = voiceNumber + 1
		if(self.partiture):
			print("Partiture: yes")
		else:
			print("Partiture: no")
		if(self.edition.composition.incipit != None):
			print("Incipit: " + self.edition.composition.incipit)
	
	def composition(self):
		return self.edition.composition