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
			return self.name + " ( -- " + str(self.died) + ")"
		elif(self.died == None):
			return self.name + " (" + str(self.born) + " -- )"
		else:
			return self.name + " (" + str(self.born) + " -- " + str(self.died) + ")"
		
class Voice:
	def __init__(self, name, range):
		self.name = name
		self.range = range
		
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
		print(self.edition.composition.voices[0].range)
		voiceNumber = 1
		composerToPrint = ""
		editorToPrint = ""
		
		for composer in self.edition.composition.authors:
			composerToPrint = composer.toString() + "; "
			composerToPrint = composerToPrint[:-2]
		for editor in self.edition.authors:
			editorToPrint = editor.toString() + "; "
			editorToPrint = editorToPrint[:-2]
			
		print("Print number: " + str(self.print_id))
		print("Composer: " + composerToPrint )
		if(self.edition.composition.name != None):
			print("Title: " + self.edition.composition.name)
		if(self.edition.composition.genre != None):
			print("Genre: " + self.edition.composition.genre)
		if(self.edition.composition.key != None):
			print("Key: " + self.edition.composition.key)
		if(self.edition.composition.year != None):
			print("Composition year: " + str(self.edition.composition.year))
		if(self.edition.name != None):
			print("Edition: " + self.edition.name)
		print("Editor: " + editorToPrint)
		for voice in self.edition.composition.voices:
			if(voice.name != None):
				print("Voice" + str(voiceNumber) + ":" + voice.name)
			if(voice.range != None):
				print("Range" + str(voiceNumber) + ":" + voice.range)
			voiceNumber = voiceNumber + 1
		if(self.partiture):
			print("Partiture: yes")
		else:
			print("Partiture: no")
		if(self.edition.composition.incipit != None):
			print("Incipit: " + self.edition.composition.incipit)
		print("")
		
	def composition(self):
		return self.edition.composition