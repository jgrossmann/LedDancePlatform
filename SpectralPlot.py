import matplotlib.pyplot as plt
import pylab
import time

class SpectralPlot(object):
    def __init__(self, sampSize, freq):
        self.sampSize = sampSize
        self.freq = freq/2
        self.bin = self.freq/sampSize
        self.xarray = []
        for i in xrange(sampSize):
            self.xarray.append(i*self.bin) 
        self.window = plt.plot()
        self.window.xlabel("Frequency")
        self.window.ylabel("dB")
        self.window.show()
                
    def plot(self, data):
        self.window.plot(self.xarray, data)
        self.window.show()

def main():
    win = plt
    win.ion()
    win.plot([1,2,3], [4,5,8])
    win.xlabel("frequency")
    win.ylabel("dB")
    win.draw()
    time.sleep(1)
    while True:
        print "plot"
        win.cla()
        win.plot([1,2,3],[8,10,13])
        win.draw()

if __name__ == "__main__":
    main()
