
#### TO USE
#CALL THE FUNCTION 'from drawing import *'#
### In a main.py file
#ONLY IMPORT I NEED IS drawing.py
#ABOUT: This file contains functions that draw shapes and lines on the screen

#All import
from imports import *
#imports colors
from colors import *
#importing my own matrix math file
from matrix import *
#Imports rgb functions from rgb.py file to change colors
from rgb import *
#importing image reader
sys.path.insert(0, 'ImageReader')
from ImageReader import *

#initializing a clear command
clear_command = 'cls' if os.name == 'nt' else 'clear'
def clear():
    os.system(clear_command)

#setting a screen size
def screen(height, width, filling = purple):
    filling += "  " + reset
    #Creates a 2d array that acts as the screen
    return [[filling for x in range(width)] for y in range(height)]

#Printing Base Scene to the console
def printScreenTest(screen, clear = True, hideCursor = True):
    #Hide cursor
    sys.stdout.write('\033[?25l')
    sys.stdout.flush()
    # Create an off-screen buffer
    buffer = io.StringIO()

    for row in screen:
        # Write to the buffer instead of directly to the screen
        buffer.write(''.join(row) + '\n')
        buffer.flush()

    if clear:
        sys.stdout.write('\033[?25l')
        # Move the cursor to the top of the terminal
        sys.stdout.write('\033[H\033[?25l')
        sys.stdout.flush()

    # Swap the buffer with the screen
    sys.stdout.write(buffer.getvalue())
    sys.stdout.flush()

    # Clear the buffer for the next frame
    buffer.close()
    #unhides cursor after printing
    if not hideCursor:
        sys.stdout.write('\033[?25h')
        sys.stdout.flush()
    # Ends it with a reset
    sys.stdout.write(reset)
    sys.stdout.flush()


def printScreen(screen, clear=True, hideCursor=True):
    """Prints the screen to the terminal efficiently with reduced flicker.

    Args:
        screen: A list of lists representing the characters to be printed,
                where each inner list represents a row.
        clear: Whether to clear the screen before printing (default: True).
        hideCursor: Whether to hide the cursor after printing (default: True).
    """

    # Hide cursor
    sys.stdout.write('\033[?25l')
    sys.stdout.flush()


    buffer = ('\033[%d;1H%s\n' % (y + 1, ''.join(row))
          for y, row in enumerate(screen))

    # Combine and print the buffer in one go
    sys.stdout.write(''.join(buffer))
    sys.stdout.flush()

    # Unhide cursor if requested
    if not hideCursor:
        sys.stdout.write('\033[?25h')
        sys.stdout.flush()

    # Reset terminal settings (optional)
    sys.stdout.write(reset)  # You might need to define a "reset" string specific to your terminal
    sys.stdout.flush()



#Add lines to a screen screen at bottom left corner of drawing with (x, y)
def addToScreen(screen, obj, colIndex, rowIndex, getDrawnOver = False):
    # The pixels that are being drawn over when drawing new Image
    try:
        drawnOver = []
        screenLength = len(screen)
        objLength = len(obj)
        for i, row in enumerate(obj):
            rowLength = len(row)
            overList = screen[screenLength- (objLength+rowIndex)+i][colIndex:colIndex+rowLength]
            screen[screenLength - (objLength+rowIndex)+i][colIndex:colIndex+rowLength] = row
            drawnOver.append(overList)
        # Returns a list with the [drawnOver Image, the column it was at, and the row on the screen it was at]
        # To replace drawn over area call this function by setting it equal to something
        # Then say addToScreen(screen, something[0], something[1], something[2])
        if getDrawnOver:
            return screen
        return [drawnOver, colIndex, rowIndex]
    except IndexError:
        raise ValueError(f"Index ({colIndex, rowIndex}) out of bounds for \nLength:{len(screen)}\nWidth:{len(screen[0])}")

