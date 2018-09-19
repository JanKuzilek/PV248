import sys
import re

authorsDictionary = {}
centuriesDictionary = {}
file = sys.argv[1]

if(sys.argv[2] == 'composer'):
	r = re.compile(r"Composer: (.+)")
	for line in open(file, 'r', encoding = "utf-8"):
		m = r.match(line)
		if(m is None):
			continue

		authors = m.group(1).split(';')

		for author in authors:
			rBrackets = re.compile(r'\((.*)\)')
			mBrackets = rBrackets.search(author)
			if(mBrackets):
				if("-" in mBrackets.group(1)):
					author = author.replace("(" + mBrackets.group(1) + ")",'')
			
			author = author.strip()

			if(author in authorsDictionary.keys()):
				authorsDictionary[author] = authorsDictionary[author] + 1
			else:
				authorsDictionary[author] = 1

	for key, value in authorsDictionary.items():
		if(value > 0):
			print(str(key) + ": " + str(value))

elif(sys.argv[2] == 'century'):
	r = re.compile(r"Composition Year: (..+)")
	for line in open(file, 'r', encoding = "utf-8"):
		m = r.match(line)
		if(m is None):
			continue
		
		year = 0
		if('century' in m.group(1)):
			year = 	re.findall(r'\d{2}', str(m.group(1)))
			if len(year) > 0:
				finalYear = str(int(year[0]) * 100 - 1) 
		else:
			year = re.findall(r'\d{4}', str(m.group(1)))
			if len(year) > 0:
				finalYear = year[0]

		century = (int(float(finalYear .strip())) // 100) + 1

		if(century in centuriesDictionary.keys()):
			centuriesDictionary[century] = centuriesDictionary[century] + 1
		else:
			centuriesDictionary[century] = 1

	for key, value in centuriesDictionary.items():
		print(str(key) + ": " + str(value))