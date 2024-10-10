import sys
# Add the DrawingAPI, ImageReader, and KeyboardActions directories to the path
sys.path.extend(['DrawingAPI', 'ImageReader', 'KeyboardActions'])
# Insert DrawingAPI
from DrawingAPI import *
# Import the ImageReader
from ImageReader import *
# Import the Keyboard Listener
from KeyboardActions import *

NUMBERS = [f'ImageReader{dir_sep}LettersSprites{dir_sep}SmallNumbers.png']
Numbers = pixelImage(NUMBERS, SPRITE_COLOR_REPLACE, cyan).getPixel(0)
NUMBERS = {}
for i in range(0, 10):
    NUMBERS[i] = scanArea(Numbers, (i*3, 0), 5, 3)
def addNumbers(Scene, number, x, y, color):
    for i in str(number):
        coloredNumber = NUMBERS[int(i)]
        # coloredNumber = changeRGB(coloredNumber, SPRITE_BLACK, color)
        addToScreenWithoutColor(Scene, changeRGB(coloredNumber, SPRITE_BLACK, color), cyan, x, y)
        x += 4