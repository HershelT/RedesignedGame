from neccessaryImports import *
BACKGROUND_COLOR = cyan
AnimationSprites = [f'ImageReader{dir_sep}Animations{dir_sep}TNT-Animation.png']
AnimationSprites = pixelImage(AnimationSprites, SPRITE_COLOR_REPLACE, BACKGROUND_COLOR).getPixel(0)
ANIMATION_SHEET_LENGTH = len(AnimationSprites)
ANIMATION_SHEET_WIDTH = len(AnimationSprites[0])
ANIMATION_SIZE = 16
ANIMATION_SHEET = {}
class Animation:
    def __init__(self, name, frameSize = 4, sprite : list[list[list]] = [[]]):
        self.name = name
        self.frameSize = frameSize
        if sprite == [[]]:
            self.sprite = [[] for i in range(0, frameSize)]
    def getName(self):
        return self.name
    def getFrameSize(self):
        return self.frameSize
    def getSprite(self, frame = 0):
        return self.sprite[frame]
    #add a new sprite to the animation frame
    def setSprite(self, newSprite, frame = 0):
        self.sprite[frame] = newSprite

def scanAnimationSheet(animationSheet : list[list], ANIMATION_NAMES_LIST : list[Animation], placement= 0 ):
    for i in range(0, 1):
        for j in range(0, 4):
            ANIMATION_NAMES_LIST[i].setSprite(scanArea(animationSheet, (j*ANIMATION_SIZE, placement), ANIMATION_SIZE, ANIMATION_SIZE), j)
        ANIMATION_SHEET[ANIMATION_NAMES_LIST[i].getName()] = ANIMATION_NAMES_LIST[i]

ANIMATION_PLAYER = [Animation(name = "TNT Explosion", frameSize = 4)]


scanAnimationSheet(AnimationSprites, ANIMATION_PLAYER, 0)

# for i in range(0, ANIMATION_SHEET["TNT Explosion"].getFrameSize()):
#     printScreen(ANIMATION_SHEET["TNT Explosion"].getSprite(i))
#     time.sleep(0.5)