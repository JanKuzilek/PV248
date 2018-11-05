import numpy
import sys

fileName = sys.argv[1]
file = open(fileName, 'r', encoding='utf-8')

sortedVariables = []
variables = []
equations = []
results = []

for line in file:
	splittedLine = line.split(" ")
	for part in splittedLine:
		letter = "".join(filter(str.isalpha, part))
		if(letter not in variables):
			variables.append(str(letter))
	
	variables.remove("")
	sortedVariables = sorted(variables)
	
file.seek(0)

for line in file:
	equation = [0] * len(sortedVariables)
	splittedLine = line.split(" ")
	nextValueIsNegative = False
	nextIsLast = False
	
	for part in splittedLine:
		if(part == ""):
			continue
		elif(part == "+"):
			nextValueIsNegative = False
		elif(part == "-"):
			nextValueIsNegative = True
		elif(part == "="):
			nextIsLast = True
			nextValueIsNegative = False
		elif(nextIsLast):
			results.append(int(part))
		else:
			index = sortedVariables.index("".join(filter(str.isalpha, part)))
			numberAsStr = "".join(filter(str.isnumeric, part))
			number = 1
			if(numberAsStr != ""):
				number = int(numberAsStr)
			if(nextValueIsNegative):
				equation[index] = 0 - number
			else:
				equation[index] = number
	
	equations.append(equation)

numpyMatrixEquations = numpy.asmatrix(equations)

rightSideSquare = []
for result in results:
	listOfLists = []
	listOfLists.append(result)
	rightSideSquare.append(listOfLists)
	
augmentedMatrix = numpy.concatenate((numpyMatrixEquations, rightSideSquare), axis=1)

matrixRank = numpy.linalg.matrix_rank(numpyMatrixEquations)
augmentedMatrixRank = numpy.linalg.matrix_rank(augmentedMatrix)

if(matrixRank != augmentedMatrixRank):
	print("no solution")
elif(matrixRank < len(sortedVariables)):
	print("solution space dimension: " + str(len(sortedVariables) - matrixRank))
else:
	stringToBePrinted = "solution: "
	index = 0
	for res in numpy.linalg.solve(equations, results):
		stringToBePrinted = stringToBePrinted + sortedVariables[index] + " = " + str(res) + ", "
		index = index + 1
	print(stringToBePrinted[:-2])
	