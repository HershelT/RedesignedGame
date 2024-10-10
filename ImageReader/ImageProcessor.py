# Import the Pillow library, and other python libraries
from PIL import Image, ImageChops
import os
import re
import copy
import numpy as np
reset = "\033[0m"
black = "\033[40m"

# Check if the operating system is Windows
is_windows = os.name == 'nt'
dir_sep = '\\' if is_windows else '/'

def generate_ansi_colors():
    basic_colors = [(0, 0, 0), (128, 0, 0), (0, 128, 0), (128, 128, 0),
                    (0, 0, 128), (128, 0, 128), (0, 128, 128), (192, 192, 192),
                    (128, 128, 128), (255, 0, 0), (0, 255, 0), (255, 255, 0),
                    (0, 0, 255), (255, 0, 255), (0, 255, 255), (255, 255, 255)]    
    levels = [0, 95, 135, 175, 215, 255]
    extended_colors = [(r, g, b) for r in levels for g in levels for b in levels]    
    return basic_colors + extended_colors
ansi_colors = generate_ansi_colors()
# print(ansi_colors)


#Mapping function to make keys and values in a line
def map_function(line):
    # Read the keys and values
    key, value = line.strip().split(":")
    return key.strip(), value.strip()
#reads the gpl_file to get the keys and values using a mapping function
def read_gpl_file():
    with open(f"ImageReader{dir_sep}ansi_dict.gpl", "r")as file:
        # Skip the header lines
        for _ in range(3):
            next(file)
        # Use the map function to read the keys and values
        keys_and_values = dict(map(map_function, file))
    return keys_and_values

#write the pixel_to_ansicode dictionary values to a gpl file
def write_gpl_file():
    with open(f"ImageReader{dir_sep}ansi_dict.gpl", "w") as file:
        # Write the header
        file.write("pixel_to_ansicode = \n")
        file.write("ANSI Colors dictionary\n")
        file.write("Columns: 2\n")  
        # Write the colors
        for key, value in pixel_to_ansicode.items():    
            file.write(f'{key} : {value}\n')

#Creates a color pallete for aseprite on gpl file
def create_color_palette():
    with open("ansiDictionary.gpl", "w") as file:
        # Write the header
        file.write("GIMP Palette\n")
        file.write("Name: ANSI Colors\n")
        file.write("Columns: 4\n")
        file.write("#\n")
        # Write the colors
        for rgb in ansi_colors:
            file.write(f"{rgb[0]} {rgb[1]} {rgb[2]} Color\n")

pixel_to_ansicode = read_gpl_file()
# print(pixel_to_ansicode)

class Pixel: 
    def __init__(self, image: list):
        self.image = image
    #Sets a specific pixel to a new color
    def setPixel(self, row, col, color):
        self.image[row][col] = color + "  " + "\033[0m"
    #Replaces all the pixels with a new pixel color
    def replaceAllPixels(self, newColor):
        for row in range(len(self.image)):
            for col in range(len(self.image[row])):
                self.image[row][col] = newColor + "  " + "\033[0m"
    #Changes certain colored pixels to a new pixel
    def replacePixels(self, oldColor, newColor):
        for row in range(len(self.image)):
            for col in range(len(self.image[row])):
                if oldColor in self.image[row][col]:
                    self.image[row][col] = newColor + "  " + "\033[0m"
        return self.image
    #Makes the rows the columns and the columns the rows
    def transpose(self):
        self.image = list(map(list, zip(*self.image)))
    def rotateRight(self):
        self.image = list(map(list, zip(*self.image[::-1])))
    def rotateLeft(self):
        self.image = list(map(list, zip(*self.image)))
    def flip(self):
        self.image = [list(reversed(row)) for row in self.image]
    #Rotates the matrix by a set degrees between -360 and 360 degrees
    def rotate(self, degrees):
        degrees %= 360  # Simplify degrees with modulo

        rotations = {
            0: lambda: self,  # Return self for 0 degrees
            90: self.rotateLeft(),
            180: lambda: (self.rotateRight(), self.rotateRight()),  # Return self after double rotateRight
            270: self.rotateRight(),
        }

        try:
            rotation_func = rotations[degrees % 360]
        except KeyError:
            raise ValueError(f"Invalid rotation angle. Angle must be a multiple of 90, 180, 270, or 360. Got {degrees}")

        return rotation_func()

    #Gets the 2d array representation of the image
    def getImage(self):
        return self.image
    #returns a deepcopy of the 2d array
    def getCopy(self, image):
        return Pixel(copy.deepcopy(image))
    #gets certain color of pixel at speicifc position
    def getPixel(self, col, row):
        return self.image[row][col]
    #gets the length (amount of rows) in a 2d array
    def getLength(self):
        return len(self.image)
    #gets the width (amount of columns) in 2d array
    def getWidth(self):
        return len(self.image[0])
    
    