#Get pixel range from screen with certain height and width
def getFromScreen(screen, colIndex, rowIndex, height, width):
    try:
        return [row[colIndex:colIndex+width] for row in screen[len(screen) -(rowIndex+height):len(screen) - (rowIndex)]]
    except IndexError:
        raise ValueError(f"Index ({colIndex, rowIndex}) out of bounds for \nLength:{len(screen)}\nWidth:{len(screen[0])}")


#Add colors only on certain color pixels
#Is less efficient because it has to add eahc pixel individually in order to check
def addToScreenOnColor(screen, obj, onColor, colIndex, rowIndex, getDrawnOver = False):
    # The pixels that are being drawn over when drawing new Image
    try:
        drawnOver = []
        screenLength = len(screen)
        objLength = len(obj)
        onColor += "  " + reset
        for i, row in enumerate(obj):
            rowLength = len(row)
            overList = screen[screenLength- (objLength+rowIndex)+i][colIndex:colIndex+rowLength]
            drawnOver.append(overList)
            for j, pixel in enumerate(row):
                if screen[screenLength - (objLength+rowIndex)+i][colIndex+j] == onColor:
                    screen[screenLength - (objLength+rowIndex)+i][colIndex+j] = pixel
        if getDrawnOver:
            return screen
        return [drawnOver, colIndex, rowIndex]
    except IndexError:
        raise ValueError(f"Index ({colIndex, rowIndex}) out of bounds for \nLength:{len(screen)}\nWidth:{len(screen[0])}")
    
#Add colors from object given that are from given color
def addToScreenWithColor(screen, obj, withColor, colIndex, rowIndex, getDrawnOver = False):
    # The pixels that are being drawn over when drawing new Image
    try:
        drawnOver = []
        screenLength = len(screen)
        objLength = len(obj)
        withColor += "  " + reset
        for i, row in enumerate(obj):
            rowLength = len(row)
            overList = screen[screenLength- (objLength+rowIndex)+i][colIndex:colIndex+rowLength]
            drawnOver.append(overList)
            for j, pixel in enumerate(row):
                #checks if current pixel is color from obj that matches with color given
                if pixel in withColor:
                    screen[screenLength - (objLength+rowIndex)+i][colIndex+j] = pixel  
        if getDrawnOver:
            return screen
        return [drawnOver, colIndex, rowIndex]
    except IndexError:
        raise ValueError(f"Index ({colIndex, rowIndex}) out of bounds for \nLength:{len(screen)}\nWidth:{len(screen[0])}")

#Add colors from the obj to the screen as long as its not the color that is specified
def addToScreenWithoutColor(screen, obj, withoutColor, colIndex, rowIndex, getDrawnOver = False):
    # The pixels that are being drawn over when drawing new Image
    try:
        drawnOver = []
        screenLength = len(screen)
        objLength = len(obj)
        withoutColor += "  " + reset
        for i, row in enumerate(obj):
            rowLength = len(row)
            overList = screen[screenLength- (objLength+rowIndex)+i][colIndex:colIndex+rowLength]
            drawnOver.append(overList)
            for j, pixel in enumerate(row):
                #checks if current pixel is color from obj that matches with color given, then if so, skips
                if  not (pixel in withoutColor):
                    screen[screenLength - (objLength+rowIndex)+i][colIndex+j] = pixel
                # else:
                #     screen[screenLength - (objLength+rowIndex)+i][colIndex+j] = black + "  " + reset
        if getDrawnOver:
            return screen
        return [drawnOver, colIndex, rowIndex]
    except IndexError:
        raise ValueError(print(f"Index ({colIndex, rowIndex}) out of bounds for \nLength:{len(screen)}\nWidth:{len(screen[0])}"))








