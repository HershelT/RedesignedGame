from ImageProcessor import *


SPRITE_COLOR_REPLACE = [f'ImageReader{dir_sep}BlocksSprites{dir_sep}backGroundColor.png']
SPRITE_COLOR_REPLACE = pixelImage(SPRITE_COLOR_REPLACE)
SPRITE_BLACK = SPRITE_COLOR_REPLACE.getPixel(0).getPixel(1, 0)
SPRITE_COLOR_REPLACE = SPRITE_COLOR_REPLACE.getPixel(0).getPixel(0, 0)


# spriteBlack = letters.getPixel(0).getPixel(0, 8)
# print(f"{spriteBlack} Hello World")
# import time
# time.sleep(5)