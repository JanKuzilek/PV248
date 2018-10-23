import sys
import sqlite3
import json
import scorelib

inputComposerNameSubstring = sys.argv[1]

def getPrints(listOfPrintIds):
	prints = []
	
	for id in listOfPrintIds:
		composers = []
		editors = []
		voices = {}
	
		cur.execute('''SELECT print.id, print.partiture, edition.id, edition.name, score.id, score.name, score.incipit, score.key, score.genre, score.year FROM print 
		JOIN edition ON edition.id = print.edition
		JOIN score ON score.id = edition.score WHERE print.id = ? ''', (id,))
		rowMain = cur.fetchone()
		
		editionId = rowMain[2]
		compositionId = rowMain[4]
		
		cur.execute('''SELECT number, range, name FROM voice WHERE score = ? ''', (compositionId,))
		for voice in cur:
			voices[voice[0]] = scorelib.Voice(voice[2], voice[1])
		
		cur.execute('''SELECT name, born, died FROM score_author JOIN person ON person.id = score_author.composer WHERE score_author.score = ? ''', (compositionId,))
		for comp in cur:
			composers.append(scorelib.Person(comp[0], comp[1], comp[2]))
		
		cur.execute('''SELECT name, born, died FROM edition_author JOIN person ON person.id = edition_author.editor WHERE edition_author.edition = ? ''', (editionId,))
		for edi in cur:
			editors.append(scorelib.Person(edi[0], edi[1], edi[2]))
			
		composition = scorelib.Composition(rowMain[5], rowMain[6], rowMain[7], rowMain[8], voices, composers)
		setattr(composition, "composition year", rowMain[9])
		edition = scorelib.Edition(rowMain[3], composition, editors)
		
		if(rowMain[1] == "Y" or rowMain[1] == "y"):
			partiture = True
		else:
			partiture = False
		printInstance = scorelib.Print(edition, partiture)
		setattr(printInstance, "print number", rowMain[0])
		prints.append(printInstance)
	return prints

def serialize(obj):
    return obj.__dict__

dict = {}

conn = sqlite3.connect( "scorelib.dat" )
cur = conn.cursor()
cur2 = conn.cursor()

for rowName in cur.execute('''SELECT person.name FROM person WHERE person.name LIKE ? ''', ('%'+inputComposerNameSubstring+'%',)):
	for rowPrintId in cur2.execute('''SELECT print.id FROM person
JOIN score_author ON person.id = score_author.composer
JOIN edition ON edition.score = score_author.score
JOIN print ON print.edition = edition.id
WHERE person.name = ?''', (rowName[0],)):
		printIds = []
		if(rowName[0] in dict):
			printIds = dict[rowName[0]]
		printIds.append(rowPrintId[0])
		dict[rowName[0]] = printIds
	
dictionaryToBePrinted = {}	
for key, value in dict.items():
	dictionaryToBePrinted[key] = getPrints(value)

print(json.dumps(dictionaryToBePrinted, default = serialize, indent = 2, ensure_ascii = False))