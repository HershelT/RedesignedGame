from neccessaryImports import *
from GameSprites import *
from Maps import *
BACKGROUND_COLOR = cyan

class Block:
    def __init__(self, name, sprite : list[list], solid = False, moveable = False, breakable = False, isBackground = False):
        self.name = name
        self.sprite = sprite
        self.solid = solid
        self.moveable = moveable
        self.breakable = breakable
        self.background = isBackground
    def getName(self):
        return self.name
    def getSprite(self) -> list:
        return self.sprite
    def getSolid(self):
        return self.solid
    def getBlockCopy(self):
        return Block(self.name, self.sprite, self.solid, self.moveable, self.breakable, self.background)
    def getMoveable(self):
        return self.moveable
    def getBreakable(self):
        return self.breakable
    def getBackground(self):
        return self.background
    def setMoveable(self, newMoveable):
        self.moveable = newMoveable
    def setSolid(self, newSolid):
        self.solid = newSolid
    def setBreakable(self, newBreakable):
        self.breakable = newBreakable
    def drawOverSprite(self, sprite):
        self.sprite = addToScreen(self.sprite, sprite, 0, 0, True)
        return self.sprite
    def changeSprite(self, sprite):
        self.sprite = sprite
    def changeName(self, name):
        self.name = name
    


class Player:
    def __init__(self, name, sprite, x, y, block : Block = ("Air", square(16, 16, red), False), maxHealth = 5):
        self.name = name
        self.sprite = sprite
        self.blockBehind = block.getBlockCopy()
        self.x = x
        self.y = y
        self.currentChunk = 0
        self.lastDirection = "w"
        self.lastPosX = x
        self.lastPosY = y
        self.maxHealth = maxHealth
        self.health = maxHealth
        self.inventory = {}
    def getName(self):
        return self.name
    def getSprite(self):
        return self.sprite
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getChunk(self):
        return self.currentChunk
    def getBlockBehind(self) -> Block:
        return self.blockBehind.getBlockCopy()
    def getDirection(self):
        return self.lastDirection
    def getLastX(self):
        return self.lastPosX
    def getLastY(self):
        return self.lastPosY
    def getInventory(self):
        return self.inventory
    def getMaxHealth(self):
        return self.maxHealth
    def getHealth(self):
        return self.health
    def setLastX(self, lastX):
        self.lastPosX = lastX
    def setLastY(self, lastY):
        self.lastPosY = lastY
    def setBlockBehind(self, block : Block):
        self.blockBehind = block.getBlockCopy()
    def setX(self, x):
        self.x = x
    def setY(self, y):
        self.y = y
    def setSprite(self, sprite):
        self.sprite = sprite
    def setName(self, name):
        self.name = name
    def setDirection(self, direction):
        self.lastDirection = direction
    def setChunk(self, chunk):
        self.currentChunk = chunk
    def setHealth(self, health):
        if "max" in str(health): 
            self.health = self.maxHealth
        elif health > self.maxHealth:
            self.health = self.maxHealth
    
        else:
            self.health = health
        if health == 0:
            return False
        return True
    def setMaxHealth(self, maxHealth):
        self.maxHealth = maxHealth
    def setInventory(self, inventory):
        self.inventory = inventory
    def changeInventory(self, item, amount):
        self.inventory[item] += amount
    def addToInventory(self, item):
        if item in self.inventory:
            self.inventory[item] += 1
        else:
            self.inventory[item] = 1
    def calculateMovement(self, forceDirection = False):
        tempDirection = self.lastDirection
        directionTuple = (0, 0)
        if forceDirection:
            self.lastDirection = forceDirection
        if self.lastDirection == "w":
            directionTuple = (0, 1)
        elif self.lastDirection == "a":
            directionTuple =  (-1, 0)
        elif self.lastDirection == "s":
           directionTuple =  (0, -1)
        elif self.lastDirection == "d":
            directionTuple =  (1, 0)
        if forceDirection: 
            self.lastDirection = tempDirection
        return directionTuple