#Function for getting rgb values to asci code by giving parameters (r, g, b)
def rgb(r, g, b):
    #Checks if r,g,b value in stored dictionary of all rgb values and there corresponding ascii value
    #If it is not so, it calculates the ansi color closest to the rgb value, adds it to dictionary
    #and returns it
    if (r,g,b) not in pixel_to_ansicode:
        def distance(c1, c2):
            return sum((x1-x2)**2 for x1,x2 in zip(c1, c2))
        rgb_color = (r, g, b)
        # Find the index of the closest color in the ansi_colors list
        closest_color = min(range(len(ansi_colors)), key=lambda index: distance(rgb_color, ansi_colors[index]))
        # Return the ANSI color code
        pixel_to_ansicode[rgb_color] = "\033[48;5;{}m".format(closest_color)
        return "\033[48;5;{}m".format(closest_color)
    return pixel_to_ansicode[(r, g, b)] 




#Class for creating a 2d array image with right colors from a png file
#used for creating 2d sprites in aseprite or others and importing it
#Can add it to scenes using addToScreen
class pixelImage:

    @staticmethod
    def trim_image(img):
    # Convert the image to RGB if it's not already
        if img.mode != 'RGB':
            img = img.convert('RGB')

        # Create a background image of the same color as the corner pixel
        bg = Image.new('RGB', img.size, img.getpixel((0,0)))

        # Find the difference between the input image and the background image
        diff = ImageChops.difference(img, bg)

        # The difference is zero for all pixels that match the background color,
        # so we need to find the bounding box of the non-zero regions
        bbox = diff.getbbox()

        # If the bounding box is not None, crop the image to that bounding box
        if bbox:
            img = img.crop(bbox)

        return img
    def __init__(self, img : list, oldColor = False, newColor = False, findPixel = False, trim = False):
        imageList = []

        self.ImageAnscii = []
        for image in img:
            if trim:
                imageList.append(self.trim_image(Image.open(image)))
            else:
                imageList.append(Image.open(image))
        for rgb in imageList:
            pixel = self.getPixelToAnscii(rgb)
            pixel = Pixel(pixel)
            if oldColor != False:
                pixel = pixel.replacePixels(oldColor, newColor)
            self.ImageAnscii.append(pixel)

    def getAnsciiList(self):
        return self.ImageAnscii
    def size(self, image):
        width, height = image.size
        return width, height
    def rgb_to_anscii(self, r, g, b):
        return rgb(r,g,b)
    def getPixelToAnscii(self, image):
        # Convert the image to RGB if it's not already
        if image.mode != 'RGB':
            image = image.convert('RGB')
        #Map each pixel to a color from ascii
        ansi_codes = list(map(lambda pixel: (self.rgb_to_anscii(*pixel) + '  '), image.getdata()))
        # Convert the list of ANSI codes to a 2D numpy array and return it as a list
        np2d = np.array(ansi_codes).reshape(image.size[1], image.size[0])
        return np2d.tolist()
    #Prints the ascii image into a 2d array for each pixelImage in the list
    def printOutImage(self, imageAnscii : list):
        # drawing = self.colors.tolist()  
        print('\033[0m\n'.join(''.join(row) for row in imageAnscii), end=reset)
    def printOutNumpy(self, imageAnscii : list):
        print(np.array(imageAnscii))
    #returns the Pixel class of the image array at a specific index
    #use this to modify the image using the Pixel class
    def getPixel(self, index = 0) -> Pixel:
        return self.ImageAnscii[index]
    #Returns the 2d array of the pixel image at a certain index
    def getPixelImage(self, index = 0):
        array : Pixel = self.ImageAnscii[index]
        return array.getImage()
    


