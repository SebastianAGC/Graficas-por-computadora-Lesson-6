
def getPossibleValues(pixels):
    array = []
    step = 2 / pixels
    start = -1
    while start < 1:
        array.append(start)
        start = start + step
    return array

def getPixelValues(minValue, maxValue, valueArray):
    min = 0
    max = 0
    for i in range(len(valueArray)):
        if(valueArray[i] > minValue):
            min = i-1
            break

    for i in range(len(valueArray)):
        if(valueArray[i] > maxValue):
            max = i-1
            break
    return min, max

def normalize(x, y, viewPort):
    newX = int((x + 1) * (viewPort["width"] / 2) + viewPort["x"])
    newY = int((y + 1) * (viewPort["heigth"] / 2) + viewPort["y"])
    return newX, newY