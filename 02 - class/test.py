import sys
import re
import scorelib

file = sys.argv[1]

def createPerson(composerString):
	if(composerString == None or composerString == ""):
		return scorelib.Person(None, None, None)
	
	name = None
	born = None
	died = None

	name = re.sub(r'\(.*\d.*\)', '', composerString).strip()
	
	rBrackets = re.compile(r'\((.*\d.*)\)')
	mBrackets = rBrackets.search(composerString)
	if(mBrackets != None):
		findYears = re.findall(r'\d{4}', mBrackets.group(1))
		
		if(len(findYears) == 2):
			born = findYears[0]
			died = findYears[1]
		else:
			rBorn = re.compile( r"(\d{4}-)")
			rDied = re.compile( r"(-\d{4})")
			mBorn = rBorn.match(mBrackets.group(1))
			mDied = rDied.match(mBrackets.group(1))
			if(mBorn):
				born = int(findYears[0])
			elif(mDied):
				died = int(findYears[0])
			elif("*" in mBrackets.group(1)):
				born = int(findYears[0])
			elif("+" in mBrackets.group(1)):
				died = int(findYears[0])
		
	return scorelib.Person(name, born, died)
		
def separateYear(yearString):
	years = re.findall(r'\d{4}', yearString)
	if(len(years) > 0):
		return int(years[0])
	return None
		
def createVoice(voiceString):
	if(voiceString == None or voiceString == ""):
		return scorelib.Voice(None, None)
	
	name = None
	range = None
	
	rRange = re.compile( r"(.+--.+?)[,;] (.*)")
	mRange = rRange.search(voiceString)
	
	if(mRange):
		range = mRange.group(1)
		name = mRange.group(2)
	else:
		name = voiceString
	
	return scorelib.Voice(name, range)	
	
def getPartiture(value):
	rTrue = re.compile(r'.*yes.*')
	mTrue = rTrue.match(value)
	if(mTrue):
		return True
	return False
	
def processRecord(record):
	print_id, title, genre, key, compositionYear, editionName, incipit = None, None, None, None, None, None, None
	composers, editors, voices = [], [], []
	partiture = False
				
	for text in record:	
		splitted = text.split(":")
		element = splitted[0]
		value = None
		if(len(splitted) > 1):
			value = splitted[1].strip()
		if(value == None):
			continue
		
		if("Print" in element):
			print_id = int(value)
		if("Composer" in element):
			for composerString in value.split(";"):
				composers.append(createPerson(composerString.strip()))
		if("Title" in element):
			title = value
		if("Genre" in element):
			genre = value
		if("Key" in element):
			key = value
		if("Composition" in element):
			compositionYear = separateYear(value)
		if("Edition" in element):
			editionName = value
		if("Editor" in element):
			for editorString in value.split(";"):
				editors.append(createPerson(editorString.strip()))
		if("Voice" in element):
			voices.append(createVoice(value))
		if("Partiture" in element):
			partiture = getPartiture(value)
		if("Incipit" in element and incipit == None):				
			incipit = value
	composition = scorelib.Composition(title, incipit, key, genre, compositionYear, voices, composers)
	edition = scorelib.Edition(editionName, composition, editors)
	printRecord = scorelib.Print(edition, print_id, partiture)
	
	return printRecord
	
def load(filename):
	listOfPrints = []
	record = []
	
	for line in open(filename, 'r', encoding = "utf-8"):
		if(line != '\n'):
			record.append(line)
		else:
			if(len(record) == 0):
				continue
			listOfPrints.append(processRecord(record))
			record = []
	
	listOfPrints.append(processRecord(record))
	return listOfPrints

for item in load(file):
	item.format()