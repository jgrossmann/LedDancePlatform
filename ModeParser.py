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
            self.modes['randsquares'] = 'default=True'

    
    def separateModes(self):
        argsList = " ".join(self.args)
        modeIndex = argsList.find("--",0,len(argsList))
        tempArgsList = argsList
        mode = "default"
        if(modeIndex != -1):
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
                if(mode[0] in self.availModes):
                    self.modes[mode[0]] = "default=True"
            else:
                if(mode[0] in self.availModes):
                    self.modes[mode[0]] = ",".join(mode[1:])

        if(len(self.modes.items()) == 0):
            self.modes['randsquares'] = "default=True"
                
        
    def parseServerData(self, data):
        """
        If kill command, send false to kill app otherwise parse into a
        mode and set self.modes and return self.modes.items()[0]
        """
        if(data == "kill"):
            return False
        mode = data.split(" ",1)
        if(len(mode) == 1):
            self.modes= {mode[0]:"default=True"}
        elif(len(mode) == 2):
            if(mode[1].count("'") > 2 or mode[1].count('"') > 2):
                return self.modes.items()[0]
            else:
                self.modes = {mode[0]:mode[1]}
        return self.modes.items()[0]

if __name__ == "__main__":
    parser = ModeParser(sys.argv, ["thetachi","bassring"])
    print parser.modes
