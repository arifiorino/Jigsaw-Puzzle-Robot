from PIL import Image
import math

vectors1=[[0,-1],[1,0],[0,1],[-1,0]]
vectors2=[[0,-1],[1,-1],[1,0],[1,1],[0,1],[-1,1],[-1,0],[-1,-1]]
def dist(a,b):
    return math.sqrt((b[0]-a[0])**2+(b[1]-a[1])**2)
def addVectors(a,b):
    return [a[0]+b[0],a[1]+b[1]]
def subtractVectors(a,b):
    return [a[0]-b[0],a[1]-b[1]]
def vectorMagnitude(v):
    return math.sqrt(v[0]**2+v[1]**2)

ALPHA_THRESHOLD=50


class Piece:
    def __init__(self, imageName):
        self.image=Image.open(imageName)
        self.imagePixels=self.image.convert('RGBA').load()
        self.size=self.image.size
        self.firstPixel=[0,0]

        self.borderPixels=[]
        self.getBorderPixels()

        self.borderVectors=[]
        self.getBorderVectors(20)

    def getBorderPixels(self):
        borderPixels1=[] #Unorganized border pixels
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                if self.imagePixels[x,y][-1]>=ALPHA_THRESHOLD:
                    if x==0 or x==self.size[0]-1 or y==0 or y==self.size[1]-1:
                        borderPixels1.append([x,y])
                    else:
                        for vector in vectors1:
                            if self.imagePixels[x+vector[0],y+vector[1]][-1]<ALPHA_THRESHOLD:
                                borderPixels1.append([x,y])
                                break

        done1=False
        pixel=borderPixels1[0]
        while not done1:
            done2=False
            for vector in vectors2:
                if addVectors(pixel,vector) not in self.borderPixels: #not going backwards
                    for nextPixel in borderPixels1:
                        if addVectors(pixel,vector)==nextPixel:
                            pixel=nextPixel
                            self.borderPixels.append(pixel)
                            done2=True
                            break
                if done2:
                    break
            if pixel==borderPixels1[0]:
                done1=True
        print('borderLength=',len(self.borderPixels))

    def getBorderVectors(self, n):
        for delta in range(1,n+1):
            self.borderVectors.append([])
            for i in range(len(self.borderPixels)):
                self.borderVectors[-1].append(subtractVectors(self.borderPixels[(i+delta)%len(self.borderPixels)],self.borderPixels[i]))

    def compareBorderVectors(self, piece):
        e=''
        smallestLength=min(len(self.borderPixels),len(piece.borderPixels))
        largestLength=max(len(self.borderPixels),len(piece.borderPixels))

        differences=[]
        for borderOffset in range(largestLength):
            differences.append([])
            for borderI in range(smallestLength):
                totalDifference=0
                for borderDelta in range(len(self.borderVectors)):
                    totalDifference+=vectorMagnitude(subtractVectors(self.borderVectors[borderDelta][borderI],piece.borderVectors[borderDelta][(borderI+borderOffset)%smallestLength]))
                differences[-1].append(totalDifference)
                e+=str(totalDifference)+','
            e+='\n'

        f=open('export.csv','w')
        f.write(e)
        f.close()

piece1 = Piece('piece 1 fifth.png')
piece2 = Piece('piece 2 fifth.png')

piece1.compareBorderVectors(piece2)