#Bresenhams line drawing lgorithm
def bresenham(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1

    x, y = x1, y1
    eps = 0

    if dx > 0:
        xi = 1
    else:
        xi = -1
        dx = -dx

    if dy > 0:
        yi = 1
    else:
        yi = -1
        dy = -dy

    if dx > dy:
        while x != x2:
            yield x, y
            eps += dy
            if (eps << 1) >= dx:
                y += yi
                eps -= dx
            x += xi
    else:
        while y != y2:
            yield x, y
            eps += dx
            if (eps << 1) >= dy:
                x += xi
                eps -= dy
            y += yi

    yield x2, y2


#Checks if a slope is within 0 and 1
def is_steep(dx, dy):
    return abs(dy) > abs(dx) + abs(dx // 2)

# Draws a line on the screen using the algorithm
def drawLine(screen, color, point1, point2):
    for x, y in bresenham(*point1, *point2):
        addToScreen(screen, square(1, 1, color), x, y)

#Draws a line on the screen using the algorithm with custom blocks fstored in a list
def drawLineCustom(screen, point1, point2, blockObjects : list):
    spot = 0
    length = len(blockObjects)
    for x, y in bresenham(*point1, *point2):
        addToScreen(screen, blockObjects[spot%length], x, y)
        if spot == length-1 and length > 1:
            break
        spot+=1


#Create a parrallelogram
def fillTrapezoid(screen, color, point1, point2, point3, point4):#x1, x2, y2, x3, y3, x4, y4):
    firstParts = []
    secondParts = []
    #no matter which way user gives input, it will draw lines correcrtly
    if point2[1] < point1[1]:
      point2, point1 = point1, point2
    if point4[1] < point3[1]: 
      point4, point3 = point3, point4

    #Populates the lists with the (x,y) elements
    for x, y in bresenham(*point1, *point2):
        firstParts.append([x, y])
    for x2, y2 in bresenham(*point3, *point4):
        secondParts.append([x2, y2])
    
    #Gets length of lines
    First = len(firstParts)
    Second = len(secondParts) 
    # print(f"{First} {Second}")

    #checks 
    if First > len(secondParts):
         bigger = firstParts
    else:
        bigger = secondParts

    #Enumerates through the biggest list and maps elements from First->Second
    for i, ele in enumerate(bigger):
        firsts = i
        seconds = i
        
        #Checks if one list is bigger than other, then just draws all remainuing points from the last point in the list
        if i >= First: firsts = len(firstParts) - 1
        if i >= Second: seconds = len(secondParts) - 1

        #Checks if slope is between 0 and 1 so it flips the x and y axis to graph it correctly
        if is_steep(firstParts[firsts][0] - secondParts[seconds][0], firstParts[firsts][1] - secondParts[seconds][1]):
            drawLine(screen, color, (firstParts[firsts][1], firstParts[firsts][0]), (secondParts[seconds][1], secondParts[seconds][0]))
        else:
            drawLine(screen, color, (firstParts[firsts][0], firstParts[firsts][1]), (secondParts[seconds][0], secondParts[seconds][1]))

#Draws an even parallogram with width (collumns) and length (rows) goes up and to the right
def drawPG(screen, color, width, length, point):
    point1 = (point[0], point[1])
    point2 = (point[0] + length, point[1]+length)
    point3 = (point[0] + width, point[1])
    point4 = (point[0] + length + width, point[1] + length)
    fillTrapezoid(screen, color, point1, point2, point3, point4)

#Draws any size three sided triangle
def drawTriangle(screen, color, point1, point2, point3):
  drawLine(screen, color, point1, point2)
  drawLine(screen, color, point2, point3)   
  drawLine(screen, color, point1, point3)
#Draws a square or rectangle
def square(length, width, color = bright_yellow):
    color += "  " + reset
    return [[color for x in range(width)] for y in range(length)]

#Draws a square with a inner color and a perimeter color
def hollowSquare(length, width, colorOuter = bright_yellow, colorInner = bright_white):
    colorOuter += "  " + reset
    colorInner += "  " + reset
    hSquare = [[colorInner for x in range(width)] for y in range(length)]
    for x in range(0, width):
        hSquare[0][x] = colorOuter
        hSquare[length-1][x] = colorOuter
    
    for y in range(0, len(hSquare)):
        hSquare[y][0] = colorOuter
        hSquare[y][len(hSquare[0])-1] = colorOuter
    return hSquare

#Draws a set size triangle at with top of triangle at center
def drawUpTriangle(screen, color, center, radius):
    for i in range(0, radius):
        drawLine(screen, color, (center[0]+i, center[1]-i), (center[0]-i, center[1]-i))

def drawRightTriangle(screen, color, center, radius):
    for i in range(0, radius):
        drawLine(screen, color, (center[0]-i, center[1]-i), (center[0]-i, center[1]+i))

def drawLeftTriangle(screen, color, center, radius):
    for i in range(0, radius):
        drawLine(screen, color, (center[0]+i, center[1]+i), (center[0]+i, center[1]-i))

def drawDownTriangle(screen, color, center, radius):
    for i in range(0, radius):
        drawLine(screen, color, (center[0]+i, center[1]+i), (center[0]-i, center[1]+i))

def drawRectangle(screen, color, point1, point2):
    length = abs(point2[1] - point1[1])
    width = abs(point2[0] - point1[0])
    addToScreen(screen, square(length, width, color), min(point1[0], point2[0]), min(point1[1], point2[1]))


#Draws a set size square with bottom right corner being at center
def drawSetSquare(screen, color, center, length):
    addToScreen(screen, square(length, length, color), center[0], center[1])

#Draws a thick line with a thickness of your choosing
def drawThickLine(screen, color, start,end, length):
    count = 0
    for x, y in bresenham(*start, *end):
        if color == "rainbow":
            addToScreen(screen, square(length, length, rainbow[count]), x, y)
            count+=1
            if count == len(rainbow):
                count = 0
        else:
            addToScreen(screen, square(length, length, color), x, y)
    


#Get a scan of certain blocks and thickness depending on slop and thichness of line
#can use blocks for rotation and other things, as well as creating cool animations like navigating over a world
def getBlocks(object, point1, point2, height, width):
    listOfBlocks = []
    for x, y in bresenham(*point1, *point2):
        listOfBlocks.append([x, y, getFromScreen(object, x, y, height, width)])
    return listOfBlocks

#Gets a scan of pixels from a certain area
def scanArea(screen, point1, height, width):
    return getFromScreen(screen, point1[0], point1[1], height, width)

#Gets color from certain area
def getColor(screen, point1):
    return getFromScreen(screen, point1[0], point1[1], 1, 1)[0][0]

#adds border on a certain scaned area
def addBorderToArea(scene, point1, height, width, oldColor, newColor, ToScreen = True):
    #Gets the area that the user wants to put a border around
    scannedArea = scanArea(scene, point1, height, width)
    #create a new scene that is 2 larger than the scanned areag
    newScene = screen(len(scannedArea)+2, len(scannedArea[0])+2, rgb(1, 1, 1)) 
    #add the scanned area to the new scene To be used for addBorder Function
    addToScreen(newScene, scannedArea, 1, 1)
    #adds the border to the scanned area that was just placed on newScene
    addBorder(newScene, oldColor, newColor)
    #Scans the newScene and gets the object with a new border
    scanned = scanArea(newScene, (1, 1), height, width)
    #Adds the new border to the original screen that user gave if ToScreen is True
    if ToScreen:
        addToScreen(scene, scanned, point1[0], point1[1])
    #Returns the new screen with the border
    return scanned

#Increase size of object by a certain amount and add the perimeter color to that object
def createPermiter(object, perimeterSize, color):
    newObject = screen(len(object)+perimeterSize*2, len(object[0])+perimeterSize*2, color)
    addToScreen(newObject, object, perimeterSize, perimeterSize)
    return newObject







