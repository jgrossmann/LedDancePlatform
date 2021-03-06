from Tkinter import *
import random
import time
import sys
from LedSymbols import *

def main():
    window = LEDWindow()
    rgb = 1
    waves = [None for x in xrange(4)]
    color = window.bassBooster
    waves[0] = color
    while True:
        nextcolor = waves[0]
        waves[0] = color
        x = 3
        y = 5
        for i in xrange(len(waves)):
            if(waves[i] != None):
                for j in xrange(x,y):
                    window.w.itemconfigure(window.ledMatrix[x][j],fill=waves[i].color)
                    window.w.itemconfigure(window.ledMatrix[y-1][j],fill=waves[i].color)
                    window.w.itemconfigure(window.ledMatrix[j][x],fill=waves[i].color)
                    window.w.itemconfigure(window.ledMatrix[j][y-1],fill=waves[i].color)
                #nextcolor = waves[i+1]
                window.master.update()
            x-=1
            y+=1
        time.sleep(.5)
        color = color.next
        for i in xrange(len(waves)):
            if(i == 0):
                nextcolor = waves[i]
                waves[i] = color
                continue
            if(waves[i] != None):
                curColor = waves[i]
                waves[i] = nextcolor
                nextcolor = curColor
            else:
                waves[i] = nextcolor
                break
                



class Colors():
    def __init__(self, color, next):
        self.color = color
        self.next = next

class ThetaChiLetter():
    def __init__(self, letter, next):
        self.letter = letter
        self.next = next
        


class LEDWindow():
    def __init__(self):
        self.ledMatrix = [[None for x in xrange(8)]for x in xrange (8)]

        red = Colors("red",None)
        white = Colors("white",red)
        green = Colors("green", white)
        darkorange = Colors("dark orange",green)
        blue = Colors("blue",darkorange)
        yellow = Colors("yellow",blue)
        darkviolet = Colors("dark violet", yellow)
        #purple?
        cyan = Colors("cyan",darkviolet)
        hotpink = Colors("hot pink",cyan)
        darkgreen = Colors("dark green",hotpink)
        red.next = darkgreen
        
        self.colors = []
        color = red
        for i in xrange(10):
            self.colors.append(color.color)
            color = color.next

        theta = ThetaChiLetter("theta", None)
        chi = ThetaChiLetter("chi", theta)
        theta.next = chi

        self.letterMatrix = []
        self.letterWait = 0
        self.newMode = True
        self.bassBooster = red
        self.init = 0
        self.mainColors = red
        self.visualizeFreq = 10
        self.visualizeWait = 0
        self.updateSquares = False
        self.bass = False
        self.thetaChiLetter = theta
        self.visualizeWaves = [None for x in xrange(4)]
        self.master = Tk()
        self.master.wm_title("LED Dance Platform")
        self.master.protocol("WM_DELETE_WINDOW", self.callback)
        self.killed = False
        self.w = Canvas(self.master, height=320, width=320)
        x = 0
        for i in range(320,39,-40):
            y = 0
            for j in range(320,39,-40):
                self.ledMatrix[x][y]=self.w.create_rectangle(i,j,i-40,j-40,outline="black",fill=self.rgbToHex((255,255,255)),width=2)
                y += 1
            x += 1
        self.w.pack()
        self.master.update()
        
