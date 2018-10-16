import sqlite3

conn = None
cur = None

def createDb(databaseFilename):
	global conn
	conn = sqlite3.connect( databaseFilename )
	global cur
	cur = conn.cursor()
	cur.executescript(open('scorelib.sql', 'r').read())

def commit():
	conn.commit()

def close():
	conn.close()
	
def insertPerson(person):
	if(person.name == None):
		return 0

	cur.execute('SELECT * FROM person WHERE name=?', (person.name,))
	row = cur.fetchone()

	if(row == None):
		cur.execute('INSERT INTO person (born, died, name) VALUES (?, ?, ?)', (person.born, person.died, person.name))
	else:
		born = row[1]
		died = row[2]
		
		if(person.born != None):
			born = person.born
		if(person.died != None):
			died = person.died
		
		cur.execute('UPDATE person SET born=?, died=? WHERE name=?', (born, died, person.name))
		cur.execute('SELECT * FROM person WHERE name=?', (person.name,))
		row = cur.fetchone()
		return row[0]
		
	return cur.lastrowid

def insertComposition(composition):
	listOfAuthorsId = []
	listToControl = []
	
	listOfVoices = []
	listOfVoicesToTest = []
	
	number = 1
	for voice in composition.voices:
		if(voice != None and (voice.name != None or voice.range != None)):
			listOfVoices.append((number, voice.name, voice.range))
		number = number + 1
		
	for person in composition.authors:
		authId = insertPerson(person)
		if(authId != 0):
			listOfAuthorsId.append(authId)

	for row in cur.execute('SELECT * FROM score'):
		if(row[1] == composition.name and row[2] == composition.genre and row[3] == composition.key and row[4] == composition.incipit and row[5] == composition.year):
			for controlRow in cur.execute('SELECT * FROM score_author WHERE score=?', (row[0],)):
				listToControl.append(controlRow[2])
			if(set(listOfAuthorsId) == set(listToControl)):
				for controlRowVoice in cur.execute('SELECT * FROM voice WHERE score=?', (row[0],)):
					listOfVoicesToTest.append((controlRowVoice[1], controlRowVoice[4], controlRowVoice[3]))
				if(set(listOfVoices) == set(listOfVoicesToTest)):
					return row[0]
	
	cur.execute('INSERT INTO score (name, genre, key, incipit, year) VALUES (?, ?, ?, ?, ?)', (composition.name, composition.genre, composition.key, composition.incipit, composition.year))
	compId = cur.lastrowid
	
	for id in listOfAuthorsId:
		insertScoreAuthor(id, compId)
		
	counter = 1
	for voice in composition.voices:
		if(voice != None and (voice.name != None or voice.range != None)):
			insertVoice(voice, compId, counter)
		counter = counter + 1
		
	return compId

def insertVoice(voice, compId, number):
	for row in cur.execute('SELECT * FROM voice'):
		if(row[1] == number and row[2] == compId and row[3] == voice.range and row[4] == voice.name):
			return
		
	cur.execute('INSERT INTO voice (number, score, range, name) VALUES (?, ?, ?, ?)',(number, compId, voice.range, voice.name))
		
def insertEdition(edition, compId):
	listOfEditorsId = []
	listToControl = []
	for person in edition.authors:
		editId = insertPerson(person)
		if(editId != 0):
			listOfEditorsId.append(editId)
			
	for row in cur.execute('SELECT * FROM edition'):
		if(row[1] == compId and row[2] == edition.name):
			for controlRow in cur.execute('SELECT * FROM edition_author WHERE edition=?', (row[0],)):
				listToControl.append(controlRow[2])
			if(set(listOfEditorsId) == set(listToControl)):
				return row[0]
							
	cur.execute('INSERT INTO edition (score, name, year) VALUES (?, ?, ?)',(compId, edition.name, None))
	editionId = cur.lastrowid
	
	for id in listOfEditorsId:
		insertEditionAuthor(id, editionId)
	
	return editionId

def insertScoreAuthor(authId, compId):
	for row in cur.execute('SELECT * FROM score_author'):
		if(row[1] == compId and row[2] == authId):
			return
	cur.execute('INSERT INTO score_author (score, composer) VALUES (?, ?)',(compId, authId))
	
def insertEditionAuthor(authId, editionId):
	for row in cur.execute('SELECT * FROM edition_author'):
		if(row[1] == editionId and row[2] == authId):
			return
	cur.execute('INSERT INTO edition_author (edition, editor) VALUES (?, ?)',(editionId, authId))

def insertPrint(p, editId):
	partiture = "Y" if p.partiture else "N"
	cur.execute('INSERT INTO print (id, partiture, edition) VALUES (?, ?, ?)',(p.print_id, partiture, editId))