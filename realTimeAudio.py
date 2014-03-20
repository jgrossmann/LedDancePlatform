import ui_plot
import sys
import numpy
from PyQt4 import QtCore, QtGui
import PyQt4.Qwt5 as Qwt
from recorder import *
import alsaaudio as aa
import time
from LEDUpdater import LEDWindow
from ModeParser import ModeParser


def plotSomething():
    if SR.newAudio==False: 
        return
    xs,ys=SR.fft()
    arr = numpy.zeros(8)
    bassstd = SR.bassaverages.std()
    SR.bassaverages[SR.bassavgIndex] = numpy.amax(ys[:len(ys)/18])
    SR.bassavgIndex += 1
    bassmean = SR.bassaverages.mean()
    std = SR.averages.std()
    mean = SR.averages.mean()
    if(ys[len(ys)/18:].mean() > mean + std):
        platform.updateSquares = True
    SR.averages[SR.avgIndex] = ys[len(ys)/18:].mean()
    SR.avgIndex += 1
    if(SR.avgIndex >= len(SR.averages)):
        SR.avgIndex = 0

    if(bassstd + bassmean  + mean< numpy.amax(ys[:len(ys)/18])):
        if(bassstd > 1):
            arr[0] = 1

    if(SR.bassavgIndex >= len(SR.bassaverages)):
        SR.bassavgIndex = 0    
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
