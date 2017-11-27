from PIL import Image


puzzle = Image.open("puzzle quarter.png")
puzzlePixels = puzzle.convert('HSV').load()

puzzleWidth=puzzle.size[0]
puzzleHeight=puzzle.size[1]

piece = Image.open("piece transformed quarter.png")
piecePixels = piece.convert('HSV').load()
piecePixelsAlpha = piece.convert('RGBA').load()
pieceWidth=piece.size[0]
pieceHeight=piece.size[1]

def findSimilarity(pieceX, pieceY):
    totalDifference=0
    for y in range(pieceHeight):
        for x in range(pieceWidth):
            pieceColor=piecePixels[x,y]
            puzzleColor=puzzlePixels[pieceX+x,pieceY+y]
            if (piecePixelsAlpha[x,y][3]==255): #if piece isn't transparent
                difference=sum([abs(pieceColor[i]-puzzleColor[i]) for i in range(3)])
                totalDifference+=difference
    return totalDifference

largest=0
smallest=findSimilarity(0, 0)

ds=[]
for y in range(0,puzzleHeight-pieceHeight,2):
    print(y/(puzzleHeight-pieceHeight)*100,'%')
    ds.append([])
    for x in range(0,puzzleWidth-pieceWidth,2):
        ds[-1].append(findSimilarity(x, y))
        if ds[-1][-1]>largest:
            largest=ds[-1][-1]
        if ds[-1][-1]<smallest:
            smallest=ds[-1][-1]

print(largest)
print(smallest)

im = Image.new("RGB", (len(ds[0]), len(ds)), "white")
imPixels=im.load()

for y in range(len(ds)):
    for x in range(len(ds[0])):
        imPixels[x,y]=tuple([int((ds[y][x]-smallest)/(largest-smallest)*255)]*3)
        if ds[y][x]==smallest:
            imPixels[x,y]=(255,0,0)
im.save('differences.png')