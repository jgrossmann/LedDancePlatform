import ui_plot
import sys
import numpy
from PyQt4 import QtCore, QtGui
import PyQt4.Qwt5 as Qwt
from recorderWav import *
import alsaaudio as aa
import time
from LEDUpdater import LEDWindow
from ModeParser import ModeParser
import math


def plotSomething():
    if SR.newAudio==False: 
        return
    xs,ys=SR.fft()
    arr = numpy.zeros(8)
    SR.power[SR.powerIndex] = (ys**2).sum()
    SR.powerIndex +=1
    if(SR.powerIndex >= len(SR.power)):
        SR.powerIndex = 0
    bassstd = SR.bassaverages.std()
    SR.bassaverages[SR.bassavgIndex] = numpy.amax(ys[:len(ys)/17])
    SR.bassavgIndex += 1
    bassmean = SR.bassaverages.mean()
    std = SR.averages.std()
    mean = SR.averages.mean()
    if(ys[len(ys)/17:].mean() > mean + std):
        platform.updateSquares = True
    SR.averages[SR.avgIndex] = ys[len(ys)/17:].mean()
    SR.avgIndex += 1
    if(SR.avgIndex >= len(SR.averages)):
        SR.avgIndex = 0

    if(bassstd + (bassmean*1.1)  + mean< numpy.amax(ys[:len(ys)/17])):
        if(bassstd > .5):
            platform.bass = True

    if(SR.bassavgIndex >= len(SR.bassaverages)):
        SR.bassavgIndex = 0 
    arr = []
    #arr.append(int(math.log10((ys[:len(ys)/22.67]**2).sum()/10)))
    arr.append(int(math.log10(numpy.amax(ys[:len(ys)/22.67]**2)+1)))
    #arr.append(int(math.log10((ys[len(ys)/22.67:len(ys)/9.7]**2).sum()/10)))
    arr.append(int(math.log10(numpy.amax(ys[len(ys)/22.67:len(ys)/9.7]**2)+1)))
    #arr.append(int(math.log10((ys[len(ys)/9.7:len(ys)/5.2]**2).sum()/10)))
    arr.append(int(math.log10(numpy.amax(ys[len(ys)/9.7:len(ys)/5.2]**2)+1)))
    #arr.append(int(math.log10((ys[len(ys)/5.2:len(ys)/3.4]**2).sum()/10)))
    arr.append(int(math.log10(numpy.amax(ys[len(ys)/5.2:len(ys)/3.4]**2)+1)))
    #arr.append(int(math.log10((ys[len(ys)/3.4:len(ys)/2.43]**2).sum()/10)))
    arr.append(int(math.log10(numpy.amax(ys[len(ys)/3.4:len(ys)/2.43]**2)+1)))
    #arr.append(int(math.log10((ys[len(ys)/2.43:len(ys)/1.79]**2).sum()/10)))
    arr.append(int(math.log10(numpy.amax(ys[len(ys)/2.43:len(ys)/1.79]**2)+1)))
    #arr.append(int(math.log10((ys[len(ys)/1.79:len(ys)/1.31]**2).sum()/10)))
    arr.append(int(math.log10(numpy.amax(ys[len(ys)/1.79:len(ys)/1.31]**2)+1)))
    #arr.append(int(math.log10((ys[len(ys)/1.31:]**2).sum()/10)))
    arr.append(int(math.log10(numpy.amax(ys[len(ys)/1.31:]**2)+1)))
    for i in xrange(len(arr)):
        if(arr[i] > 8):
            arr[i] = 8
    SR.intensityAvg[SR.intensityIndex] = int(math.log10((ys**2).sum()+1))
    SR.longIntensityAvg[SR.longIntensityAvgIndex] = math.log10((ys**2).sum()+1)
    if(SR.longIntensityAvg[SR.longIntensityAvgIndex] > max(SR.longIntensityAvg)):
        platform.visualizeFreq = 0
    elif(SR.longIntensityAvg[SR.longIntensityAvgIndex] < min(SR.longIntensityAvg)):
        platform.visualizeFreq = 10
    else:
        platform.visualizeFreq = int(10 - ((SR.longIntensityAvg[SR.longIntensityAvgIndex] - min(SR.longIntensityAvg)) / (max(SR.longIntensityAvg) - min(SR.longIntensityAvg))) * 10)
    SR.intensityIndex += 1
    SR.longIntensityAvgIndex+=1
    if(SR.intensityIndex >= len(SR.intensityAvg)):
        SR.intensityIndex = 0
    if(SR.longIntensityAvgIndex >= len(SR.longIntensityAvg)):
        SR.longIntensityAvgIndex = 0
    if(platform.curMode[0] == "randsquares"):
        if(int(math.log10((ys**2).sum())) > SR.intensityAvg.mean() + SR.intensityAvg.std()):
            platform.updateSquares = True
    print arr
    platform.updateLEDs(arr)
    c.setData(xs,ys)
    uiplot.qwtPlot.replot()
    SR.newAudio=False

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    
    win_plot = ui_plot.QtGui.QMainWindow()
    uiplot = ui_plot.Ui_win_plot()
    uiplot.setupUi(win_plot)
    uiplot.btnA.clicked.connect(plotSomething)
    #uiplot.btnB.clicked.connect(lambda: uiplot.timer.setInterval(100.0))
    #uiplot.btnC.clicked.connect(lambda: uiplot.timer.setInterval(10.0))
    #uiplot.btnD.clicked.connect(lambda: uiplot.timer.setInterval(1.0))
    c=Qwt.QwtPlotCurve()  
    c.attach(uiplot.qwtPlot)
    
    uiplot.qwtPlot.setAxisScale(uiplot.qwtPlot.yLeft, 0,20000)
    
    uiplot.timer = QtCore.QTimer()
    uiplot.timer.start(1.0)
    
    win_plot.connect(uiplot.timer, QtCore.SIGNAL('timeout()'), plotSomething) 
    
    platform = LEDWindow()  
    parser = ModeParser(sys.argv, platform.modes)
    platform.updateMode(parser.modes.items()[0])

    SR=SwhRecorder()
    SR.setup()
    SR.continuousStart()

    ### DISPLAY WINDOWS
    win_plot.show()
    code=app.exec_()
    SR.close()
    sys.exit(code)
