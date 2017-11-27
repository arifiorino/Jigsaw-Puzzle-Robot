from PIL import Image
import math

import matplotlib.pyplot as plt
import matplotlib.animation as animation

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
def vectorOpposite(v):
    return [-v[0],-v[1]]

ALPHA_THRESHOLD=50

class Piece:
    def __init__(self, imageName):
        self.image=Image.open(imageName)
        self.imagePixels=self.image.convert('RGBA').load()
        self.size=self.image.size

        self.borderPixels=[]
        self.borderPixelsOpposite=[]
        self.getBorderPixels()

        self.borderVectors=[]
        self.borderVectorsOpposite=[]
        self.getBorderVectors(20)

        self.compareDifferences=[]

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

        self.borderPixelsOpposite=self.borderPixels[::-1]

        print('borderLength=',len(self.borderPixels))

    def getBorderVectors(self, n):
        for delta in range(1,n+1):
            self.borderVectors.append([])
            for i in range(len(self.borderPixels)):
                self.borderVectors[-1].append(subtractVectors(self.borderPixels[(i+delta)%len(self.borderPixels)],self.borderPixels[i]))

        for i1 in range(len(self.borderVectors)):
            self.borderVectorsOpposite.append([])
            for i2 in range(len(self.borderVectors[i1])-1,0,-1): #traverse p1Old backwards
                self.borderVectorsOpposite[-1].append(vectorOpposite(self.borderVectors[i1][i2]))

    def compareBorders(self, piece):
        smallestLength=min(len(self.borderPixels),len(piece.borderPixels))
        largestLength=max(len(self.borderPixels),len(piece.borderPixels))

        p1=self.borderVectorsOpposite
        p2=piece.borderVectors

        deltaWeights=[50,70,100,25,10,6,3,2,2,1,1,.8,.7,.6,.5,.4,.3,.3,.3,.3]


        for borderOffset in range(largestLength):
            self.compareDifferences.append([])
            for borderI in range(smallestLength):
                totalDifference=0
                for borderDelta in range(len(p1)):
                    totalDifference+=vectorMagnitude(subtractVectors(p1[borderDelta][(borderI+borderOffset)%len(p1[0])],p2[borderDelta][borderI%len(p2[0])]))*deltaWeights[borderDelta]
                self.compareDifferences[-1].append(totalDifference)
            if borderOffset%100==0:
                print(round(borderOffset/largestLength*100,2),'%')



piece1 = Piece('piece 1 fifth rotated.png')
piece2 = Piece('piece 2 fifth rotated.png')
piece1.compareBorders(piece2)

#Animation

fig, ax = plt.subplots()

HARDCODED_OFFSET=205


fig.add_subplot(221)
plt.title('Piece 1')
plt.imshow(piece1.image)
offsetPoint=piece1.borderPixels[HARDCODED_OFFSET]
offsetPointLine = plt.plot([offsetPoint[0]], [offsetPoint[1]], marker='o', markersize=5, color="red")[0]
image1Point=piece1.borderPixels[HARDCODED_OFFSET]
image1PointLine = plt.plot([image1Point[0]], [image1Point[1]], marker='o', markersize=5, color="blue")[0]

fig.add_subplot(222)
plt.title('Piece 2')
plt.imshow(piece2.image)
image2Point=piece2.borderPixels[0]
image2PointLine = plt.plot([image2Point[0]], [image2Point[1]], marker='o', markersize=5, color="blue")[0]

fig.add_subplot(223)
plt.title('Similarities')
line=piece1.compareDifferences[len(piece1.borderPixels)-HARDCODED_OFFSET]
rects=plt.bar(range(len(line)),line)
graphX=0
graphPointLine = plt.plot([graphX], [line[graphX]], marker='o', markersize=5, color="blue")[0]

def animateSimilarities(frameno):
    global line,piece1,rects
    line=piece1.compareDifferences[frameno]
    for rect, h in zip(rects, line):
        rect.set_height(h)
    return rects
# a1 = animation.FuncAnimation(fig, animateSimilarities, blit=False, interval=5,frames=len(piece1.compareDifferences),repeat=False)


def animateOffsetPoint(frameno):
    global offsetPoint,piece1,offsetPointLine
    offsetPoint=addVectors(offsetPoint,piece1.borderVectorsOpposite[0][frameno])
    offsetPointLine.set_xdata(offsetPoint[0])
    offsetPointLine.set_ydata(offsetPoint[1])
    return offsetPointLine
# a2 = animation.FuncAnimation(fig, animateOffsetPoint, blit=False, interval=5,frames=len(piece1.borderPixels),repeat=False)

smallestLength=min(len(piece1.borderPixels),len(piece2.borderPixels))
largestLength=max(len(piece1.borderPixels),len(piece2.borderPixels))

def animateImage1Point(frameno):
    global image1Point,image1PointLine
    image1Point=piece1.borderPixelsOpposite[(graphX+(len(piece1.borderPixels)-HARDCODED_OFFSET))%len(piece1.borderPixels)]
    image1PointLine.set_xdata(image1Point[0])
    image1PointLine.set_ydata(image1Point[1])
    return image1PointLine
a3 = animation.FuncAnimation(fig, animateImage1Point, blit=False, interval=5,frames=len(piece1.borderPixels),repeat=True)

def animateImage2Point(frameno):
    global image2Point,image2PointLine
    image2Point=piece2.borderPixels[graphX]
    image2PointLine.set_xdata(image2Point[0])
    image2PointLine.set_ydata(image2Point[1])
    return image2PointLine
a4 = animation.FuncAnimation(fig, animateImage2Point, blit=False, interval=5,frames=len(piece2.borderPixels),repeat=True)

def animateGraphPoint(frameno):
    global graphX,graphPointLine
    graphX=graphX+1
    graphPointLine.set_xdata(graphX)
    graphPointLine.set_ydata(line[graphX])
    return image2PointLine
a5 = animation.FuncAnimation(fig, animateGraphPoint, blit=False, interval=5,frames=smallestLength,repeat=True)

plt.show()