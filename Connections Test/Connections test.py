from PIL import Image
import math

#Border Vector:
#  0
#3   1
#  2

vectorConversion=[[0,-1],[1,0],[0,1],[-1,0]]
def oppositeVector(v):
    return {0:2,1:3,2:0,3:1,-1:-1}[v]
def dist(a,b):
    return math.sqrt((b[0]-a[0])**2+(b[1]-a[1])**2)
def magnitude(v):
    return dist([0,0],v)
def addVectors(vs):
    return [sum(v[0] for v in vs),sum(v[1] for v in vs)]
def dotProduct(v1,v2):
    return v1[0]*v2[0]+v1[1]*v2[1]
def angleBetween(v1,v2):
    return math.acos(dotProduct(v1,v2)/magnitude(v1)/magnitude(v2))

ALPHA_THRESHOLD=125


class Piece:
    def __init__(self, imageName):
        self.image=Image.open(imageName)
        self.imagePixels=self.image.convert('RGBA').load()
        self.size=self.image.size
        self.firstPixel=[0,0]

        self.borderImage=Image.new("RGB", self.size, "white")
        self.borderImagePixels=self.borderImage.load()

        self.borderVectors=[]
        self.getBorderVectors()
        print(self.borderVectors)

    def getBorderVectors(self):
        done=False
        while not done:
            done=self.imagePixels[self.firstPixel[0],1][-1]>ALPHA_THRESHOLD
            self.firstPixel[0]+=1


        borderPixels=[]
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                if self.imagePixels[x,y][-1]>ALPHA_THRESHOLD:
                    if x==0 or x==self.size[0]-1 or y==0 or y==self.size[1]-1:
                        borderPixels.append([x,y])
                    else:
                        for vector in range(4):
                            if self.imagePixels[x+vectorConversion[vector][0],y+vectorConversion[vector][1]][-1]<ALPHA_THRESHOLD:
                                borderPixels.append([x,y])
                                break
        print(len(borderPixels))

        done,x,y,lastVector=False,self.firstPixel[0],self.firstPixel[1],-1
        while not done:
            self.borderImagePixels[x,y]=(0,0,0)

            pVectors=[]
            for pVector in range(4):
                newX,newY=x+vectorConversion[pVector][0],y+vectorConversion[pVector][1]
                if newX in range(self.size[0]) and newY in range(self.size[1]):
                    if self.imagePixels[newX, newY][-1]>ALPHA_THRESHOLD:
                        pVectors.append(pVector)
            if oppositeVector(lastVector) in pVectors:
                pVectors.remove(oppositeVector(lastVector))

            vector=None

            if len(pVectors)==1:
                vector=pVectors[0]
            else:
                for pVector in pVectors: #if next one part of border, continue
                    newX=x+vectorConversion[pVector][0]
                    newY=y+vectorConversion[pVector][1]
                    if [newX,newY] in borderPixels:
                        vector=pVector
                        break

            if vector is None: #if not part of border, follow previous vector
                generalDirection=addVectors([vectorConversion[v] for v in self.borderVectors[-5:]])
                angles=[]
                for pVector in pVectors:
                    angles.append(angleBetween(vectorConversion[pVector],generalDirection))
                print(angles,pVectors)
                vector=pVectors[angles.index(min(angles))]


            lastVector=vector
            self.borderVectors.append(vector)
            x,y=x+vectorConversion[vector][0],y+vectorConversion[vector][1]

            if dist([x,y],self.firstPixel)==1 and len(self.borderVectors)>1:
                done=True
            if len(self.borderVectors)%20==5:
                self.borderImage.save('border.png')
                print(len(self.borderVectors))
        self.borderImage.save('border.png')

piece1 = Piece('piece 2 fifth.png')
# piece2 = Piece('piece 2 fifth.png')



