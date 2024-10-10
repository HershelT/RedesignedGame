#import game files
from ChunkLoader import *
from GameSprites import *
from EntityClass import *
from GameItems import *
from GameAnimations import *

import threading

#initialize the screen
if len(sys.argv) <= 1:
    clear()
    resizeWindow(3)
time.sleep(0.5)
#Initialize the screen and chunk global variables
SCENE_HEIGHT = 7
SCENE_WIDTH = 10
CHUNK_COUNT = 3

# def washScreen(screen):
#     screen = square(SCENE_HEIGHT*BLOCK_SIZE, SCENE_WIDTH*BLOCK_SIZE, BACKGROUND_COLOR)

Scene = screen(SCENE_HEIGHT * BLOCK_SIZE, SCENE_WIDTH * BLOCK_SIZE, BACKGROUND_COLOR)

#Creating Chunks
Chunk = ChunkLoader(SCENE_HEIGHT, SCENE_WIDTH, BLOCK_SIZE, BLOCK_SIZE, BACKGROUND_COLOR)
# Function to regenerate random seed
def generateSeed(Chunk : ChunkLoader, currentChunk = 0):
    #Regenerate the chunks to have nothing
    Chunk.clearChunks()
    for i in range(0, CHUNK_COUNT):
        LOOT_DROPS[i] = {}
        Chunk.generateChunks()
        #place blocks randomly in the bounds of the chunk
        for y in range(0, SCENE_HEIGHT):
            for x in range(0, SCENE_WIDTH):
                Sprite = SPRITE_SHEET["Wood Flooring"]
                Chunk.setBlock(i, (x, y), Block(Sprite.getName(), Sprite.getSprite(), Sprite.getSolid(), Sprite.getMoveable(), Sprite.getBreakable(), Sprite.getBackground()))
                if y != int(SCENE_HEIGHT/2) or x != int(SCENE_WIDTH/2):
                    #randomly place solid blocks
                    if random.randint(0, 1) == 1:
                        # randomly place solid blocks
                        random_key = random.choice(BLOCKS_ORES).getName()
                        if random.randint(0, 1) == 1:
                            Sprite = SPRITE_SHEET["TNT"]
                            Chunk.setBlock(i, (x, y), Block(Sprite.getName(), Sprite.getSprite(), Sprite.getSolid(), Sprite.getMoveable(), Sprite.getBreakable(), Sprite.getBackground()))
                        else:
                            Sprite = SPRITE_SHEET[random_key]
                            Chunk.setBlock(i, (x, y), Block(Sprite.getName(), Sprite.getSprite(), Sprite.getSolid(), Sprite.getMoveable(), Sprite.getBreakable(), Sprite.getBackground()))

def checkIfBomb(x, y):
    if Chunk.getBlock(PLAYER.getChunk(), (x, y)).getBreakable() and Chunk.getBlock(PLAYER.getChunk(), (x, y)).getName() == "TNT":
        return True
    return False
fourEdges = [(1, 0), (-1, 0), (0, 1), (0, -1)]
def explode(x, y, isExploding = False):
    #Add entinities and weapons
    Chunk.fillScreenWithChunk(Scene, PLAYER.getChunk())
    updatePlayerEntity(Scene, PLAYER, SCENE_WIDTH, SCENE_HEIGHT)
    addItems(Scene, PLAYER.getChunk())
    addWeapon(Scene, PLAYER, SCENE_WIDTH, SCENE_HEIGHT, False, "Flint and Steel")
    updateHealth(Scene, PLAYER, SCENE_WIDTH, SCENE_HEIGHT)
    #Animate getting lit
    addToScreenWithoutColor(Scene, ITEM_SHEET["Fire"].getSprite(), BACKGROUND_COLOR, x*BLOCK_SIZE + 4,y*BLOCK_SIZE + 4, True)
    printScreen(Scene)
    time.sleep(0.2)
    #Animate exploding TNT
    if Chunk.getBlock(PLAYER.getChunk(), (x, y)).getBreakable() and Chunk.getBlock(PLAYER.getChunk(), (x, y)).getName() == "TNT":
        for i in range(0, 4):      
                addToScreenWithoutColor(Scene, ANIMATION_SHEET["TNT Explosion"].getSprite(i), BACKGROUND_COLOR, x*BLOCK_SIZE, y*BLOCK_SIZE, True)
                printScreen(Scene)
                time.sleep(0.1)
        Chunk.setBlock(PLAYER.getChunk(), (x, y), FLOOR_BLOCK.getBlockCopy())
    elif not isExploding:
        return
    #Checks all four edges to drop the loot
    for edge in fourEdges:
        block = Chunk.getBlock(PLAYER.getChunk(), (x + edge[0], y + edge[1]))
        if block.getBreakable() and block.getName() != "TNT":
            addLootDrops(Chunk, PLAYER, x + edge[0], y + edge[1])
            Chunk.setBlock(PLAYER.getChunk(), (x + edge[0], y + edge[1]), FLOOR_BLOCK.getBlockCopy())
    #Recursively explode the blocks
    for edge in fourEdges:
        if checkIfBomb(x + edge[0], y + edge[1]):
            explode(x + edge[0], y + edge[1], True)
