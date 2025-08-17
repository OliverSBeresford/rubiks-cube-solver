import numpy as np
from collections import OrderedDict

class Cube:
    # Adjacent rows/cols for each face, starting from the left and going clockwise
    # This is used to determine which rows/cols to rotate when a face is turned
    # For example, when turning the Up face clockwise, the Left, Back, Right,
    # and Front faces will have their rows rotated accordingly.
    # The slice notation is used to indicate which rows/columns are affected.
    allItems = slice(0, None)
    all_adjacent_faces = {
        'Up': OrderedDict({ # Note: OrderedDict is only needed for Python < 3.7
            'Left': (0, allItems),
            'Back': (0, allItems),
            'Right': (0, allItems),
            'Front': (0, allItems)
        }),
        'Down': OrderedDict({
            'Left': (2, allItems),
            'Front': (2, allItems),
            'Right': (2, allItems),
            'Back': (2, allItems)
        }),
        'Left': OrderedDict({
            'Back': (allItems, 2),
            'Up': (allItems, 0),
            'Front': (allItems, 0),
            'Down': (allItems, 0)
        }),
        'Right': OrderedDict({
            'Front': (allItems, 2),
            'Up': (allItems, 2),
            'Back': (allItems, 0),
            'Down': (allItems, 2)
        }),
        'Front': OrderedDict({
            'Left': (allItems, 2),
            'Up': (2, allItems),
            'Right': (allItems, 0),
            'Down': (0, allItems)
        }),
        'Back': OrderedDict({
            'Right': (allItems, 2),
            'Up': (allItems, 2),
            'Left': (allItems, 0),
            'Down': (2, allItems)
        })
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
    
    def turn(self, face, direction):
        """
        Turns the specified face in the given direction.
        :param face: 'Up', 'Down', 'Left', 'Right', 'Front', or 'Back'
        :param direction: 'clockwise' or 'counterclockwise'
        """
        
        # Handle special cases for middle, equator, and slice turns
        if face == 'Middle':
            self.turn_middle(direction)
            return
        elif face == 'Equator':
            self.turn_equator(direction)
            return
        elif face == 'Slice':
            self.turn_slice(direction)
            return
        
        # Misinput validation
        if face not in ['Up', 'Down', 'Left', 'Right', 'Front', 'Back']:
            raise ValueError("Invalid face name")
        
        if direction not in ['clockwise', 'counterclockwise']:
            raise ValueError("Invalid direction")
        
        direction_sign = -1 if direction == 'clockwise' else 1
        
        # Rotate the face
        self.__setattr__(face, np.rot90(self.__getattribute__(face), direction_sign))
        
        # This is an ordered dictionary of adjacent faces with their respective row/col selectors
        adjacent_faces = Cube.all_adjacent_faces[face]
        # Iterator for which faces are adjacent and which rows/cols to rotate
        selected_faces = list(adjacent_faces.keys())
        selected_indices = list(adjacent_faces.values())
        
        # Save the current state of the face to the left of the face being turned
        tempLeft = self.__getattribute__(selected_faces[0])[selected_indices[0]].copy()
        for i in range(direction_sign, len(selected_faces) * direction_sign, direction_sign):
            # Rotate the rows/cols of the adjacent faces
            self.__getattribute__(selected_faces[i - direction_sign])[selected_indices[i - direction_sign]] = self.__getattribute__(selected_faces[i])[selected_indices[i]].copy()
        
        # Update the last face with the saved state (either above or below depending on direction)
        self.__getattribute__(selected_faces[-direction_sign])[selected_indices[-direction_sign]] = tempLeft
        
    def turn_middle(self, direction):
        """
        Turns the middle slice of the cube in the given direction.
        (The slice in between the Left and Right faces)
        :param direction: 'clockwise' or 'counterclockwise'
        
        This assumes the perspective is facing the Left face
        """
        # Middle slice is a special case, it affects both Up and Down faces
        if direction not in ['clockwise', 'counterclockwise']:
            raise ValueError("Invalid direction")
    
        # Rotate the middle rows of Up, Front, Down, and Back faces
        if direction == 'clockwise':
            # Rotate Up, Front, Down, and Back faces
            temp = self.Up[:, 1].copy()
            self.Up[:, 1] = self.Back[:, 1]
            self.Back[:, 1] = self.Down[:, 1]
            self.Down[:, 1] = self.Front[:, 1]
            self.Front[:, 1] = temp
        else:
            # Rotate Up, Front, Down, and Back faces in the opposite direction
            temp = self.Up[:, 1].copy()
            self.Up[:, 1] = self.Front[:, 1]
            self.Front[:, 1] = self.Down[:, 1]
            self.Down[:, 1] = self.Back[:, 1]
            self.Back[:, 1] = temp
    
    def turn_equator(self, direction):
        """
        Turns the equator slice of the cube in the given direction.
        (The slice in between the Up and Down faces)
        :param direction: 'clockwise' or 'counterclockwise'
        
        This assumes the perspective is facing the Bottom face
        """
        if direction not in ['clockwise', 'counterclockwise']:
            raise ValueError("Invalid direction")
    
        # Rotate the middle rows of Left, Front, Right, and Back faces
        if direction == 'clockwise':
            # Rotate Left, Front, Right, and Back faces
            temp = self.Left[1, :].copy()
            self.Left[1, :] = self.Back[1, :]
            self.Back[1, :] = self.Right[1, :]
            self.Right[1, :] = self.Front[1, :]
            self.Front[1, :] = temp
        else:
            # Rotate Left, Front, Right, and Back faces in the opposite direction
            temp = self.Left[1, :].copy()
            self.Left[1, :] = self.Front[1, :]
            self.Front[1, :] = self.Right[1, :]
            self.Right[1, :] = self.Back[1, :]
            self.Back[1, :] = temp
            
    def turn_slice(self, direction):
        """
        Turns the slice of the cube in the given direction.
        (The slice in between the Front and Back faces)
        :param direction: 'clockwise' or 'counterclockwise'
        
        This assumes the perspective is facing the Front face
        """
        if direction not in ['clockwise', 'counterclockwise']:
            raise ValueError("Invalid direction")
    
        # Rotate the middle rows of Up, Left, Down, and Right faces
        if direction == 'clockwise':
            # Rotate Up, Left, Down, and Right faces
            temp = self.Up[1, :].copy()
            self.Up[1, :] = self.Left[:, 1]
            self.Left[:, 1] = self.Down[1, :]
            self.Down[1, :] = self.Right[:, 1]
            self.Right[:, 1] = temp
        else:
            # Rotate Up, Left, Down, and Right faces in the opposite direction
            temp = self.Up[1, :].copy()
            self.Up[1, :] = self.Right[:, 1]
            self.Right[:, 1] = self.Down[1, :]
            self.Down[1, :] = self.Left[:, 1]
            self.Left[:, 1] = temp
        

x = Cube()
print(x)
x.turn('Slice', 'clockwise')
print(x)