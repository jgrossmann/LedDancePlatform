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
        self.file = wave.open('/home/john/LedDancePlatform/pony.wav', 'r')
        self.RATE=44100
        #self.RATE = self.file.getframerate()
        print self.RATE
        self.nChannels = self.file.getnchannels()
        self.BUFFERSIZE=2**10 #2048 is a good buffer size
        self.secToRecord=.1
        self.threadsDieNow=False
        self.newAudio=False
        output = aa.PCM(aa.PCM_PLAYBACK, aa.PCM_NORMAL)
        output.setchannels(self.nChannels)
        output.setrate(self.RATE)
        output.setformat(aa.PCM_FORMAT_S16_LE)
        output.setperiodsize(self.BUFFERSIZE)
        self.audioString = ""
        self.output = output
        self.bassaverages = numpy.zeros(16)
        self.averages = numpy.zeros(32)
        self.bassavgIndex = 0
        self.avgIndex = 0
        self.power = numpy.zeros(16)
        self.powerIndex = 0
        self.intensity = 0
        self.intensityAvg = numpy.zeros(16)
        self.longIntensityAvg = numpy.zeros(32)
        self.longIntensityAvgIndex=0
        self.intensityIndex = 0
        
    def setup(self):

        self.buffersToRecord=int(self.RATE*self.secToRecord/self.BUFFERSIZE)
        if self.buffersToRecord==0: self.buffersToRecord=1
        self.samplesToRecord=int(self.BUFFERSIZE*self.buffersToRecord)
        self.chunksToRecord=int(self.samplesToRecord/self.BUFFERSIZE)
        self.secPerPoint=1.0/self.RATE
        
        self.p = pyaudio.PyAudio()
        #use recorder.py file to use an input stream instead of wave file
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
        #self.output.write(audioString)
        self.audioString+=audioString
        return numpy.fromstring(audioString,dtype=numpy.int16)
        
    def record(self,forever=True):
        """record secToRecord seconds of audio."""
        while True:
            if self.threadsDieNow: break
            for i in range(self.chunksToRecord):
                self.audio[i*self.nChannels*self.BUFFERSIZE:(i+1)*self.nChannels*self.BUFFERSIZE]=self.getAudio()
            self.newAudio=True 
            self.audio *= numpy.hanning(len(self.audio))
            self.output.write(self.audioString)
            self.audioString = ""
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
        
    def fft(self,data=None,trimBy=1.5,logScale=False,divBy=2000):
        if data==None: 
            data=self.audio.flatten()
        left,right=numpy.split(numpy.abs(numpy.fft.fft(data)),2)
        ys=numpy.add(left,right[::-1])
        if logScale:
            ys=numpy.multiply(20,numpy.log10(ys))
        xs=numpy.arange(self.BUFFERSIZE/2,dtype=float)
        if trimBy:
            i=int((self.BUFFERSIZE/2)/trimBy)
            ys=ys[:i]
            xs=xs[:i]
        xs*=self.RATE/(self.BUFFERSIZE * (4096/self.BUFFERSIZE))
        if divBy:
            ys=ys/float(divBy)
        return xs,ys
    
    ### VISUALIZATION ###
    
    def plotAudio(self):
        """open a matplotlib popup window showing audio data."""
        pylab.plot(self.audio.flatten())
        pylab.show()        
            
