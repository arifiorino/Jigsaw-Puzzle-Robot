from PIL import Image
import math

ALPHA_THRESHOLD=50
OFFSET_CONSTANT=1
FORWARD_CONSTANT=5
vectors1=[[0,-1],[1,0],[0,1],[-1,0]]
vectors2=[[0,-1],[1,-1],[1,0],[1,1],[0,1],[-1,1],[-1,0],[-1,-1]]

#BOTH COLOR AND SHAPE AT THE SAME TIME DOESN'T WORK

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
        self.borderPixelsOpposite=[]
        self.borderLength=0
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
        self.borderPixelsOpposite=self.borderPixels[::-1]
        self.borderLength=len(self.borderPixels)
        print("Border Length:",self.borderLength)
    def getBorderAngles(self):
        for i in range(len(self.borderPixels)):
            v=subtractVectors(self.borderPixels[i],self.borderPixels[(i+FORWARD_CONSTANT)%len(self.borderPixels)])
            v2=subtractVectors(self.borderPixels[(i+OFFSET_CONSTANT)%len(self.borderPixels)],self.borderPixels[(i+OFFSET_CONSTANT+FORWARD_CONSTANT)%len(self.borderPixels)])
            self.borderAngles.append(angleBetweenVectors(v,v2))
        for i in range(len(self.borderPixels)-1,-1,-1):
            v=subtractVectors(self.borderPixels[i],self.borderPixels[(i-FORWARD_CONSTANT)%len(self.borderPixels)])
            v2=subtractVectors(self.borderPixels[(i-OFFSET_CONSTANT)%len(self.borderPixels)],self.borderPixels[(i-OFFSET_CONSTANT-FORWARD_CONSTANT)%len(self.borderPixels)])
            self.borderAnglesOpposite.append(angleBetweenVectors(v,v2))

class PieceConnection:
    def __init__(self, biggerPiece, smallerPiece,connectionValues,shapeDifference,colorDifference):
        self.biggerPiece=biggerPiece
        self.smallerPiece=smallerPiece
        self.connectionValues=connectionValues
        self.offset, self.start, self.end = connectionValues
        self.shapeDifference=shapeDifference
        self.colorDifference=colorDifference
    def saveImages(self):
        biggerImage=self.biggerPiece.image.copy()
        biggerImagePixels=biggerImage.load()
        for borderI in range(self.offset+self.start,self.offset+self.end):
            pixel=self.biggerPiece.borderPixels[borderI%self.biggerPiece.borderLength]
            biggerImagePixels[pixel[0],pixel[1]]=(255,0,0,255)
        biggerImage.save("Export/Bigger.png")

        smallerImage=self.smallerPiece.image.copy()
        smallerImagePixels=smallerImage.load()
        for borderI in range(self.start,self.end):
            pixel=self.smallerPiece.borderPixelsOpposite[borderI%self.smallerPiece.borderLength]
            smallerImagePixels[pixel[0],pixel[1]]=(255,0,0,255)
        smallerImage.save("Export/Smaller.png")

def getPieceShapeConnections(p1,p2):
    biggerPiece=[p1,p2][int(p1.borderLength<p2.borderLength)]
    smallerPiece=[p1,p2][int(p1.borderLength>p2.borderLength)]
    biggerLength=biggerPiece.borderLength
    smallerLength=smallerPiece.borderLength

    print('\nFinding similarities...')

    differences=[]
    for offset in range(0,biggerLength-1,1):
        for start in range(0,smallerLength-1,1):
            for end in range(start+50,start+51,1):
                shapeDifference=0
                colorDifference=0
                for borderI in range(start,end): #SMALLER PIECE OPPOSITE!!!!
                    biggerPieceAngle=biggerPiece.borderAngles[(borderI+offset)%biggerLength]
                    smallerPieceAngle=smallerPiece.borderAnglesOpposite[borderI%smallerLength]

                    pixel1=biggerPiece.borderPixels[(offset+borderI)%biggerPiece.borderLength]
                    color1=biggerPiece.imagePixels[pixel1[0],pixel1[1]]
                    pixel2=smallerPiece.borderPixelsOpposite[borderI%smallerPiece.borderLength]
                    color2=smallerPiece.imagePixels[pixel2[0],pixel2[1]]

                    shapeDifference+=(biggerPieceAngle-smallerPieceAngle)**2
                    for i in range(3):
                        colorDifference+=(color1[i]-color2[i])**2 / 100.0
                differences.append([[offset,start,end],shapeDifference+colorDifference,[shapeDifference,colorDifference]])
        if offset%10==0:
            print(str(round(offset/biggerLength*100))+'%')

    print('\nFinding connections...')

    minimums=[differences[0]] #minimums includes first minimum
    for value in differences:
        if value[1]<minimums[0][1]:
            minimums[0]=value

    alreadyChecked=[minimums[0]]
    for cutoff in range(int(minimums[0][1]),int(minimums[0][1]*1.3),5):
        for value in differences:
            if value[1]<cutoff and not value in alreadyChecked:
                isMinimum=True
                for value2 in alreadyChecked:
                    if sum([abs(value[0][i]-value2[0][i]) for i in range(3)])<50:
                        isMinimum=False
                if isMinimum:
                    minimums.append(value)
                alreadyChecked.append(value)
        if (cutoff-int(minimums[0][1]))%200 == 0:
            print(str(round((cutoff-int(minimums[0][1]))/int(minimums[0][1]*.3)*100))+'%')
    print(len(minimums),'connections.')
    pieceConnections=[]
    for minimum in minimums:
        pieceConnections.append(PieceConnection(biggerPiece,smallerPiece,minimum[0],minimum[2][0],minimum[2][1]))

    return pieceConnections

piece1 = Piece('Pieces Resized/Piece 2.png')
piece2 = Piece('Pieces Resized/Piece 4.png')

pieceConnections=getPieceShapeConnections(piece1,piece2)

for pieceConnection in pieceConnections:
    print('Connection:',pieceConnection.connectionValues)
    print('Shape Difference:',int(pieceConnection.shapeDifference))
    print('Color Difference:',pieceConnection.colorDifference)

    pieceConnection.saveImages()

    input()