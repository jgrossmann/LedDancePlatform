"""
Frequency bands from FFT:
    Use real_fft to eliminate effort of making imaginary part
    Effective Frequency max is Sample rate / 2
    Each bin is a frequency range starting: n * samplerate / numBins
    10log10(FFT bin value) gives energy in dB of freq range. this is
    efficient way to find peaks which correspond to tones in audio.

    Numpy has a hamming function to make peaks more profound. Test and
    check before definitely using.

    Also look into just finding volume spikes in audio using audioop?

    MAKE SURE TO TEST GPU PROCESSING WITH FFT! ALSO WITH MATRIX MATH!
"""
import time
from LEDUpdater import LEDWindow
import LEDUpdater
from struct import unpack
import wave
import numpy as np
import alsaaudio as aa
import smbus
import pyaudio as pa
import aubio
from SpectralPlot import SpectralPlot

def main():
    #Creates the 8x8 LED window
    window = LEDWindow()
    
    matrix = [0,0,0,0,0,0,0,0]
    dataPoints = len(matrix)
    power = []
    weighting = [2,2,8,8,16,32,64,64]
    avgLen = 10
    peaksIndex = 0
    peaks = np.zeros(shape=(dataPoints,avgLen)) - 1
    averages = np.zeros(shape=(dataPoints,2))
        
    
    # Set up audio
    wavfile = wave.open('/home/john/LedDancePlatform/pony.wav', 'r')
    #wavfile = wave.open('/home/pi/LedDancePlatform/pony.wav','r')
    sample_rate = wavfile.getframerate()
    print sample_rate
    no_channels = wavfile.getnchannels()
    chunk       = 2048 # Use a multiple of 8
    output = aa.PCM(aa.PCM_PLAYBACK, aa.PCM_NORMAL)
    output.setchannels(no_channels)
    output.setrate(sample_rate)
    output.setformat(aa.PCM_FORMAT_S16_LE)
    output.setperiodsize(chunk)

    #graphs audio spectrum
    #comment this out along with update code in calculate_levels
    spectrum = SpectralPlot(chunk, sample_rate)
    

    # Return power array index corresponding to a particular frequency
    def piff(val):
       return int(2*chunk*val/sample_rate)

    def rolling_window(a, window):
        shape = a.shape[:-1] + (a.shape[-1] - window + 1, window)
        strides = a.strides + (a.strides[-1],)
        return np.lib.stride_tricks.as_strided(a, shape=shape, strides=strides)


    """   
    def avgPeak(peaks, newpeak, index, avgLen):
        peaks[index] = newpeak
        index = (index+1) % avgLen
        return peaks
    """
    def calculate_levels(data, chunk,sample_rate,peaks,
                        peaksIndex, dataPoints, avgLen, averages,
                        spectrum):
       #global matrix
       # Convert raw data (ASCII string) to numpy array
       data = data.astype(np.int)
       #data = unpack("%dh"%(len(data)/2),data)
       energy = numpy.dot(data,data)/float(0xffffffff)

       energy_avg = averages
       
       
       data = np.array(data, dtype='h') * np.hanning(chunk*2)
       #data = np.hamming(2*chunk)
       # Apply FFT - real data
       fourier=np.fft.rfft(data)
       # Remove last element in array to make it the same size as chunk
       fourier=np.delete(fourier,len(fourier)-1)
       # Find average 'amplitude' for specific frequency ranges in Hz
       #power = 10*np.log10(np.abs(fourier)+1e-20)
       power = np.abs(fourier)+1e-20
       power = power/100000
       power = power[:len(power)/2]
       #updates spectral graph
       spectrum.update(power)
        
       fRange = (chunk/(dataPoints))
       
       for i in xrange(dataPoints):
          maxval = np.amax(power[(i*fRange/2):
                                 (fRange*(i+1)/2)],-1)
          peaks[i][peaksIndex] = maxval
          if(i == 0):
            print maxval
          if(maxval > averages[i][0] + 5):
            averages[i][1] = 1
          else:
            averages[i][1] = 0
       avgList = np.mean(np.mean(rolling_window(peaks,avgLen),
                               -1),-1)
       for j in xrange(dataPoints):
           averages[j][0] = avgList[j]
       #matrix = avgList/10
       
     
       
       #for i in xrange(dataPoints):
    

       

       """  
       matrix[0]= int(np.mean(power[piff(0)    :piff(156):1]))
       matrix[1]= int(np.mean(power[piff(156)  :piff(313):1]))
       matrix[2]= int(np.mean(power[piff(313)  :piff(625):1]))
       matrix[3]= int(np.mean(power[piff(625)  :piff(1250):1]))
       matrix[4]= int(np.mean(power[piff(1250) :piff(2500):1]))
       matrix[5]= int(np.mean(power[piff(2500) :piff(5000):1]))
       matrix[6]= int(np.mean(power[piff(5000) :piff(10000):1]))
       matrix[7]= int(np.mean(power[piff(10000):piff(20000):1]))
       # Tidy up column values for the LED matrix
       matrix=np.divide(np.multiply(matrix,weighting),1000000)
       """
       # Set floor at 0 and ceiling at 8 for LED matrix
       #matrix=np.clip(matrix,0,8)
      #return matrix.astype(int)
       return averages


    # Process audio file   
    print "Processing....."
    data = wavfile.readframes(chunk)
    print data
    while data!='':
        output.write(data)   
        averages=calculate_levels(data, chunk,sample_rate, peaks, peaksIndex,dataPoints, avgLen, averages, spectrum)
        peaksIndex = (peaksIndex+1)%avgLen
        #window.turnOffLEDs()
        window.updateLEDs(averages, "thetachi")   
        data = wavfile.readframes(chunk)


    


if __name__ == "__main__":
    main()


