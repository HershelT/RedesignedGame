import re
#ABOUT: This file contains colors for the text and the pixels


#The reset and getting rid of colors 
reset = "\033[0m"
ansi_escape = re.compile(r'\033\[\d+m')

#Colors for text and font
text_black = "\033[30m"
text_red = "\033[31m"
text_green = "\033[32m"
text_yellow = "\033[33m"
text_blue = "\033[34m"
text_magenta = "\033[35m"
text_cyan = "\033[36m"
text_white = "\033[37m"
text_bright_black = "\033[90m"
text_bright_red = "\033[91m"
text_bright_green = "\033[92m"
text_bright_yellow = "\033[93m"
text_bright_blue = "\033[94m"
text_bright_magenta = "\033[95m"
text_bright_cyan = "\033[96m"
text_bright_white = "\033[97m"

#colors for pixels (highlight)
red = "\033[41m"
green = "\033[42m"
yellow = "\033[43m"
blue = "\033[44m"
magenta = "\033[45m"
cyan = "\033[46m"
white = "\033[47m"
black = "\033[40m"
purple = "\033[48;5;54m"
grey = "\033[48;5;236m"
silver = "\033[48;5;145m"
colorsDict = {
    0 : black,
    1 : red,
    2 : green,
    3 : yellow,
    4 : blue,
    5 : magenta,
    6 : cyan,
    7 : white,
    8 : purple,
    9 : grey,
    10 : silver,
    'r' : reset
}
#brigh colors for pixels (highlight)
bright_black = "\033[100m"
bright_red = "\033[101m"
bright_green = "\033[102m"
bright_yellow = "\033[103m"
bright_blue = "\033[104m"
bright_magenta = "\033[105m"
bright_cyan = "\033[106m"
bright_white = "\033[107m"
bright_purple = "\033[105m"
bright_orange = "\033[101m"
bright_lime = "\033[102m"
bright_teal = "\033[104m"
bright_pink = "\033[105m"
colorsBrightDict = {
    0 : bright_black,
    1 : bright_red,
    2 : bright_green,
    3 : bright_yellow,
    4 : bright_blue,
    5 : bright_magenta,
    6 : bright_cyan,
    7 : bright_white,
    8 : bright_purple,
    9 : bright_orange,
    10 : bright_lime,
    11 : bright_teal,
    12 : bright_pink,
    'r' : reset
}



#Rainbow colors
rainbow = [red, green, yellow, blue, magenta, cyan, white]
rainbow_bright = [bright_red, bright_green, bright_yellow, bright_blue, bright_magenta, bright_cyan, bright_white]

#Create a function to get the asci code value before a string by splitting after the m and returning the first value
def getColorFromAnsi(string):
    return string.split("m")[0] + "m"