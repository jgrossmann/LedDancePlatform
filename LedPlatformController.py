"""
Written by John Grossmann
"""

import sys
import numpy
import time
import math
import traceback
from FileRecorder import *
#from MicInRecorder import *
from LEDUpdater import LEDWindow
from ModeParser import *
from AudioAnalyzer import *
from ServerSocektConnection import *




def analyzeAudio():
    #No new audio to analyze
    if(SR.newAudio == False):
        return

    xs,ys = SR.fft()
    fIntervals = []

    #Calls all of the necessary audio analysis functions
    if(mode[0] in platform.bassModes):
        AA.analyzeBass(ys,xs)
            
    if(mode[0] in platform.visualizerModes):
        fIntervals = AA.analyzeFrequencyIntervals(ys,xs)

    AA.analyzeNonBass(ys,xs)
    AA.analyzeIntensity(ys,xs)
    
    
    platform.updateLEDs(fIntervals)
    SR.newAudio=False

if __name__ == "__main__":
    
    #Setup Led graphical window or actual Led platform matrix
    platform = LEDWindow() 
    AA = AudioAnalyzer(platform)
    
    #parses mode input to set mode 
    parser = ModeParser(sys.argv, platform.modes)
    mode = parser.modes.items()[0]
    platform.updateMode(mode)

    #Sets up socket connection to node.js server
    server = ServerSocketConnection("/tmp/Led_Dance_Platform_Server")
    server.connectToSocket()
    for i in xrange(50):
        #Making sure there is no junk on the socket
        data = server.listen(.05)

    #Setup and starts the program main loop
    SR=SwhRecorder()
    SR.setup()
    SR.continuousStart()
    
    #Ends if window is killed
    while platform.killed == False:
        try:
        """
        Mainloop which tries to analyze new audio data if there is new data
        then it very briefly polls the node.js server to see if there is 
        new data. If new data, it should be parsed into mode form and 
        the dance platform updater should be notified.
        """

            analyzeAudio()
            data = server.listen(.01)

            if(data):
                data = parser.parseServerData(data)
                if(parser.parseServerData(data) == False):
                    #if returns False, kill was called from server
                    #otherwise data should be updated appropriately
                    break
                platform.updateMode(data)
        except:
            print traceback.format_exc()
            SR.continuousEnd()
            SR.close()
            sys.exit("Killing App")

    #Kill threads, cleanup, exit program   
    SR.continuousEnd()
    server.disconnectSocket()
    SR.close()
    sys.exit("Killing App")
