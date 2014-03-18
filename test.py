import sys
import time

class ModeParser(object):
    def __init__(self, args, availModes):
        self.modes = {}
        self.availModes = availModes
        if(len(args)>1):
            self.args = args[1:]
            self.separateModes()
        else:   
            self.modes['default'] = 'randsquares'

    
    def separateModes(self):
        argsList = " ".join(self.args)
        modeIndex = argsList.find("--",0,len(argsList))
        tempArgsList = argsList
        mode = "default"
        curtime = time.time()
        while(modeIndex != -1):
            if(time.time() - curTime > 2):
                #2 second timeout
                self.modes = {'default':'randsquares'}
                return
            tempArgsList = tempArgsList[modeIndex:]
            modeIndex = argsList.find("--",2,len(tempArgsList))
            if(modeIndex != -1):
                mode = tempArgsList[2:modeIndex+2].split(",")
                if(len(mode) == 1):
                    mode = tempArgsList[2:modeIndex+2].split(" ")
            else:
                mode = tempArgsList[2:].split(",")
                if(len(mode) == 1):
                    mode = tempArgsList[2:].split(" ")
            
            if(len(mode) == 1):
                if(mode in self.availModes):
                    self.modes[mode] = "default"
            else:
                if(mode[0] in self.availModes):
                    self.modes[mode[0]] = ",".join(mode[1:])

        if(len(self.modes.items()) == 0):
            self.modes['default'] = "randsquares"
                
        