class ChunkLoader:
    def __init__(self, height, width, blockHeight, blockWidth, background = cyan):
        self.height = height
        self.width = width
        self.countChunks = 0
        self.chunks = {}
        self.blockHeight = blockHeight
        self.blockWidth = blockWidth
        self.background = background
    def addChunk(self, count):
        self.chunks[count] = {}
    def generateChunks(self):
        self.addChunk(self.countChunks)
        #Set all blocks to air within the chunk boundry
        for y in range(0, self.height):
            for x in range(0, self.width):
                self.chunks[self.countChunks][(x, y)] = Block("Air", square(self.blockHeight, self.blockWidth, self.background), False, False, False, True)
        #Creating invisibile walls around the chunk to help with collision and less checks
        for y in range(-1, self.height + 1):
            for x in range(-1, self.width + 1):
                if (x < 0 or x >= self.width) or (y < 0 or y >= self.height):
                    self.chunks[self.countChunks][(x, y)] = Block("Wall", square(self.blockHeight, self.blockWidth, black), True, False, False)
        self.countChunks += 1
    def regenerateChunks(self):
        self.countChunks = 0
        self.chunks = {}
        self.generateChunks()
    def getChunk(self, chunk):
        return self.chunks[chunk]
    def getBackground(self):
        return self.background
    def getBlock(self, chunk, blockPos) -> Block:
        return self.chunks[chunk][blockPos]
    def printChunk(self, chunk): #Print out the 2d array of blocks
        for y in range(0, self.height):
            for x in range(0, self.width):
                block : Block = self.chunks[chunk][(x, y)]
                printScreen(block.getSprite())
    def setBlock(self, chunk, blockPos, block : Block) -> Block:
        previousBlock = self.chunks[chunk][blockPos]
        self.chunks[chunk][blockPos] = block
        return previousBlock
    def changeBlockSprite(self, chunk, blockPos, sprite):
        previousBlock = self.chunks[chunk][blockPos]
        self.chunks[chunk][blockPos].changeSprite(sprite)
        return previousBlock
    def drawOverBlock(self, chunk, blockPos, sprite):
        self.chunks[chunk][blockPos].drawOverSprite(sprite)
    def swapBlocks(self, chunk, blockPos1, blockPos2):
        tempBlock = self.chunks[chunk][blockPos1]
        self.chunks[chunk][blockPos1] = self.chunks[chunk][blockPos2]
        self.chunks[chunk][blockPos2] = tempBlock
    def clearChunks(self):
        self.chunks = {}
        self.countChunks = 0

    def getChunks(self):
        return self.chunks
    def getChunkCount(self):
        return self.countChunks
    def getHeight(self):
        return self.height
    def getWidth(self):
        return self.width
    def getBlockHeight(self):
        return self.blockHeight
    def getBlockWidth(self):
        return self.blockWidth
    
    def loadMap(self, ChunkNumber, mapToLoad, blockMap):
        # self.chunks[ChunkNumber] = {}
        
        mapToLoad = mapToLoad[1]
        for y in range(0, self.height):
            for x in range(0, self.width):
                block : Sprite = SPRITE_SHEET[blockMap[mapToLoad[self.height - y - 1][x]]]
                self.chunks[ChunkNumber][(x, y)] = Block(block.getName(), block.getSprite(), block.getSolid(), block.getMoveable(), block.getBreakable(), block.getBackground())
    
    #updates a scene object on screen, if trying to overwrite visuals
    def updateBlockOnScreen(self, screen, blockPos, sprite):
        return addToScreen(screen, sprite, blockPos[0]*self.blockWidth, blockPos[1]*self.blockHeight, True)
        
    def fillScreenWithChunk(self, screen, chunk):
        for y in range(0, self.height):
            for x in range(0, self.width):
                addToScreen(screen, self.chunks[chunk][(x, y)].getSprite(),  x * self.blockWidth, y * self.blockHeight)



#Convert Sprite to Block
def convertToBlock(sprite : Sprite):
    return Block(sprite.getName(), sprite.getSprite(), sprite.getSolid(), sprite.getMoveable(), sprite.getBreakable(), sprite.getBackground())