##---------IMPORTANT, MUST UPDATE SELF.MODES WITH ADDITIONAL FUNCTIONS IF YOU WANT THE MODES TO BE USABLE!!!!!!-------#####
        self.modes = ["thetachi","bassring","levels","randsquares","visualize1","solidcolor","textdisplay"]
        self.bassModes = ["thetachi","bassring"]
        self.visualizerModes = ["visualize1"]
        self.freqIntervalModes = ["levels"]
        self.curMode = ("randsquares","default=True")
        self.lastMode = None
        self.symbolDict = {'!':exclamation,'.':period,',':comma,'?':question,'$':dollar, '#':pound,'/':backslash,'+':plus,'-':minus,'=':equals, '<':lessthan, '>':greaterthan, ':':colon}
        

    def updateMode(self, mode):
        if(mode[0] == "textdisplay" and self.curMode[0] != "textdisplay"):
            self.lastMode = self.curMode
        self.curMode = mode
        self.newMode = True
        self.init = 0

    def updateLEDs(self, matrix):
        args = self.curMode[1]
        try:
            eval("self."+self.curMode[0]+"("+str(matrix)+","+args+")")
            #getattr(self, self.curMode[0])(matrix,*)
        except ValueError:
            print "ERROR, in function of: ",self.curMode
            print sys.exc_info()[0]
            if(self.curMode[0] in self.modes):
                self.updateMode((self.curMode[0],"default=True"))
            else:
                self.updateMode(("randsquares","default=True"))
                args = self.curMode[1].split(",")
                getattr(self, self.curMode[0])(matrix,*args)


    def randsquares(self,matrix,default=True,change=False,halfblack=False):
        if(change):
            if(self.updateSquares):
                self.updateSquares = False
                self.init = 0

        if(self.init == 0):
            self.init = 1
            for i in xrange(len(self.ledMatrix)):
                for j in xrange(len(self.ledMatrix)):
                    touchColors = []
                    availColors = []
                    if(halfblack):
                        if((i+j)%2 == 0):
                            self.w.itemconfigure(self.ledMatrix[i][j],fill=self.rgbToHex((1,1,1)))
                            continue
                    if(j > 0):
                        touchColors.append(self.w.itemcget(self.ledMatrix[i][j-1], "fill"))
                        if(i < len(self.ledMatrix)-1):
                            touchColors.append(self.w.itemcget(self.ledMatrix[i+1][j-1], "fill"))
                    if(i > 0):
                        if(j > 0):
                            touchColors.append(self.w.itemcget(self.ledMatrix[i-1][j-1], "fill"))
                        touchColors.append(self.w.itemcget(self.ledMatrix[i-1][j], "fill"))
                    for k in xrange(len(self.colors)):
                        if(self.colors[k] not in touchColors):
                            availColors.append(self.colors[k])
                    color = availColors[random.randrange(0,len(availColors))]
                    self.w.itemconfigure(self.ledMatrix[i][j],
                                                fill=color)
        self.master.update()
    

    def visualize1(self, matrix, default=True):
        if(self.visualizeWait < self.visualizeFreq):
            self.visualizeWait += 1
            return
        self.visualizeWait = 0
        if(self.visualizeWaves[0] == None):
            self.visualizeWaves[0] = self.colors[random.randrange(len(self.colors))]
        color = self.visualizeWaves[0]
        x = 3
        y = 5
        for i in xrange(len(self.visualizeWaves)):
            if(self.visualizeWaves[i] != None):
                for j in xrange(x,y):
                    self.w.itemconfigure(self.ledMatrix[x][j],fill=self.visualizeWaves[i])
                    self.w.itemconfigure(self.ledMatrix[y-1][j],fill=self.visualizeWaves[i])
                    self.w.itemconfigure(self.ledMatrix[j][x],fill=self.visualizeWaves[i])
                    self.w.itemconfigure(self.ledMatrix[j][y-1],fill=self.visualizeWaves[i])
                self.master.update()
            x-=1
            y+=1
        while color == self.visualizeWaves[0]:
            color = self.colors[random.randrange(len(self.colors))]
        for i in xrange(len(self.visualizeWaves)):
            if(i == 0):
                nextcolor = self.visualizeWaves[i]
                self.visualizeWaves[i] = color
                continue
            if(self.visualizeWaves[i] != None):
                curColor = self.visualizeWaves[i]
                self.visualizeWaves[i] = nextcolor
                nextcolor = curColor
            else:
                self.visualizeWaves[i] = nextcolor
                break

    def thetachi(self, matrix, default=True):
        bass = 0
        if(self.bass):
            self.bass = 0
      
            self.turnOffLEDs("all")
            getattr(self, self.thetaChiLetter.letter)(matrix)
            self.thetaChiLetter = self.thetaChiLetter.next

    def theta(self, matrix):
        self.w.itemconfigure(self.ledMatrix[1][1],fill="red")
        self.w.itemconfigure(self.ledMatrix[1][2],fill="red")
        self.w.itemconfigure(self.ledMatrix[1][3],fill="red")
        self.w.itemconfigure(self.ledMatrix[1][4],fill="red")
        self.w.itemconfigure(self.ledMatrix[1][5],fill="red")
        self.w.itemconfigure(self.ledMatrix[1][6],fill="red")
        self.w.itemconfigure(self.ledMatrix[6][1],fill="red")
        self.w.itemconfigure(self.ledMatrix[6][2],fill="red")
        self.w.itemconfigure(self.ledMatrix[6][3],fill="red")
        self.w.itemconfigure(self.ledMatrix[6][4],fill="red")
        self.w.itemconfigure(self.ledMatrix[6][5],fill="red")
        self.w.itemconfigure(self.ledMatrix[6][6],fill="red")
        self.w.itemconfigure(self.ledMatrix[2][1],fill="red")
        self.w.itemconfigure(self.ledMatrix[3][1],fill="red")
        self.w.itemconfigure(self.ledMatrix[4][1],fill="red")
        self.w.itemconfigure(self.ledMatrix[5][1],fill="red")
        self.w.itemconfigure(self.ledMatrix[2][6],fill="red")
        self.w.itemconfigure(self.ledMatrix[3][6],fill="red")
        self.w.itemconfigure(self.ledMatrix[4][6],fill="red")
        self.w.itemconfigure(self.ledMatrix[5][6],fill="red")

        self.w.itemconfigure(self.ledMatrix[2][4],fill="red")
        self.w.itemconfigure(self.ledMatrix[3][4],fill="red")
        self.w.itemconfigure(self.ledMatrix[4][4],fill="red")
        self.w.itemconfigure(self.ledMatrix[5][4],fill="red")
        self.master.update()

    def chi(self, matrix):
        self.w.itemconfigure(self.ledMatrix[1][1],fill="red")
        self.w.itemconfigure(self.ledMatrix[2][2],fill="red")
        self.w.itemconfigure(self.ledMatrix[3][3],fill="red")
        self.w.itemconfigure(self.ledMatrix[4][4],fill="red")
        self.w.itemconfigure(self.ledMatrix[5][5],fill="red")
        self.w.itemconfigure(self.ledMatrix[6][6],fill="red")
        self.w.itemconfigure(self.ledMatrix[6][1],fill="red")
        self.w.itemconfigure(self.ledMatrix[5][2],fill="red")
        self.w.itemconfigure(self.ledMatrix[4][3],fill="red")
        self.w.itemconfigure(self.ledMatrix[3][4],fill="red")
        self.w.itemconfigure(self.ledMatrix[2][5],fill="red")
        self.w.itemconfigure(self.ledMatrix[1][6],fill="red")
        self.master.update()


    def levels(self, matrix, default=True):
        self.turnOffLEDs("all")
        for i in xrange(len(matrix)):
            color = self.colors[i]
            for j in xrange(int(matrix[i])):
                
                self.w.itemconfigure(self.ledMatrix[i][j], fill=color)
        self.master.update()


    def bassring(self, matrix, default=True):
        if self.init == 0 or self.updateSquares:
            self.init = 1
            self.updateSquares = False
            for i in xrange(1,len(self.ledMatrix)-1):
                for j in xrange(1,len(self.ledMatrix)-1):
                    touchColors = []
                    availColors = []
                    if(j > 1):
                        touchColors.append(self.w.itemcget(self.ledMatrix[i][j-1], "fill"))
                        if(i < len(self.ledMatrix)-1):
                            touchColors.append(self.w.itemcget(self.ledMatrix[i+1][j-1], "fill"))
                    if(i > 1):
                        if(j > 1):
                            touchColors.append(self.w.itemcget(self.ledMatrix[i-1][j-1], "fill"))
                        touchColors.append(self.w.itemcget(self.ledMatrix[i-1][j], "fill"))
                    for k in xrange(len(self.colors)):
                        if(self.colors[k] not in touchColors):
                            availColors.append(self.colors[k])
                    color = availColors[random.randrange(0,len(availColors))]
                    self.w.itemconfigure(self.ledMatrix[i][j],
                                            fill=color)
            self.master.update()
                                   
        if(self.bass):
            self.bass = 0
            for i in xrange(len(self.ledMatrix)):
                
                self.w.itemconfigure(self.ledMatrix[i][0],
                                    fill=self.bassBooster.color)
                self.w.itemconfigure(self.ledMatrix[i][len          (matrix)-1],fill=self.bassBooster.color)
                self.w.itemconfigure(self.ledMatrix[0][i],
                                    fill=self.bassBooster.color)
                self.w.itemconfigure(self.ledMatrix[len          (matrix)-1][i],fill=self.bassBooster.color)
            self.bassBooster = self.bassBooster.next
        self.master.update()


    def textdisplay(self,matrix,default=True,text=False):
        if(len(self.letterMatrix) > 0):
            if(self.letterWait < 1):
                self.letterWait += 1
                return
            else:
                self.letterWait = 0

            for i in xrange(len(self.ledMatrix)-1,0,-1):
                for j in xrange(len(self.ledMatrix)):
                    self.w.itemconfigure(self.ledMatrix[i][j],fill=self.w.itemcget(self.ledMatrix[i-1][j],"fill"))
            self.turnOffLEDs("letters")

            for i in self.letterMatrix[0]:
                self.w.itemconfigure(self.ledMatrix[0][i],fill="red")
            self.letterMatrix = self.letterMatrix[1:]
            self.master.update()

        elif(text):
            #self.textDisplayTimer = 0.0
            symbol = text[0]
            if(symbol.isalpha() == False and symbol.isdigit()==False and symbol.isspace()==False):
                if(symbol not in self.symbolDict):
                    self.updateMode(("textdisplay","text="+"'"+text[1:]+"'"))
                    return
            if(symbol.isdigit()):
                self.letterMatrix = [[]]+eval("num"+symbol+"()")
            elif(symbol.isspace()):
                self.letterMatrix = [[],[],[],[]]
            elif(symbol in self.symbolDict):
                self.letterMatrix = [[]]+self.symbolDict[symbol]()               
            else:
                symbol = symbol.lower()
                self.letterMatrix = [[]]+eval(symbol+"()")
            if(len(text) == 1):
                self.letterMatrix += [[],[],[],[],[],[],[],[]]
            self.updateMode(("textdisplay","text="+"'"+text[1:]+"'"))

        else:
            if(self.lastMode != None):
                self.updateMode(self.lastMode)
            else:
                self.updateMode(("randsquares","default=True"))                
       

    def solidcolor(self,matrix,default=True,colorrgb=False):
        if(self.newMode):
            self.newMode = False
            if(colorrgb):
                colorrgb = eval(colorrgb)
                for i in colorrgb:
                    if i < 0 or i > 255:
                        self.updateMode(("randsquares","default=True"))
                        return
                for i in xrange(len(self.ledMatrix)):
                    for j in xrange(len(self.ledMatrix)):
                        self.w.itemconfigure(self.ledMatrix[i][j],
                                            fill=self.rgbToHex(colorrgb))
                self.master.update()

    def turnOffLEDs(self, Leds):
        if Leds == "bassring":
            for i in xrange(len(self.ledMatrix)):
                
                self.w.itemconfigure(self.ledMatrix[i][0],
                                    fill="white")
                self.w.itemconfigure(self.ledMatrix[i][len          (self.ledMatrix)-1],fill="white")
                self.w.itemconfigure(self.ledMatrix[0][i],
                                    fill="white")
                self.w.itemconfigure(self.ledMatrix[len          (self.ledMatrix)-1][i],fill="white")
        elif Leds == "letters":
            for i in xrange(len(self.ledMatrix)):
                self.w.itemconfigure(self.ledMatrix[0][i],fill="white")
        else:
            
            for i in range(len(self.ledMatrix)):
                for j in range(len(self.ledMatrix)):
                    self.w.itemconfigure(self.ledMatrix[i][j],
                                    fill="white")
        self.master.update()


    def callback(self):
        self.killed = True
        self.master.destroy()
        sys.exit("Killing Program")

    def hexToRGB(self,hex):
        hex = hex.lstrip('#')
        lv = len(hex)
        return tuple(int(hex[i:i+lv/3],16)for i in range(0,lv,lv/3))

    def rgbToHex(self,rgb):
        return "#%02x%02x%02x" % rgb
    
   

if __name__ == "__main__":
    main()     

        
