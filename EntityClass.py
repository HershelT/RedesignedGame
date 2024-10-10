from ChunkLoader import *
from GameSprites import *
from GameItems import *
#Entity Functions to update screen entitites
PERIMETER_COLOR = white
PERIMETER_SIZE = 3
PERIMETER_RADIUS = 1





CROSS_HAIR = square(PERIMETER_SIZE+2, PERIMETER_SIZE+2, PERIMETER_COLOR)
drawLine(CROSS_HAIR, black, (PERIMETER_SIZE, 1), (1, PERIMETER_SIZE))
drawLine(CROSS_HAIR, black, (PERIMETER_SIZE, PERIMETER_SIZE), (1, 1))
addPerimeter(CROSS_HAIR, PERIMETER_COLOR, PERIMETER_RADIUS)



# PERIMETER_BLOCK = addPerimeter(square(BLOCK_SIZE-4, BLOCK_SIZE-4, BACKGROUND_COLOR), PERIMETER_COLOR, PERIMETER_RADIUS)
PERIMETER_BLOCK = CROSS_HAIR
def checkWithintBounds(x, y, SCENE_WIDTH, SCENE_HEIGHT):
    if x >= 0 and x < SCENE_WIDTH and y >= 0 and y < SCENE_HEIGHT:
        return True
    return False
def updatePlayerEntity(Scene, PLAYER: Player, SCENE_WIDTH, SCENE_HEIGHT):
    addToScreenWithoutColor(Scene, PLAYER.getSprite(), BACKGROUND_COLOR, PLAYER.getX()*BLOCK_SIZE, PLAYER.getY()*BLOCK_SIZE, True)
    #Get the cordinate direction  of the player
    facing = PLAYER.calculateMovement()
    #If not on edge of screen add cursor
    # if checkWithintBounds((PLAYER.getX()+facing[0]), (PLAYER.getY() + facing[1]), SCENE_WIDTH, SCENE_HEIGHT):
    #     #Add the perimeter block to the screen
    #     addToScreenWithoutColor(Scene, PERIMETER_BLOCK, BACKGROUND_COLOR, (PLAYER.getX()+facing[0])*BLOCK_SIZE + int(BLOCK_SIZE/PERIMETER_SIZE) , (PLAYER.getY() + facing[1])*BLOCK_SIZE + int(BLOCK_SIZE/PERIMETER_SIZE))

#Adds weapon player is holding to the screen
WEAPON = "Blue Pickaxe"
def addWeapon(Scene, PLAYER: Player, SCENE_WIDTH, SCENE_HEIGHT, forceMovement = False, Weapon = WEAPON):
    #Get the cordinate direction  of the player
    facing = PLAYER.calculateMovement(forceMovement)
    #If not on edge of screen
    if checkWithintBounds((PLAYER.getX()+facing[0]), (PLAYER.getY() + facing[1]), SCENE_WIDTH, SCENE_HEIGHT):
        #Add the perimeter block to the screen
        weapon : Item = ITEM_SHEET[Weapon]
        weapon = weapon.getSprite()
        displacementX = 0
        displacementY = 0
        if forceMovement:
            playerDirection = forceMovement
        else:
            playerDirection = PLAYER.getDirection()
        if playerDirection == "a" or playerDirection == "s":
            if playerDirection == "a": 
                weapon = mirror(weapon)
                displacementX = -12
                displacementY = 6
            else: 
                weapon = mirror(rotate(rotate(weapon, 270), 270))
                displacementX = -6
                displacementY = 12
            # addToScreenWithoutColor(Scene, weapon, BACKGROUND_COLOR, (PLAYER.getX()+facing[0])*BLOCK_SIZE + int(BLOCK_SIZE/2), (PLAYER.getY() + facing[1])*BLOCK_SIZE + int(BLOCK_SIZE/2))
        else:
            if playerDirection == "d": 
                displacementX = 4
                displacementY = 6
            if playerDirection == "w": 
                displacementX = -6
                displacementY = -4
        return addToScreenWithoutColor(Scene, weapon, BACKGROUND_COLOR, (PLAYER.getX()+facing[0])*BLOCK_SIZE - displacementX, (PLAYER.getY() + facing[1])*BLOCK_SIZE+displacementY)
    return False

LOOT_DROPS = {}
#Add Loot items to LOOT_DROPS
def addLootDrops(Chunk : ChunkLoader, PLAYER : Player,x, y):
    lootName = Chunk.getBlock(PLAYER.getChunk(), (x, y)).getName()
    if lootName in ITEM_SHEET:
        if PLAYER.getChunk() not in LOOT_DROPS:
            LOOT_DROPS[PLAYER.getChunk()] = {}
        LOOT_DROPS[PLAYER.getChunk()][(x, y)] = ITEM_SHEET[Chunk.getBlock(PLAYER.getChunk(), (x, y)).getName()]
#Adding small items to the screen to be picked up
def addItems(Scene, chunkNumber):
    loot = LOOT_DROPS[chunkNumber]
    for key in loot:
        addToScreenWithoutColor(Scene, expandPerimeter(loot[key].getSprite(),white, BACKGROUND_COLOR), BACKGROUND_COLOR, key[0]*BLOCK_SIZE + int(BLOCK_SIZE/4)-1, key[1]*BLOCK_SIZE + int(BLOCK_SIZE/4)-1)

#Draw the health to the screen
def updateHealth(Scene, PLAYER: Player, SCENE_WIDTH, SCENE_HEIGHT):
    #Get the health of the player
    health = PLAYER.getHealth()
    maxHealth = PLAYER.getMaxHealth()
    #Get the screen width
    # screenWidth = SCENE_WIDTH*BLOCK_SIZE
    #Get the screen height
    screenHeight = SCENE_HEIGHT*BLOCK_SIZE
    # screenWidth = SCENE_WIDTH*BLOCK_SIZE
    #Get the health bar
    healthBar = ITEM_SHEET["Bomb"].getSprite()
    inventory = PLAYER.getInventory()
    #Draw the health bar
    for i in range(0, maxHealth):
        if i >= health:
            healthBar = ITEM_SHEET["Empty Bomb"].getSprite()
        addToScreenWithoutColor(Scene, expandPerimeter(healthBar, white, BACKGROUND_COLOR, 1, BACKGROUND_COLOR), BACKGROUND_COLOR, ITEM_SIZE*(i) + i*1, screenHeight - ITEM_SIZE - 2)
    addNumbers(Scene, health, ITEM_SIZE*(i) + i*4, screenHeight - ITEM_SIZE - 2, red)
    #DRAW the inventory
    for i, keys in enumerate(inventory):
        addToScreenWithoutColor(Scene, expandPerimeter(ITEM_SHEET[keys].getSprite(), black, BACKGROUND_COLOR, 1, BACKGROUND_COLOR), BACKGROUND_COLOR, ITEM_SIZE*(i) + i*1, screenHeight - ITEM_SIZE*2 - 4)
        if inventory[keys] > 9:
            space = ""
        else:
            space = " "
        addToScreen(Scene, [[f'{white}{text_black}{space}{str(inventory[keys])}{reset}']], ITEM_SIZE*(i) + i*1, screenHeight - ITEM_SIZE*2 - 4)