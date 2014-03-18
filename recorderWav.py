import matplotlib
matplotlib.use('TkAgg') # <-- THIS MAKES IT FAST!
import numpy
import scipy
import struct
import pyaudio
import threading
import pylab
import struct
import wave
import alsaaudio as aa

class SwhRecorder:
    """Simple, cross-platform class to record from the microphone."""
    
    def __init__(self):
        """minimal garb is executed when class is loaded."""
        self.file = wave.open('/home/john/LedDancePlatform/AllNightLonger.wav', 'r')
        #self.RATE=48100
        self.RATE = self.file.getframerate()
        print self.RATE
        self.nChannels = self.file.getnchannels()
        self.BUFFERSIZE=2**13 #2048 is a good buffer size
        self.secToRecord=.1
        self.threadsDieNow=False
        self.newAudio=False
        output = aa.PCM(aa.PCM_PLAYBACK, aa.PCM_NORMAL)
        output.setchannels(self.nChannels)
        output.setrate(self.RATE)
        output.setformat(aa.PCM_FORMAT_S16_LE)
        output.setperiodsize(self.BUFFERSIZE)
        self.output = output
        self.bassaverages = numpy.zeros(16)
        self.averages = numpy.zeros(32)
        self.bassavgIndex = 0
        self.avgIndex = 0
        
    def setup(self):
        """initialize sound card."""
        #TODO - windows detection vs. alsa or something for linux
        #TODO - try/except for sound card selection/initiation

       # self.buffersToRecord=int(self.RATE*self.secToRecord/self.BUFFERSIZE)
        self.buffersToRecord = 1
        if self.buffersToRecord==0: self.buffersToRecord=1
        #self.samplesToRecord=int(self.BUFFERSIZE*self.buffersToRecord)
        self.samplesToRecord = 2048
        #self.chunksToRecord=int(self.samplesToRecord/self.BUFFERSIZE)
        self.chunksToRecord = self.buffersToRecord
        self.secPerPoint=1.0/self.RATE
        
        self.p = pyaudio.PyAudio()
        #self.inStream = self.p.open(format=pyaudio.paInt16,channels=1,rate=self.RATE,input=True,frames_per_buffer=self.BUFFERSIZE)
        self.inStream = self.file
        self.xsBuffer=numpy.arange(self.BUFFERSIZE)*self.secPerPoint
        self.xs=numpy.arange(self.chunksToRecord*self.BUFFERSIZE)*self.secPerPoint
        self.audio=numpy.empty((self.chunksToRecord*self.BUFFERSIZE*self.nChannels),dtype=numpy.int16)               
    
    def close(self):
        """cleanly back out and release sound card."""
        self.inStream.close()
        self.p.close(self.inStream)
    
    ### RECORDING AUDIO ###  
    
    def getAudio(self):
        """get a single buffer size worth of audio."""
        audioString=self.inStream.readframes(self.BUFFERSIZE)
        self.output.write(audioString)
        temp = numpy.fromstring(audioString,dtype=numpy.int16)
        temp *= numpy.hanning(len(temp))
        """
        if(self.nChannels > 1):
            monoAudio = numpy.int16([])
            for i in xrange(len(temp)):
                if(i % 2 == 0):
                    monoAudio = numpy.append(monoAudio,temp[i])
            return monoAudio
        """
        return temp
        
    def record(self,forever=True):
        """record secToRecord seconds of audio."""
        while True:
            if self.threadsDieNow: break
            for i in range(self.chunksToRecord):
                self.audio[0:self.nChannels*self.BUFFERSIZE]=self.getAudio()
            self.newAudio=True 
            if forever==False: break
    
    def continuousStart(self):
        """CALL THIS to start running forever."""
        self.t = threading.Thread(target=self.record)
        self.t.start()
        
    def continuousEnd(self):
        """shut down continuous recording."""
        self.threadsDieNow=True

    ### MATH ###
            
    def downsample(self,data,mult):
        """Given 1D data, return the binned average."""
        overhang=len(data)%mult
        if overhang: data=data[:-overhang]
        data=numpy.reshape(data,(len(data)/mult,mult))
        data=numpy.average(data,1)
        return data    
        
    def fft(self,data=None,trimBy=20,logScale=False,divBy=200000):
        if data==None: 
            data=self.audio.flatten()
        left,right=numpy.split(numpy.abs(numpy.fft.fft(data)),2)
        ys=numpy.add(left,right[::-1])
        if logScale:
            ys=numpy.multiply(20,numpy.log10(ys))
        xs=numpy.arange(self.BUFFERSIZE/2,dtype=float)
        if trimBy:
            i=int((self.BUFFERSIZE/2/trimBy))
            ys=ys[:i]
            xs=xs[:i]*self.RATE/self.BUFFERSIZE*20
        if divBy:
            ys=ys/float(divBy)
        print "bassavg",self.bassaverages.mean()
        print "bassstd",self.bassaverages.std()
        print "bassmax",numpy.amax(ys[:len(ys)/8])
        print "bassavg + bassstd",self.bassaverages.mean() + self.bassaverages.std()
        print "avg", self.averages.mean()
        print "std", self.averages.std()
        print "currAvg",ys.mean()
        print "avg + std", self.averages.mean() + self.averages.std()
        return xs,ys
    
    ### VISUALIZATION ###
    
    def plotAudio(self):
        """open a matplotlib popup window showing audio data."""
        pylab.plot(self.audio.flatten())
        pylab.show()        
            