generateSeed(Chunk)

# #Creating player sprite
# sprite = square(BLOCK_SIZE-4, BLOCK_SIZE-4, BACKGROUND_COLOR)
# drawDownTriangle(sprite, yellow, (6, 5), 4)
# drawDownTriangle(sprite, yellow, (5, 5), 4)
# drawUpTriangle(sprite, magenta, (6, 6), 4)
# drawUpTriangle(sprite, magenta, (5, 6), 4)
# playerSprite = addToScreen(square(BLOCK_SIZE, BLOCK_SIZE, BACKGROUND_COLOR ), sprite, 2, 2, True)
# for i in range(0, 3):
#     addToScreenWithColor(playerSprite, rotate(sprite, 270), BACKGROUND_COLOR, 2, 2, True)
# addToScreenWithoutColor(playerSprite, square(4, 4, rgb(255, 175, 135)), BACKGROUND_COLOR, 6, 10, True)
# drawLine(playerSprite, black, (5, 10), (4, 8))
# drawLine(playerSprite, black, (10, 10), (11, 8))
# drawRectangle(playerSprite, white, (4, 7), (6, 9))
# drawSetSquare(playerSprite, black, (7, 12), 1)
# drawSetSquare(playerSprite, black, (9, 12), 1)
FLOOR = SPRITE_SHEET["Wood Flooring"]
FLOOR_BLOCK = Block(FLOOR.getName(), FLOOR.getSprite(), FLOOR.getSolid(), FLOOR.getMoveable(), FLOOR.getBreakable(), FLOOR.getBackground())

#Create the player
STARTING_POSITION = (int(SCENE_WIDTH/2)-1, int(SCENE_HEIGHT/2))
PLAYER = Player("PLAYER", SPRITE_SHEET["PLAYER"].getSprite(), STARTING_POSITION[0], STARTING_POSITION[1], FLOOR_BLOCK)
AIR = Block("Air", square(BLOCK_SIZE, BLOCK_SIZE, BACKGROUND_COLOR), False, False, False, True)
#LOAD GAME MAP
for i in range(0, CHUNK_COUNT):
    Chunk.loadMap(i, LEVELS[i], BLOCK_INDEX)
PLAYER.setHealth(LEVELS[PLAYER.getChunk()][0])

#Fill the screen with the chunk
Chunk.fillScreenWithChunk(Scene, PLAYER.getChunk())
#initialize the keyboard listener
keys = MyKeyListener()
listener = keyboard.Listener(
    on_press=keys.on_press,
    on_release=keys.on_release
)
listener.start()

rotating = False
# run = False
# class RotateSpriteThread(threading.Thread):
#     def __init__(self):
#         threading.Thread.__init__(self)

#     def run(self):
#         global rotating
#         global run
#         while run:
#             rotating = True
#             time.sleep(0.1)
# rotatingThread = RotateSpriteThread()
# rotatingThread.start()
# run = False
FAIL = False
BROKE_BLOCK = False

