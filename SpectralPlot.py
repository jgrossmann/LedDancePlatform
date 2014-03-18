import matplotlib.pyplot as plt
import pylab
import time
from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
import sys
from pyqtgraph.ptime import time


class SpectralPlot(object):
    def __init__(self, sampSize, freq):
        self.app = QtGui.QApplication([])
        self.sampSize = sampSize
        self.freq = freq/2
        self.bin = self.freq/sampSize
        self.xarray = []
        for i in xrange(sampSize):
            self.xarray.append(i*self.bin)
        self.xarray = self.xarray[:len(self.xarray)/2]
        p = pg.plot()
        p.setWindowTitle('Spectral Analyzer')
        p.setRange(QtCore.QRectF(0, 0, self.freq, 100)) 
        p.setLabel('bottom', 'Frequency', units='Hz')
        p.setLabel('left', 'Amplitude', untis = 'dB')
        self.p = p
        self.curve = self.p.plot()

    def update(self, data):
        
        self.curve.setData(self.xarray, data)
        self.app.processEvents()  ## force complete redraw for every plot



if __name__ == "__main__":
    main()
