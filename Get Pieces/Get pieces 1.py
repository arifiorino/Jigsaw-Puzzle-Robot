from PIL import Image
import sys

#Recursion didn't work :(

vectors1=[[0,-1],[1,0],[0,1],[-1,0]]
vectors2=[[0,-1],[1,-1],[1,0],[1,1],[0,1],[-1,1],[-1,0],[-1,-1]]

allPieces = Image.open("Pieces.png").convert('HSV')
allPiecesPixels = allPieces.load()

backgroundColor=allPiecesPixels[0,0]

pieces=[]
piecesPixels=[]

def colorDifference(color1,color2):
    return sum([abs(color1[i]-color2[i]) for i in range(len(color1))])

def createPiece(piece, piecePixels, startX, startY, x=0, y=0):

    if x<0:
        piece2=Image.new('HSV',[piece.size[0]+1,piece.size[1]])
        piece2.paste(piece,(1,0))
        piece=piece2
    if x>=piece.size[0]:
        piece2=Image.new('HSV',[piece.size[0]+1,piece.size[1]])
        piece2.paste(piece,(0,0))
        piece=piece2
    if y<0:
        piece2=Image.new('HSV',[piece.size[0],piece.size[1]+1])
        piece2.paste(piece,(0,1))
        piece=piece2
    if y>=piece.size[1]:
        piece2=Image.new('HSV',[piece.size[0],piece.size[1]+1])
        piece2.paste(piece,(0,0))
        piece=piece2

    piece.convert('RGBA').save('Pieces/Piece 1.png')

    piecePixels=piece.load()
    x,y=max(0,x),max(0,y)

    piecePixels[x,y]=allPiecesPixels[startX+x,startY+y]
    allPiecesPixels[startX+x,startY+y]=backgroundColor #delete from allpieces

    for offset in vectors1:
        if startX+x+offset[0] in range(allPieces.size[0]) and startY+y+offset[1] in range(allPieces.size[1]):
            print(colorDifference(allPiecesPixels[startX+x+offset[0],startY+y+offset[1]],backgroundColor))
            if colorDifference(allPiecesPixels[startX+x+offset[0],startY+y+offset[1]],backgroundColor) > 150:
                print('Adding',x+offset[0],y+offset[1])
                createPiece(piece,piecePixels,startX,startY,x+offset[0],y+offset[1])


for y in range(allPieces.size[1]):
    for x in range(allPieces.size[0]):
        print(allPiecesPixels[x,y],backgroundColor,colorDifference(allPiecesPixels[x,y],backgroundColor))
        if colorDifference(allPiecesPixels[x,y],backgroundColor) > 150:
            pieces.append(Image.new('HSV', (1,1), allPiecesPixels[x,y]))
            piecesPixels.append(pieces[-1].load())
            createPiece(pieces[-1],piecesPixels[-1],x,y)

count=1
for piece in pieces:
    piece.save('Pieces/Piece '+str(count)+'.png')