from PIL import Image
import colorsys

boardImage = Image.open("Pieces.png").convert('HSV')
boardImagePixels = boardImage.load()

backgroundColor=boardImagePixels[0,0]

def colorDifference(color1,color2):
    return sum([abs(color1[i]-color2[i]) for i in range(len(color1))])

boardLines=[]
for y in range(boardImage.size[1]):
    boardLine=[]
    for x in range(boardImage.size[0]):
        if colorDifference(boardImagePixels[x,y],backgroundColor) > 130:
            if len(boardLine)>0 and boardLine[-1][-1] == x-1:
                boardLine[-1].append(x)
            else:
                boardLine.append([x])
    boardLines.append(boardLine)

class Piece:
    def __init__(self,firstLine,firstLineI):
        self.lines=[firstLine]
        self.firstLineI=firstLineI
        self.lastLineI=firstLineI
        self.image=None
    def addLine(self,line,lineI):
        if lineI==self.lastLineI:
            self.lines[-1].extend(line)
        if lineI==self.lastLineI+1:
            self.lastLineI+=1
            self.lines.append(line)
    def mergeWithPiece(self, piece2):
        firstLineDiff= self.firstLineI - piece2.firstLineI
        lastLineDiff= self.lastLineI - piece2.lastLineI

        if firstLineDiff>0:
            self.lines=[[]]*firstLineDiff+self.lines
        if firstLineDiff<0:
            piece2.lines=[[]]*(firstLineDiff*-1)+piece2.lines
        if lastLineDiff>0:
            piece2.lines=piece2.lines+[[]]*lastLineDiff
        if lastLineDiff<0:
            self.lines=self.lines+[[]]*(lastLineDiff*-1)

        self.firstLineI=min(self.firstLineI, piece2.firstLineI)
        self.lastLineI=max(self.lastLineI, piece2.lastLineI)
        for lineI in range(len(self.lines)):
            self.lines[lineI].extend(piece2.lines[lineI])
    def getSize(self):
        minX=1000000
        for line in self.lines:
            for x in line:
                if x<minX:
                    minX=x
        maxX=0
        for line in self.lines:
            for x in line:
                if x>maxX:
                    maxX=x
        return (maxX-minX+1,self.lastLineI-self.firstLineI+1)
    def saveImage(self,imageName):
        self.image=Image.new('RGBA',self.getSize())
        imagePixels=self.image.load()

        minX=1000000
        for line in self.lines:
            for x in line:
                if x<minX:
                    minX=x

        y=0
        for line in self.lines:
            for x in line:
                h,s,v=boardImagePixels[x,y+self.firstLineI]
                h,s,v=h/255.0,s/255.0,v/255.0
                r,g,b=colorsys.hsv_to_rgb(h,s,v)
                r,g,b=int(r*255),int(g*255),int(b*255)
                imagePixels[x-minX,y]=(r,g,b)
            y+=1
        self.image.convert('RGBA').save(imageName)

def mergePieceIs(pieceIs):
    global pieces
    piece=pieces[pieceIs[0]]
    for pieceI in pieceIs[1:]:
        piece.mergeWithPiece(pieces[pieceI])
    for pieceI in pieceIs[-1:0:-1]:
        pieces.pop(pieceI)

pieces=[]
for lineI in range(len(boardLines)):
    for lineGroup in boardLines[lineI]:
        connectPieceIs=[]
        for pieceI in range(len(pieces)):
            found=False
            if pieces[pieceI].lastLineI>=lineI-1:
                for x1 in lineGroup:
                    for x2 in pieces[pieceI].lines[lineI-pieces[pieceI].firstLineI-1]:
                        if x1==x2:
                            connectPieceIs.append(pieceI)
                            found=True
                            break
                    if found:
                        break
        if len(connectPieceIs)==1:
            pieces[connectPieceIs[0]].addLine(lineGroup,lineI)
        if len(connectPieceIs)==0:
            pieces.append(Piece(lineGroup,lineI))
        if len(connectPieceIs)>1:
            mergePieceIs(connectPieceIs)
            pieces[connectPieceIs[0]].addLine(lineGroup,lineI)

print(len(pieces),'total pieces.')

count=1
for piece in pieces:
    if piece.getSize()[0]*piece.getSize()[1]>20:
        piece.saveImage('Pieces/Piece '+str(count)+'.png')
        count+=1

print(count-1,'actual pieces.')