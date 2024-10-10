#ABOUT: This file contains functions that manipulate a matrix (the screen)


#Transpose the matrix, meaning move the rows to collumns and collumns to rows
def transpose(matrix):
    return list(map(list, zip(*matrix)))

#Rotate the matrix to the right
def rotateRight(matrix):
    return list(map(list, zip(*matrix[::-1])))

#Rotate the matrix to the left
def rotateLeft(matrix):
    return list(map(list, zip(*matrix)))
def mirror(matrix):
    return [list(reversed(row)) for row in matrix]
def flip(matrix):
    return [row for row in matrix[::-1]]
def mirror(matrix):
    return [list(reversed(row)) for row in matrix]

#Rotate matrix by degrees from -360 and 360
#TO do make it so can rotate any degree using draw line
def rotate(matrix, degrees):
    degrees %= 360  # Simplify degrees with modulo

    rotations = {
        0: matrix,  # Return self for 0 degrees
        90: rotateLeft(matrix),
        180: flip(matrix),  # Return self after double rotateRight
        270: rotateRight(matrix),
    }

    try:
        rotation_func = rotations[degrees % 360]
    except KeyError:
        raise ValueError(f"Invalid rotation angle. Angle must be a multiple of 90, 180, 270, or 360. Got {degrees}")

    return rotation_func
    