# # Save the scene by writing it to a file that can be looked at later 
# #create that function
# def saveScene(Scene, fileName = "Scene.txt", is2d = True):
#     # fileName = "Scene.txt"
#     with open(fileName, "w") as file:
#         if is2d:
#             for row in Scene:
#                 for col in row:
#                     # Seperate the characters by a * so that they can be split later
#                     file.write(str(col))
#                     file.write("*")
#                 file.write("\n")
#         else:
#             for col in Scene:
#                 file.write(str(col))
#                 file.write("*")
#     print(f"\033[42m Scene saved to {fileName} \033[0m")

# #Get the scene from the file that was saved
# def getScene(fileName = "Scene.txt"):
#     # fileName = "Scene.txt"
#     Scene = []
#     with open(fileName, "r") as file:
#         for line in file:
#             # Split off each charcter from the * and append it to the Scene and get the whole line as a list of elements split off by *
#             Scene.append(line.strip().split("*")[:-1])
#     return Scene













#declare all the images
# humanList = [f'ImageReader{dir_sep}PythonTerminalSprites{dir_sep}Human1.png',
#             f'ImageReader{dir_sep}PythonTerminalSprites{dir_sep}Human2.png',
#             f'ImageReader{dir_sep}PythonTerminalSprites{dir_sep}Human3.png',
#             f'ImageReader{dir_sep}PythonTerminalSprites{dir_sep}Human4.png',
#             f'ImageReader{dir_sep}PythonTerminalSprites{dir_sep}Human5.png',
#             f'ImageReader{dir_sep}PythonTerminalSprites{dir_sep}Human6.png',
#             f'ImageReader{dir_sep}PythonTerminalSprites{dir_sep}Human7.png',
#             f'ImageReader{dir_sep}PythonTerminalSprites{dir_sep}Human8.png',
#             f'ImageReader{dir_sep}PythonTerminalSprites{dir_sep}Human9.png',
#             f'ImageReader{dir_sep}PythonTerminalSprites{dir_sep}Human10.png',
#             f'ImageReader{dir_sep}PythonTerminalSprites{dir_sep}Human11.png']
# bulletList = [f'ImageReader{dir_sep}PythonTerminalSprites{dir_sep}Bullet1.png',
#             f'ImageReader{dir_sep}PythonTerminalSprites{dir_sep}Bullet2.png']
# heartList = [f'ImageReader{dir_sep}PythonTerminalSprites{dir_sep}Heart.png']
# healthList = [f'ImageReader{dir_sep}PythonTerminalSprites{dir_sep}Health1.png',
#               f'ImageReader{dir_sep}PythonTerminalSprites{dir_sep}Health2.png',
#               f'ImageReader{dir_sep}PythonTerminalSprites{dir_sep}Health3.png',]
# BackgroundList = [f'ImageReader{dir_sep}PythonTerminalSprites{dir_sep}Background.png']
# SlugThingList = [f'ImageReader{dir_sep}PythonTerminalSprites{dir_sep}SlugThing1.png']
# GameBoyList = [f'ImageReader{dir_sep}PythonTerminalSprites{dir_sep}GameBoy.png']

# Create a new PixelImage object for each image in the list
# Human  = pixelImage(humanList)
# Bullet = pixelImage(bulletList)
# Heart  = pixelImage(heartList)
# Health = pixelImage(healthList)
# Background = pixelImage(BackgroundList)
# SlugThing = pixelImage(SlugThingList)
# GameBoy = pixelImage(GameBoyList)


# write_gpl_file()

#Stores a file of all known pixel and asci codes, use this to write new one to save time 
#on loading on later computers