#Main game loop
triggerChange = True
while not keys.is_esc_pressed():
    #Screen is updated only when there is a change
    # KEY_PRESSED = keys.get_pressed_key()
    if triggerChange:
        #Update the screen
        Chunk.fillScreenWithChunk(Scene, PLAYER.getChunk())
        #Update the player's position (update entities)
        updatePlayerEntity(Scene, PLAYER, SCENE_WIDTH, SCENE_HEIGHT)
        
        if (PLAYER.getX(), PLAYER.getY()) in LOOT_DROPS[PLAYER.getChunk()]:
            letter = False
            if PLAYER.getDirection() == "w" or PLAYER.getDirection() == "s": letter = "d"
            if PLAYER.getX() == 0: letter = "d"
            elif PLAYER.getX() == SCENE_WIDTH - 1: letter = "a"
            overwrite = addWeapon(Scene, PLAYER, SCENE_WIDTH, SCENE_HEIGHT, letter, LOOT_DROPS[PLAYER.getChunk()][(PLAYER.getX(), PLAYER.getY())].getName())
            PLAYER.addToInventory(LOOT_DROPS[PLAYER.getChunk()][(PLAYER.getX(), PLAYER.getY())].getName())
            del LOOT_DROPS[PLAYER.getChunk()][(PLAYER.getX(), PLAYER.getY())]
            addItems(Scene, PLAYER.getChunk())
            updateHealth(Scene, PLAYER, SCENE_WIDTH, SCENE_HEIGHT)
            printScreen(Scene)
            time.sleep(0.3)
            if overwrite: addToScreen(Scene, overwrite[0], overwrite[1], overwrite[2])
        else:
            addItems(Scene, PLAYER.getChunk())  
            updateHealth(Scene, PLAYER, SCENE_WIDTH, SCENE_HEIGHT)
        if BROKE_BLOCK:
            BROKE_BLOCK = False
            letter = PLAYER.getDirection()
            if letter == "a" or letter == "d":
                letter = "w"
            else:
                letter = "d"
            overwrite = addWeapon(Scene, PLAYER, SCENE_WIDTH, SCENE_HEIGHT, letter)
            printScreen(Scene)
            time.sleep(0.1)
            if overwrite:
                addToScreen(Scene, overwrite[0], overwrite[1], overwrite[2])
        #Add entinities and weapons
        addWeapon(Scene, PLAYER, SCENE_WIDTH, SCENE_HEIGHT)
        updateHealth(Scene, PLAYER, SCENE_WIDTH, SCENE_HEIGHT)
        #DisplayScreen
        printScreen(Scene)
        print(f"{black} X: {PLAYER.getX()} Y: {PLAYER.getY()} Chunk: {PLAYER.getChunk()} {reset}", flush=True)
        MovementInFront = PLAYER.calculateMovement()
        blockName = Chunk.getBlock(PLAYER.getChunk(), (PLAYER.getX() + MovementInFront[0], PLAYER.getY() + MovementInFront[1]))
        print(f" {grey}BlockFacing: {blockName.getName()}{reset} \
                \n {red}IsSolid: {blockName.getSolid()}{reset} \
                \n {blue}IsMoveable: {blockName.getMoveable()}{reset} \
                \n {magenta}IsBreakable: {blockName.getBreakable()}{reset} \
                \n", flush=True)
        time.sleep(0.05)
        triggerChange = False

    movement = keys.wasd()
    if (movement != False):
        #Update the player's last position
        PLAYER.setLastX(PLAYER.getX())
        PLAYER.setLastY(PLAYER.getY())
        #Which direction the player is facing
        previousDirection = PLAYER.getDirection()
        PLAYER.setDirection(movement) 
        #Calculate the movement of the player
        toMove = PLAYER.calculateMovement()
        #Move the player
        PLAYER.setX(PLAYER.getX() +toMove[0])
        PLAYER.setY(PLAYER.getY() + toMove[1])
        triggerChange = False
        BlockToCheck = Chunk.getBlock(PLAYER.getChunk(), (PLAYER.getX(), PLAYER.getY()))
        if  BlockToCheck.getSolid() or (PLAYER.getX() == PLAYER.getLastX() and PLAYER.getY() == PLAYER.getLastY()):
            #Push Block Forward
            if BlockToCheck.getMoveable():                
                #Can only swap if next block is air
                if Chunk.getBlock(PLAYER.getChunk(), (PLAYER.getX() + toMove[0], PLAYER.getY() + toMove[1])).getBackground():
                    #Swap the block with the air block
                    Chunk.swapBlocks(PLAYER.getChunk(), (PLAYER.getX(), PLAYER.getY()), (PLAYER.getX() + toMove[0], PLAYER.getY() + toMove[1])) 
                    #Update the screen
                    triggerChange = True
            #If no interaction happens (i.e movement is blocked) then reset the player's position
            if not triggerChange:
                #only update the screen if the player's direction changes (working on pointer)
                if not (previousDirection == PLAYER.getDirection()):
                    triggerChange = True
                PLAYER.setX(PLAYER.getLastX())
                PLAYER.setY(PLAYER.getLastY())
                # keys.keys_pressed.discard(all)
        else:
            #Set old position to what was overwritten
            Chunk.setBlock(PLAYER.getChunk(), (PLAYER.getLastX(), PLAYER.getLastY()), PLAYER.getBlockBehind().getBlockCopy())
            # save the block the player is about to step on to the player's block behind
            PLAYER.setBlockBehind(Chunk.getBlock(PLAYER.getChunk(), (PLAYER.getX(), PLAYER.getY())).getBlockCopy())
            #Update the screen
            triggerChange = True
    #Place a TNT block
    if keys.is_t_pressed():
            ToMove = PLAYER.calculateMovement()
            #Place a TNT block if the block is breakable
            if Chunk.getBlock(PLAYER.getChunk(), (PLAYER.getX() + ToMove[0], PLAYER.getY() + ToMove[1])).getBackground():
                if "TNT" in PLAYER.getInventory():
                    #subtract the TNT block from the player's inventory
                    PLAYER.inventory["TNT"] -= 1
                    if PLAYER.inventory["TNT"] == 0:
                        del PLAYER.inventory["TNT"]
                    Chunk.setBlock(PLAYER.getChunk(), (PLAYER.getX() + ToMove[0], PLAYER.getY() + ToMove[1]), convertToBlock(SPRITE_SHEET["TNT"]))
                    #Update the screen
                    triggerChange = True
    #Trade items for something
    if keys.is_q_pressed():
        tempInventory = PLAYER.getInventory()
        if "Diamond Ore" in tempInventory:
            if tempInventory["Diamond Ore"] >= 3:
                PLAYER.inventory["Diamond Ore"] -= 3
                if PLAYER.inventory["Diamond Ore"] == 0:
                    del PLAYER.inventory["Diamond Ore"]
                PLAYER.addToInventory("Health Potion")
                #Update the screen
                triggerChange = True
    #consume health potion
    if keys.is_v_pressed():
        if "Health Potion" in PLAYER.getInventory() and PLAYER.getHealth() < PLAYER.getMaxHealth():
            PLAYER.setHealth(PLAYER.getHealth() + 1)
            PLAYER.inventory["Health Potion"] -= 1
            if PLAYER.inventory["Health Potion"] == 0:
                del PLAYER.inventory["Health Potion"]
            #Update the screen
            triggerChange = True
    #Move between Chunks
    if keys.is_c_pressed() and PLAYER.getChunk() < Chunk.getChunkCount()-1:
        #set the block behind before moving to the next chunk
        Chunk.setBlock(PLAYER.getChunk(), (PLAYER.getX(), PLAYER.getY()), PLAYER.getBlockBehind().getBlockCopy())
        PLAYER.setChunk(PLAYER.getChunk() + 1)
        # Chunk.changeBlockSprite(PLAYER.getChunk(), (PLAYER.getX(), PLAYER.getY()), PLAYER.getSprite())
        triggerChange = True
    if keys.is_z_pressed() and PLAYER.getChunk() > 0:
        Chunk.setBlock(PLAYER.getChunk(), (PLAYER.getX(), PLAYER.getY()), PLAYER.getBlockBehind().getBlockCopy())
        PLAYER.setChunk(PLAYER.getChunk() - 1)
        # Chunk.changeBlockSprite(PLAYER.getChunk(), (PLAYER.getX(), PLAYER.getY()), PLAYER.getSprite())
        triggerChange = True
    #blow up around blocks on left, top, right, bottom
    if keys.is_b_pressed():
        #Get the cordinate direction  of the player
        facing = PLAYER.calculateMovement()
        #Get the block to blow up
        block = Chunk.getBlock(PLAYER.getChunk(), (PLAYER.getX() + facing[0], PLAYER.getY() + facing[1]))
        #If the block is breakable
        if block.getName() == "TNT":
            #Animate getting lit
            printScreen(Scene)
            explode(PLAYER.getX() + facing[0], PLAYER.getY() + facing[1])
            triggerChange = True
            FAIL = not PLAYER.setHealth(PLAYER.getHealth() - 1)
    if keys.is_x_pressed() or rotating:
        #Rotate the player sprite
        PLAYER.setSprite(rotate(PLAYER.getSprite(), 270))
        #Update the screen
        triggerChange = True
        if rotating:
            rotating = False
    #erase the next block
    if keys.is_e_pressed():
        ToMove = PLAYER.calculateMovement()
        #change block to air if block is breakable
        if Chunk.getBlock(PLAYER.getChunk(), (PLAYER.getX() + ToMove[0], PLAYER.getY() + ToMove[1])).getBreakable():
            addLootDrops(Chunk, PLAYER, PLAYER.getX() + ToMove[0], PLAYER.getY() + ToMove[1])
            Chunk.setBlock(PLAYER.getChunk(), (PLAYER.getX() + ToMove[0], PLAYER.getY() + ToMove[1]), FLOOR_BLOCK.getBlockCopy())
            #update screen
            BROKE_BLOCK = True
            triggerChange = True
    #Regenerate the blocks
    if keys.is_r_pressed():
        #Regenerate the blocks into a new seed
        generateSeed(Chunk)
        #Update the screen
        triggerChange = True
    #Increase health
    if keys.is_h_pressed():
        PLAYER.setHealth(PLAYER.getHealth() + 1)
        #Update the screen
        triggerChange = True
    #load predetermined map
    if keys.is_m_pressed() or FAIL:
        LOOT_DROPS[PLAYER.getChunk()] = {}
        Chunk.fillScreenWithChunk(Scene, PLAYER.getChunk())
        for i in range(0, 8):
            addToScreen(Scene, PLAYER.getBlockBehind().getBlockCopy().getSprite(), PLAYER.getX()*BLOCK_SIZE, PLAYER.getY()*BLOCK_SIZE)
            PLAYER.setSprite(rotate(PLAYER.getSprite(), 270))
            addToScreenWithoutColor(Scene, PLAYER.getSprite(), BACKGROUND_COLOR, PLAYER.getX()*BLOCK_SIZE, PLAYER.getY()*BLOCK_SIZE)
            printScreen(Scene)
            time.sleep(0.2)
        Chunk.setBlock(PLAYER.getChunk(), (PLAYER.getX(), PLAYER.getY()), PLAYER.getBlockBehind().getBlockCopy())
        #RESET the player and the blocks map
        PLAYER.setHealth(PLAYER.getMaxHealth())
        PLAYER.setX(STARTING_POSITION[0])
        PLAYER.setY(STARTING_POSITION[1])
        PLAYER.setLastX(STARTING_POSITION[0])
        PLAYER.setLastY(STARTING_POSITION[1])
        PLAYER.setInventory({})
        #Regenerate the blocks into a new seed
        PLAYER.setHealth(LEVELS[PLAYER.getChunk()][0])
        Chunk.loadMap(PLAYER.getChunk(), LEVELS[PLAYER.getChunk()], BLOCK_INDEX)
        # PLAYER.setChunk()
        PLAYER.setBlockBehind(Chunk.getBlock(PLAYER.getChunk(), (PLAYER.getX(), PLAYER.getY())).getBlockCopy())
        time.sleep(0.5)
        #Update the screen
        triggerChange = True
        FAIL = False
    keys.keys_pressed.discard(all)

run = False
# rotatingThread.join()
sys.exit()    
