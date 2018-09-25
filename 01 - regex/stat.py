import sys
import re

composersDictionary = {}
centuriesDictionary = {}
file = sys.argv[1]

if(sys.argv[2] == 'composer'):
	rComposer = re.compile(r"Composer: (.+)")
	
	for line in open(file, 'r', encoding = "utf-8"):
		mComposer = rComposer.match(line)
		if(mComposer is None):
			continue

		composers = mComposer.group(1).split(';')

		for composer in composers:
			rBrackets = re.compile(r'\((.*\d.*)\)')
			mBrackets = rBrackets.search(composer)
			if(mBrackets):
				composer = composer.replace("(" + mBrackets.group(1) + ")",'')
			
			composer = composer.strip()

			if(composer in composersDictionary.keys()):
				composersDictionary[composer] = composersDictionary[composer] + 1
			else:
				composersDictionary[composer] = 1

	for key, value in composersDictionary.items():
		print(str(key) + ": " + str(value))

elif(sys.argv[2] == 'century'):
	rComposed = re.compile(r"Composition Year: (..+)")
	
	for line in open(file, 'r', encoding = "utf-8"):
		mComposed = rComposed.match(line)
		if(mComposed is None):
			continue
		
		composed = str(mComposed.group(1))
		year = 0
		century = 0

		if('century' in composed):
			century = int(re.findall(r'\d{2}', composed)[0])
		else:
			year = int(re.findall(r'\d{4}', composed)[0])
			if(year % 100 == 0):
				century = year // 100
			else:
				century = year // 100 + 1

		if(century in centuriesDictionary.keys()):
			centuriesDictionary[century] = centuriesDictionary[century] + 1
		else:
			centuriesDictionary[century] = 1

	for key, value in centuriesDictionary.items():
		print(str(key) + "th century: " + str(value))