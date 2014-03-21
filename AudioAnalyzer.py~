"""
Written by John Grossmann
"""

import sys
import numpy
import math


class AudioAnalyzer(object):

    def __init__(self, platform):
        #Initialize variables/arrays to keep track of audio stats
        self.bassaverages = numpy.zeros(16)
        self.averages = numpy.zeros(32)
        self.bassavgIndex = 0
        self.avgIndex = 0
        self.intensity = 0
        self.intensityAvg = numpy.zeros(16)
        self.longIntensityAvg = numpy.zeros(64)
        self.longIntensityAvgIndex=0
        self.intensityIndex = 0
        self.platform = platform


    def analyzeBass(self,ys,xs):
        bassStd= self.bassaverages.std()
        bassMean = self.bassaverages.mean()
        maxBass = numpy.amax(ys[:len(ys)/(xs[len(xs)-1]/200)])
        self.bassaverages[self.bassavgIndex] = maxBass
        self.bassavgIndex += 1
        if(self.bassavgIndex >= len(self.bassaverages)):
            self.bassavgIndex = 0 

        #Update for any mode where event happens on bass hit
        if(bassStd + (bassMean*1.3) < maxBass):
            if(bassStd > .5):
                self.platform.bass = True


    def analyzeNonBass(self,ys,xs):
        std = self.averages.std()
        mean = self.averages.mean()
        curVal = ys[len(ys)/(xs[len(xs)-1]/200):].mean()
        self.averages[self.avgIndex] = curVal
        self.avgIndex += 1
        if(self.avgIndex >= len(self.averages)):
            self.avgIndex = 0 

        #Update for modes which change squares based on average value
        if( curVal > mean + std):
            self.platform.updateSquares = True   

    def analyzeFrequencyIntervals(self,ys,xs):
        numPnts = len(ys)
        maxFreq = xs[len(xs)-1]
        fIntervals = []
        #150hz
        int1 = numPnts/(maxFreq/150.0)
        #350hz
        int2 = numPnts/(maxFreq/350.0)
        #650hz
        int3 = numPnts/(maxFreq/650.0)
        #1000hz
        int4 = numPnts/(maxFreq/1000.0)
        #1400hz
        int5 = numPnts/(maxFreq/1400.0)
        #1900hz
        int6 = numPnts/(maxFreq/1900.0)
        #2600hz
        int7 = numPnts/(maxFreq/2600.0)
        #dont need int8 because use int7 and take the rest

        fIntervals.append(int(math.log10(numpy.amax(ys[:int1]**2)+1)))
        fIntervals.append(int(math.log10(numpy.amax(ys[int1:int2]**2)+1)))
        fIntervals.append(int(math.log10(numpy.amax(ys[int2:int3]**2)+1)))
        fIntervals.append(int(math.log10(numpy.amax(ys[int3:int4]**2)+1)))
        fIntervals.append(int(math.log10(numpy.amax(ys[int4:int5]**2)+1)))
        fIntervals.append(int(math.log10(numpy.amax(ys[int5:int6]**2)+1)))
        fIntervals.append(int(math.log10(numpy.amax(ys[int6:int7]**2)+1)))
        fIntervals.append(int(math.log10(numpy.amax(ys[int7:]**2)+1)))
        for i in xrange(len(fIntervals)):
            if(fIntervals[i] > 8):
                fIntervals[i] = 8
        return fIntervals

    def analyzeIntensity(self,ys,xs):
        curIntensity = math.log10((ys**2).sum()+1)
        longMax = numpy.amax(self.longIntensityAvg)
        longMin = numpy.amin(self.longIntensityAvg)
        self.intensityAvg[self.intensityIndex] = curIntensity
        self.longIntensityAvg[self.longIntensityAvgIndex] = curIntensity
        self.intensityIndex += 1
        self.longIntensityAvgIndex+=1
        if(self.intensityIndex >= len(self.intensityAvg)):
            self.intensityIndex = 0
        if(self.longIntensityAvgIndex >= len(self.longIntensityAvg)):
            self.longIntensityAvgIndex = 0

        #Used for setting speed of visualizer modes
        if(curIntensity > longMax):
            self.platform.visualizeFreq = 0
        elif(curIntensity < longMin):
            self.platform.visualizeFreq = 10
        elif(longMax <= 0):
            self.platform.visualizeFreq = 10
        else:
            self.platform.visualizeFreq = int(10 -((curIntensity - longMin)/((longMax - longMin)*.75)) * 10)
        print self.platform.visualizeFreq
        #Randsquares mode uses intensity average instead of norm avg
        if(self.platform.curMode[0] == "randsquares"):
            if(curIntensity > self.intensityAvg.mean() + self.intensityAvg.std()):
                self.platform.updateSquares = True

