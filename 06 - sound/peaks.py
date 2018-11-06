import sys
import numpy
import wave
import struct

fileName = sys.argv[1]
wave_read = wave.open(fileName, 'rb')

numberOfChannels = wave_read.getnchannels()
framerate = wave_read.getframerate()
sizeOfInput = wave_read.getnframes()

numberOfWindows  = sizeOfInput // framerate

globalLow = -1
globalHigh = -1


for x in range(numberOfWindows):
	windowData = wave_read.readframes(framerate)
	format = str(framerate * numberOfChannels)  + "h"
	unpackedData = struct.unpack(format, windowData)
	
	if(numberOfChannels == 2):
		averageAmplitudesOfStereo = []
		for i in range(0, len(unpackedData), 2):
			averageAmplitudesOfStereo.append((unpackedData[i] + unpackedData[i + 1])/2)
		finalData = numpy.array(averageAmplitudesOfStereo)
	else:
		finalData = numpy.array(unpackedData)
	
	amplitudes = numpy.abs(numpy.fft.rfft(finalData))
	averageOfAmplitudeInWindow = numpy.average(amplitudes)
	peak = 20 * averageOfAmplitudeInWindow
	
	windowHigh = -1
	windowLow = -1
	for index in range(len(amplitudes)):
		if amplitudes[index] > peak:
			if windowLow == -1 or windowLow > index:
				windowLow = index
			if windowHigh == -1 or windowHigh < index:
				windowHigh = index

	if globalLow == -1:
		globalLow = windowLow
	if globalLow > windowLow:
		globalLow = windowLow
	if globalHigh < windowHigh:
		globalHigh = windowHigh

if (globalHigh == -1 and globalLow == -1):
	print("no peaks")
else:
	print("low:", globalLow, "high:", globalHigh)
	
