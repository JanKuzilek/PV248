import sys
import sqlite3
import json
import scorelib

inputPrintNumber = sys.argv[1]

listOfAuthors = []

conn = sqlite3.connect( "scorelib.dat" )
cur = conn.cursor()

for row in cur.execute(
'''SELECT person.name,person.born,person.died FROM person
JOIN score_author ON person.id = score_author.composer
JOIN edition ON edition.score = score_author.score
JOIN print ON print.edition = edition.id
WHERE print.id = ?''', (inputPrintNumber,)
):
	listOfAuthors.append(scorelib.Person(row[0],row[1],row[2]))

def serialize(obj):
    return obj.__dict__

print(json.dumps(listOfAuthors, default = serialize, indent = 2, ensure_ascii = False))