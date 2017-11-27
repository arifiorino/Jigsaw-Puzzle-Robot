from PIL import Image
import math

ALPHA_THRESHOLD=50
OFFSET_CONSTANT=5
FORWARD_CONSTANT=15
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

class Piece:
    def __init__(self, imageName):
        self.image=Image.open(imageName)
        self.imagePixels=self.image.convert('RGBA').load()
        self.size=self.image.size

        self.borderPixels=[]
        self.getBorderPixels()

        self.borderAngles=[]
        self.borderAnglesOpposite=[]
        self.getBorderAngles()

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

    def getBorderAngles(self):
        for i in range(len(self.borderPixels)):
            v=subtractVectors(self.borderPixels[i],self.borderPixels[(i+FORWARD_CONSTANT)%len(self.borderPixels)])
            v2=subtractVectors(self.borderPixels[(i+OFFSET_CONSTANT)%len(self.borderPixels)],self.borderPixels[(i+OFFSET_CONSTANT+FORWARD_CONSTANT)%len(self.borderPixels)])
            self.borderAngles.append(angleBetweenVectors(v,v2))
        self.borderAnglesOpposite=[-self.borderAngles[i] for i in range(len(self.borderAngles)-1,-1,-1)]

piece1 = Piece('Pieces Resized/Piece 1.png')
piece2 = Piece('Pieces Resized/Piece 3.png')



import matplotlib.pyplot as plt
import matplotlib.animation as animation

borderI=0
fig, ax = plt.subplots()


fig.add_subplot(221)
plt.title('Piece 1')
plt.imshow(piece1.image)
image1PointLine = plt.plot([piece1.borderPixels[0][0]], [piece1.borderPixels[0][1]], marker='o', markersize=5, color="blue")[0]
image1PointLine2 = plt.plot([piece1.borderPixels[FORWARD_CONSTANT][0]], [piece1.borderPixels[FORWARD_CONSTANT][1]], marker='o', markersize=5, color="red")[0]

fig.add_subplot(222)
plt.title('Piece 1 Angles')
line=piece1.borderAngles
rects=plt.bar(range(len(line)),line)
graphPointLine = plt.plot([0], [line[0]], marker='o', markersize=5, color="blue")[0]

fig.add_subplot(223)
plt.title('Piece 2')
plt.imshow(piece2.image)

fig.add_subplot(224)
plt.title('Piece 2 Angles')
plt.bar(range(len(piece2.borderAnglesOpposite)),piece2.borderAnglesOpposite)

def animateImage1Point(frameno):
    global piece1,image1PointLine,borderI
    image1PointLine.set_xdata(piece1.borderPixels[borderI][0])
    image1PointLine.set_ydata(piece1.borderPixels[borderI][1])
    # print(piece1.borderAngles[borderI%len(piece1.borderPixels)])

    borderI+=1
    borderI%=len(piece1.borderPixels)
    return image1PointLine
a1 = animation.FuncAnimation(fig, animateImage1Point, blit=False, interval=5,frames=len(piece1.borderPixels),repeat=True)

def animateImage1Point2(frameno):
    global piece1,image1PointLine2,borderI
    image1PointLine2.set_xdata(piece1.borderPixels[(borderI+FORWARD_CONSTANT)%len(piece1.borderPixels)][0])
    image1PointLine2.set_ydata(piece1.borderPixels[(borderI+FORWARD_CONSTANT)%len(piece1.borderPixels)][1])
    return image1PointLine2
a2 = animation.FuncAnimation(fig, animateImage1Point2, blit=False, interval=5,frames=len(piece1.borderPixels),repeat=True)

def animateGraphPoint(frameno):
    global piece1,line,graphPointLine,borderI
    graphPointLine.set_xdata(borderI)
    graphPointLine.set_ydata(line[borderI])
    return graphPointLine
a3 = animation.FuncAnimation(fig, animateGraphPoint, blit=False, interval=5,frames=len(piece1.borderPixels),repeat=True)

plt.show()