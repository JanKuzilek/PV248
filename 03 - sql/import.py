import sys
import dataLoader
import databaseHelper

dataFilename = sys.argv[1]
databaseFilename = sys.argv[2]

databaseHelper.createDb(databaseFilename)

for printRecord in dataLoader.load(dataFilename):
	compId = databaseHelper.insertComposition(printRecord.composition())
	editId = databaseHelper.insertEdition(printRecord.edition, compId)
	databaseHelper.insertPrint(printRecord, editId)

databaseHelper.commit()
databaseHelper.close()
