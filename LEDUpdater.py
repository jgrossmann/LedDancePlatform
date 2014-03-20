from Tkinter import *
import alsaaudio
import audioop
import random
import time

def main():
    window = LEDWindow()
    rgb = 1
    while(True):
        if(rgb > 255):
            #rgb = 1
            True
        for i in range(12):
            for j in range(12):
                True
                #color = (1,1,rgb)
                #window.w.itemconfigure(window.ledMatrix[i][j],fill=window.rgbToHex(color))
                #window.master.update()
        #rgb += 1
        
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
        self.ledMatrix = [[None for x in xrange(9)]for x in xrange (9)]
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

        self.bassBooster = white
        self.init = 0
        self.updateSquares = False
        self.thetaChiLetter = theta
        self.master = Tk()
        self.master.protocol("WM_DELETE_WINDOW", self.callback)
        self.w = Canvas(self.master, height=320, width=320)
        x = 0
        for i in range(320,-1,-40):
            y = 0
            for j in range(320,-1,-40):
                self.ledMatrix[x][y]=self.w.create_rectangle(i,j,i-40,j-40,outline="black",fill=self.rgbToHex((255,255,255)),width=2)
                y += 1
            x += 1
        self.w.pack()
        self.master.update()
        
##---------IMPORTANT, MUST UPDATE SELF.MODES WITH ADDITIONAL FUNCTIONS IF YOU WANT THE MODES TO BE USABLE!!!!!!-------#####
        self.modes = ["thetachi","bassring","levels","randsquares"]
        self.curMode = ("randsquares","default=True")
        

    def updateMode(self, mode):
        self.curMode = mode

    def updateLEDs(self, matrix):
        args = self.curMode[1]
        try:
            print self.curMode
            print args
            print("self."+self.curMode[0]+"("+str(matrix)+","+args+")")
            print "why didnt it print"
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

    def randsquares(self,matrix,default=True,change=False):
        print "in function"
        print change
        if(change):
            if(self.updateSquares):
                self.updateSquares = False
                self.init = 0

        if(self.init == 0):
            self.init = 1
            for i in xrange(len(matrix)):
                for j in xrange(len(matrix)):
                    touchColors = []
                    availColors = []
                    if(j > 0):
                        touchColors.append(self.w.itemcget(self.ledMatrix[i][j-1], "fill"))
                        if(i < len(matrix)):
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
    
    def columns(self, matrix):
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                self.w.itemconfigure(self.ledMatrix[i][j],
                                fill="red")
        self.master.update()

    def thetachi(self, matrix, default=True):
        bass = 0
        for i in range(len(matrix)):
            if(matrix[i]):
                if(i == 0):
                    bass = 1
                    continue
        if(bass):
            self.turnOffLEDs("all")
            getattr(self, self.thetaChiLetter.letter)(matrix)
            self.thetaChiLetter = self.thetaChiLetter.next
            self.master.update()

    def theta(self, matrix):
        for i in xrange(1,len(matrix)-1):
            self.w.itemconfigure(self.ledMatrix[1][i],fill="red")
            self.w.itemconfigure(self.ledMatrix[6][i],fill="red")
            self.w.itemconfigure(self.ledMatrix[i][1],fill="red")
            self.w.itemconfigure(self.ledMatrix[i][6],fill="red")
        self.w.itemconfigure(self.ledMatrix[2][4],fill="red")
        self.w.itemconfigure(self.ledMatrix[3][4],fill="red")
        self.w.itemconfigure(self.ledMatrix[4][4],fill="red")
        self.w.itemconfigure(self.ledMatrix[5][4],fill="red")

    def chi(self, matrix):
        for i in xrange(1,len(matrix)-1):
            self.w.itemconfigure(self.ledMatrix[i][i],fill="red")
            self.w.itemconfigure(self.ledMatrix[i][len(matrix)-i-1],fill="red")

    def levels(self, matrix, default=True):
        self.turnOffLEDs("all")
        for i in xrange(len(matrix)):
            color = self.colors[i]
            print color
            for j in xrange(int(matrix[i])):
                
                self.w.itemconfigure(self.ledMatrix[i][j], fill=color)
        self.master.update()


    def bassring(self, matrix, default=True):
        if self.init == 0 or self.updateSquares:
            self.init = 1
            self.updateSquares = False
            for i in xrange(1,len(matrix)-1):
                for j in xrange(1,len(matrix)-1):
                    touchColors = []
                    availColors = []
                    if(j > 1):
                        touchColors.append(self.w.itemcget(self.ledMatrix[i][j-1], "fill"))
                        if(i < len(matrix)-1):
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
            
        bass = 0
        for i in range(len(matrix)):
            if(i == 0):
                if(matrix[i]):
                    bass = 1
                    #self.turnOffLEDs("bassring")
                continue
            if(i == len(matrix)-1):
                continue
            
            
        if(bass):
            for i in xrange(len(matrix)):
                
                self.w.itemconfigure(self.ledMatrix[i][0],
                                    fill=self.bassBooster.color)
                self.w.itemconfigure(self.ledMatrix[i][len          (matrix)-1],fill=self.bassBooster.color)
                self.w.itemconfigure(self.ledMatrix[0][i],
                                    fill=self.bassBooster.color)
                self.w.itemconfigure(self.ledMatrix[len          (matrix)-1][i],fill=self.bassBooster.color)
            self.bassBooster = self.bassBooster.next
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
        else:
            
            for i in range(len(self.ledMatrix)):
                for j in range(len(self.ledMatrix)):
                    self.w.itemconfigure(self.ledMatrix[i][j],
                                    fill="white")
        self.master.update()

    def callback(self):
        self.master.destroy()

    def hexToRGB(self,hex):
        hex = hex.lstrip('#')
        lv = len(hex)
        return tuple(int(hex[i:i+lv/3],16)for i in range(0,lv,lv/3))

    def rgbToHex(self,rgb):
        return "#%02x%02x%02x" % rgb
    
   

if __name__ == "__main__":
    main()     

        
