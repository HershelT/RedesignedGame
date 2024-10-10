# Import API
from neccessaryImports import *

#set a background color for all the sprites
BACKGROUND_COLOR = cyan
ITEM_SIZE = 8

#Get the Item Sheet
ItemSprites = [f'ImageReader{dir_sep}ItemSprites{dir_sep}Items.png']
ItemSprites = pixelImage(ItemSprites, SPRITE_COLOR_REPLACE, BACKGROUND_COLOR).getPixel(0)
#Get the lengths of the sprite sheet
ITEM_SHEET_LENGTH = len(ItemSprites)
ITEM_SHEET_WIDTH = len(ItemSprites[0])
#Set a dictionary to hold all the sprites
ITEM_SHEET = {}

class Item:
    def __init__(self, name, sprite : list[list] = []):
        self.name = name
        self.sprite = sprite
    def getName(self):
        return self.name
    def getSprite(self):
        return self.sprite
    def setSprite(self, newSprite):
        self.sprite = newSprite


def scanItemSheet(itemSheet : list[list], ITEM_NAMES_LIST : list[Item], placement= 0 ):
    for i in range(0, len(ITEM_NAMES_LIST)):
        ITEM_NAMES_LIST[i].setSprite(scanArea(itemSheet, (i*ITEM_SIZE, placement), ITEM_SIZE, ITEM_SIZE))
        ITEM_SHEET[ITEM_NAMES_LIST[i].getName()] = ITEM_NAMES_LIST[i]


ITEM_ORE_BLOCKS = [Item(name = "Iron Ore Block"),
                   Item(name = "Diamond Ore Block"),
                   Item(name = "Gold Ore Block"),
                   Item(name = "Emerald Ore Block")]
ITEM_TERRAIN = [Item(name = "Grass"),
                Item(name = "Dirt"),
                Item(name = "Grass Corner")]
ITEM_STONE = [Item(name = "Stone"),
              Item(name = "Mossy Cobblestone")]
ITEM_END = [Item(name = "Obsidian"),
            Item(name = "Portal Block"),
            Item(name = "Portal")]
# END = [Item(name, True, False, False) for name in END]
ITEM_TRAVEL = [Item(name = "Door"),
               Item(name = "Platform"),
               Item(name = "Ladder")]
ITEM_DECORATION = [Item(name = "Glass"),
                   Item(name = "Brick"),
                   Item(name = "Wood Plank"),
                   Item(name = "Stone Brick")]
ITEM_INTERACTABLE = [Item(name = "Chest"),
                     Item(name = "Item Frame")]
ITEM_NETHER = [Item(name = "Netherrack"),
            Item(name = "Fire"),
            Item(name = "TNT")]
# MOVEABLE = [Item(name = "TNT")]
ITEM_WEAPOONS = [Item(name = "Diamond Pickaxe"),
                 Item(name = "Wooden Sword"),
                 Item(name = "Blue Pickaxe"),
                 Item(name = "Flint and Steel")]
ITEM_ORES = [Item(name = "Iron Ore"),
             Item(name = "Diamond Ore"),
             Item(name = "Gold Ore"),
             Item(name = "Emerald Ore")]
ITEM_POTIONS = [Item(name = "Health Potion"),
                Item(name = "Bomb"),
                Item(name = "Heart"),
                Item(name = "Empty Heart"),
                Item(name = "Empty Bomb")]

ALL_ITEM_NAMES = [ITEM_ORE_BLOCKS, ITEM_TERRAIN, ITEM_STONE, 
                  ITEM_END, ITEM_TRAVEL, ITEM_DECORATION, ITEM_INTERACTABLE, 
                  ITEM_NETHER, ITEM_WEAPOONS, ITEM_ORES, ITEM_POTIONS]

for i, itemClass in enumerate(ALL_ITEM_NAMES, 1):
    scanItemSheet(ItemSprites, itemClass, ITEM_SHEET_LENGTH-(i*ITEM_SIZE))
