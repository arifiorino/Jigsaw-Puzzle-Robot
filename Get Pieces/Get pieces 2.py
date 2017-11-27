from PIL import Image
import math


vectors1=[[0,-1],[1,0],[0,1],[-1,0]]
vectors2=[[0,-1],[1,-1],[1,0],[1,1],[0,1],[-1,1],[-1,0],[-1,-1]]

def subtractVectors(a,b):
    return [a[0]-b[0],a[1]-b[1]]

allPiecesImage = Image.open("Pieces.png").convert('HSV')
allPiecesImagePixels = allPiecesImage.load()

backgroundColor=allPiecesImagePixels[0,0]

def colorDifference(color1,color2):
    return sum([abs(color1[i]-color2[i]) for i in range(len(color1))])

piecesCoordinates=[]

for y in range(allPiecesImage.size[1]):
    for x in range(allPiecesImage.size[0]):
        if colorDifference(allPiecesImagePixels[x,y],backgroundColor) > 150:
            if len(piecesCoordinates)>0 and piecesCoordinates[-1][-1][0] == x-1:
                piecesCoordinates[-1].append([x,y])
            else:
                piecesCoordinates.append([[x,y]])

done=False
while not done:
    done=True
    piece1I,piece2I=0,0
    for piece1I in range(len(piecesCoordinates)):
        for piece2I in range(len(piecesCoordinates)):
            if piece1I!=piece2I:
                for coor1 in piecesCoordinates[piece1I]:
                    for coor2 in piecesCoordinates[piece2I]:
                        if coor1[1]==coor2[1]:
                            done=False
                            break
                    if not done:
                        break
            if not done:
                break
        if not done:
            break

    new=piecesCoordinates[piece2I][::]
    piecesCoordinates.pop(piece2I)
    piecesCoordinates[piece1I].extend(new)

    print('Added',piece2I,'to',piece1I)
    print(len(piecesCoordinates))



# count=1
# for piece in pieces:
#     piece.save('Pieces/Piece '+str(count)+'.png')