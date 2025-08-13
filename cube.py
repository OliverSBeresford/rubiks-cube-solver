import numpy as np

class Cube:
    # Adjacent rows for each face, starting from the left and going clockwise
    # This is used to determine which rows to rotate when a face is turned
    # For example, when turning the Up face clockwise, the Left, Back, Right,
    # and Front faces will have their rows rotated accordingly.
    # The slice notation is used to indicate which rows/columns are affected.
    allItems = slice(0, None)
    adjacent_rows = {
        'Up': {
            'Left': (0, allItems),
            'Back': (0, allItems),
            'Right': (0, allItems),
            'Front': (0, allItems)
        },
        'Down': {
            'Left': (2, allItems),
            'Front': (2, allItems),
            'Right': (2, allItems),
            'Back': (2, allItems)
        },
        'Left': {
            'Back': (allItems, 2),
            'Up': (allItems, 0),
            'Front': (allItems, 0),
            'Down': (allItems, 0)
        },
        'Right': {
            'Front': (allItems, 2),
            'Up': (allItems, 2),
            'Back': (allItems, 0),
            'Down': (allItems, 2)
        },
        'Front': {
            'Left': (allItems, 2),
            'Up': (2, allItems),
            'Right': (allItems, 0),
            'Down': (0, allItems)
        },
        'Back': {
            'Right': (allItems, 2),
            'Up': (allItems, 2),
            'Left': (allItems, 0),
            'Down': (2, allItems)
        }
    }
    
    def __init__(self, dictionary=None, side_length=None):
        if dictionary is None:
            # Solved rubik's Cube representation
            dictionary ={
                'Up': [['W','W','W'],['W','W','W'],['W','W','W']],
                'Right': [['R','R','R'],['R','R','R'],['R','R','R']],
                'Front': [['G','G','G'],['G','G','G'],['G','G','G']],
                'Down': [['Y','Y','Y'],['Y','Y','Y'],['Y','Y','Y']],
                'Left': [['O','O','O'],['O','O','O'],['O','O','O']],
                'Back': [['B','B','B'],['B','B','B'],['B','B','B']]
            }
            # Default side length
            side_length = 3

        # Set object attributes
        for face in dictionary:
            self.__setattr__(face, np.array(dictionary[face]))
        self.side_length = side_length
    
    def __str__(self):
        """
        Prints unfolded cube (net) in a human-readable format with colors.
        """

        # ANSI color codes for each sticker color
        color_map = {
            'W': '\033[37m',  # White
            'Y': '\033[33m',  # Yellow
            'R': '\033[31m',  # Red
            'O': '\033[38;5;208m',  # Orange (using 256-color mode)
            'G': '\033[32m',  # Green
            'B': '\033[34m',  # Blue
        }
        reset = '\033[0m'

        # Join a row into a string with colors
        def row_str(row):
            return ' '.join(f"{color_map.get(sticker, '')}{sticker}{reset}" for sticker in row)

        # Prepare each face
        U = self.Up
        R = self.Right
        F = self.Front
        D = self.Down
        L = self.Left
        B = self.Back

        s = ""
        # Up face
        for row in U:
            s += "      " + row_str(row) + "\n"
        # Left, Front, Right, Back faces
        for i in range(self.side_length):
            s += row_str(L[i]) + " " + row_str(F[i]) + " " + row_str(R[i]) + " " + row_str(B[i]) + "\n"
        # Down face
        for row in D:
            s += "      " + row_str(row) + "\n"
        return s

x = Cube()
print(x)