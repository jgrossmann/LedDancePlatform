from Tkinter import *
import alsaaudio
import audioop
import random

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
        self.ledMatrix = [[None for x in xrange(12)]for x in xrange (12)]
        red = Colors("red",None)
        green = Colors("green", red)
        orange = Colors("orange",green)
        blue = Colors("blue",orange)
        yellow = Colors("yellow",blue)
        purple = Colors("purple", yellow)
        white = Colors("white",purple)
        red.next = white
        
        theta = ThetaChiLetter("theta", None)
        chi = ThetaChiLetter("chi", theta)
        theta.next = chi

        self.bassBooster = white
        self.thetaChiLetter = theta
        self.thetaChiLetterFreq = 1
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

    def updateLEDs(self, matrix, mode):
        getattr(self, mode)(matrix)

    
    def columns(self, matrix):
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                self.w.itemconfigure(self.ledMatrix[i][j],
                                fill="red")
        self.master.update()

    def thetachi(self, matrix):
        bass = 0
        for i in range(len(matrix)):
            if(matrix[i][1]):
                if(i == 0):
                    bass = 1
                    continue
        if(bass):
            if(self.thetaChiLetterFreq ==1):
                self.thetaChiLetterFreq += 1
            else:
                self.turnOffLEDs()
                getattr(self, self.thetaChiLetter.letter)(matrix)
                self.thetaChiLetter = self.thetaChiLetter.next
                self.thetaChiLetterFreq = 1
                self.master.update()

    def theta(self, matrix):
        for i in xrange(1,len(matrix)-1):
            self.w.itemconfigure(self.ledMatrix[1][i],fill="red")
            self.w.itemconfigure(self.ledMatrix[6][i],fill="red")
            self.w.itemconfigure(self.ledMatrix[i][1],fill="red")
            self.w.itemconfigure(self.ledMatrix[i][6],fill="red")
        self.w.itemconfigure(self.ledMatrix[3][4],fill="red")
        self.w.itemconfigure(self.ledMatrix[4][4],fill="red")

    def chi(self, matrix):
        for i in xrange(1,len(matrix)-1):
            self.w.itemconfigure(self.ledMatrix[i][i],fill="red")
            self.w.itemconfigure(self.ledMatrix[i][len(matrix)-i-1],fill="red")




    def bassring(self, matrix):
        bass = 0
        for i in range(len(matrix)):
            if(matrix[i][1]):
                if(i == 0):
                    bass = 1
                    continue
                if(i == len(matrix)-1):
                    continue
                color = (random.randrange(0,256), 
                        random.randrange(0,256),
                        random.randrange(0,256))
                for j in range(1,len(matrix)-1):
                    self.w.itemconfigure(self.ledMatrix[i][j],
                                    fill=self.rgbToHex(color))
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

    def turnOffLEDs(self):
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

        
