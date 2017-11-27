from PIL import Image
import math

ALPHA_THRESHOLD=50
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
def vectorMakeLength1(v):
    return [v[0]/vectorMagnitude(v),v[1]/vectorMagnitude(v)]
def vectorOpposite(v):
    return [-v[0],-v[1]]
def angleBetweenVectors(v1,v2):
    v1,v2=vectorMakeLength1(v1),vectorMakeLength1(v2)
    a=math.degrees(math.atan2(v2[1],v2[0]) - math.atan2(v1[1],v1[0]))
    if a>180:
        a-=360
    if a<-180:
        a+=360
    return a
def makeMovingAverage(graph, period):
    movingAverage=[]
    for i in range(len(graph)):
        movingAverage.append(0)
        for di in range(-math.floor(period/2),math.floor(period/2)+1):
            movingAverage[-1]+=graph[(i+di)%len(graph)]
        movingAverage[-1]/=period
    return movingAverage

class Piece:
    def __init__(self, imageName):
        self.image=Image.open(imageName)
        self.imagePixels=self.image.convert('RGBA').load()
        self.size=self.image.size

        self.borderPixels=[]
        self.borderPixelsOpposite=[]
        self.borderLength=0
        self.getBorderPixels()

        self.borderAngles=[]
        self.borderAnglesOpposite=[]

        self.borderAngleChunks=[]
        self.borderAngleChunksOpposite=[]
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
        self.borderLength=len(self.borderPixels)
        print("Border Length:",self.borderLength)
    def getBorderAngles(self, offset, dx):
        self.borderAngles=[]
        self.borderAnglesOpposite=[]
        for i in range(len(self.borderPixels)):
            v=subtractVectors(self.borderPixels[i],self.borderPixels[(i+dx)%len(self.borderPixels)])
            v2=subtractVectors(self.borderPixels[(i+offset)%len(self.borderPixels)],self.borderPixels[(i+offset+dx)%len(self.borderPixels)])
            self.borderAngles.append(angleBetweenVectors(v,v2))
        for i in range(len(self.borderPixels)-1,-1,-1):
            v=subtractVectors(self.borderPixels[i],self.borderPixels[(i-dx)%len(self.borderPixels)])
            v2=subtractVectors(self.borderPixels[(i-offset)%len(self.borderPixels)],self.borderPixels[(i-offset-dx)%len(self.borderPixels)])
            self.borderAnglesOpposite.append(angleBetweenVectors(v,v2))
    #def getBorderAngleChunks(self, smooth):


p1 = Piece('Pieces Resized/Piece 5.png')
p1.getBorderAngles(2,5)
# p1.getBorderAngleChunks(9)

borderAngles=p1.borderAngles#makeMovingAverage(p1.borderAngles,9) #smooth?
print('\t'.join([str(a) for a in borderAngles]))

firstDerivative=[]
for i in range(len(borderAngles)):
    d=borderAngles[(i+1)%len(borderAngles)]-borderAngles[i]
    firstDerivative.append(d)
# firstDerivative=makeMovingAverage(firstDerivative,9) #smooth?
print('\t'.join([str(a) for a in firstDerivative]))

secondDerivative=[]
for i in range(len(firstDerivative)):
    d=firstDerivative[(i+1)%len(firstDerivative)]-firstDerivative[i]
    secondDerivative.append(d)
secondDerivative=makeMovingAverage(secondDerivative,9) #smooth?
print('\t'.join([str(a) for a in secondDerivative]))




# borderAngleChunks=[[]]
# for i in range(len(borderAngles)):
#     if (borderAnglesSmooth[(i-1)%len(borderAnglesSmooth)]>0) != (borderAnglesSmooth[i]>0):
#         borderAngleChunks.append([])
#     elif (dsSmooth[(i-1)%len(dsSmooth)]>0) != (dsSmooth[i]>0):
#         borderAngleChunks.append([])
#     borderAngleChunks[-1].append(borderAngles[i])