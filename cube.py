import numpy as np

class Cube:
    TRANSLATE = {
        'U': 'Up',
        'D': 'Down',
        'L': 'Left',
        'R': 'Right',
        'F': 'Front',
        'B': 'Back',
        'M': 'Middle',
        'E': 'Equator',
        'S': 'Slice'
    }
    
    # Mapping for adjacent faces when turning a face
    # Each entry: (from_face, from_idx, from_type, to_face, to_idx, to_type, reverse)
    TURN_MAPPINGS = {
        # UP face
        ('Up', 'clockwise'): [
            ('Back', 0, 'row', 'Right', 0, 'row', False),
            ('Right', 0, 'row', 'Front', 0, 'row', False),
            ('Front', 0, 'row', 'Left', 0, 'row', False),
            ('Left', 0, 'row', 'Back', 0, 'row', False),
        ],
        ('Up', 'counterclockwise'): [
            ('Back', 0, 'row', 'Left', 0, 'row', False),
            ('Left', 0, 'row', 'Front', 0, 'row', False),
            ('Front', 0, 'row', 'Right', 0, 'row', False),
            ('Right', 0, 'row', 'Back', 0, 'row', False),
        ],

        # DOWN face
        ('Down', 'clockwise'): [
            ('Front', 2, 'row', 'Right', 2, 'row', False),
            ('Right', 2, 'row', 'Back', 2, 'row', False),
            ('Back', 2, 'row', 'Left', 2, 'row', False),
            ('Left', 2, 'row', 'Front', 2, 'row', False),
        ],
        ('Down', 'counterclockwise'): [
            ('Front', 2, 'row', 'Left', 2, 'row', False),
            ('Left', 2, 'row', 'Back', 2, 'row', False),
            ('Back', 2, 'row', 'Right', 2, 'row', False),
            ('Right', 2, 'row', 'Front', 2, 'row', False),
        ],

        # LEFT face
        ('Left', 'clockwise'): [
            ('Up', 0, 'col', 'Front', 0, 'col', False),
            ('Front', 0, 'col', 'Down', 0, 'col', False),
            ('Down', 0, 'col', 'Back', 2, 'col', True),
            ('Back', 2, 'col', 'Up', 0, 'col', True),
        ],
        ('Left', 'counterclockwise'): [
            ('Up', 0, 'col', 'Back', 2, 'col', True),
            ('Back', 2, 'col', 'Down', 0, 'col', True),
            ('Down', 0, 'col', 'Front', 0, 'col', False),
            ('Front', 0, 'col', 'Up', 0, 'col', False),
        ],

        # RIGHT face
        ('Right', 'clockwise'): [
            ('Up', 2, 'col', 'Back', 0, 'col', True),
            ('Back', 0, 'col', 'Down', 2, 'col', True),
            ('Down', 2, 'col', 'Front', 2, 'col', False),
            ('Front', 2, 'col', 'Up', 2, 'col', False),
        ],
        ('Right', 'counterclockwise'): [
            ('Up', 2, 'col', 'Front', 2, 'col', False),
            ('Front', 2, 'col', 'Down', 2, 'col', False),
            ('Down', 2, 'col', 'Back', 0, 'col', True),
            ('Back', 0, 'col', 'Up', 2, 'col', True),
        ],

        # FRONT face
        ('Front', 'clockwise'): [
            ('Up', 2, 'row', 'Right', 0, 'col', False),
            ('Right', 0, 'col', 'Down', 0, 'row', True),
            ('Down', 0, 'row', 'Left', 2, 'col', False),
            ('Left', 2, 'col', 'Up', 2, 'row', True),
        ],
        ('Front', 'counterclockwise'): [
            ('Up', 2, 'row', 'Left', 2, 'col', True),
            ('Left', 2, 'col', 'Down', 0, 'row', False),
            ('Down', 0, 'row', 'Right', 0, 'col', True),
            ('Right', 0, 'col', 'Up', 2, 'row', False),
        ],

        # BACK face
        ('Back', 'clockwise'): [
            ('Up', 0, 'row', 'Left', 0, 'col', True),
            ('Left', 0, 'col', 'Down', 2, 'row', False),
            ('Down', 2, 'row', 'Right', 2, 'col', True),
            ('Right', 2, 'col', 'Up', 0, 'row', False),
        ],
        ('Back', 'counterclockwise'): [
            ('Up', 0, 'row', 'Right', 2, 'col', False),
            ('Right', 2, 'col', 'Down', 2, 'row', True),
            ('Down', 2, 'row', 'Left', 0, 'col', False),
            ('Left', 0, 'col', 'Up', 0, 'row', True),
        ]
    }
    
    def __init__(self, dictionary: dict=None, side_length: int=None):
        """
        Initializes a Cube object. If no dictionary is provided, creates a solved 3x3 cube.

        Args:
            dictionary (dict, optional): Dictionary mapping face names to 2D lists of stickers.
            side_length (int, optional): The length of one side of the cube. Defaults to 3.
        """
        if dictionary is None:
            # Solved rubik's Cube representation
            dictionary = {
                'Down': [['W','W','W'],['W','W','W'],['W','W','W']],
                'Right': [['R','R','R'],['R','R','R'],['R','R','R']],
                'Back': [['G','G','G'],['G','G','G'],['G','G','G']],
                'Up': [['Y','Y','Y'],['Y','Y','Y'],['Y','Y','Y']],
                'Left': [['O','O','O'],['O','O','O'],['O','O','O']],
                'Front': [['B','B','B'],['B','B','B'],['B','B','B']]
            }
            # Default side length
            side_length = 3

        # Set object attributes
        for face in dictionary:
            self.__setattr__(face, np.array(dictionary[face]))
        self.side_length = side_length
    
    def __str__(self):
        """
        Returns a string representation of the unfolded cube (net) in a human-readable format with colors.

        Returns:
            str: The unfolded cube as a colored string.
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
    
    def turn(self, face: str, direction: str, repeat: int = 1):
        """
        Turns the specified face in the given direction.

        Args:
            face (str): One of 'Up', 'Down', 'Left', 'Right', 'Front', or 'Back'.
            direction (str): Either 'clockwise' or 'counterclockwise'.
            repeat (int, optional): Number of times to repeat the turn. Defaults to 1.
        """
        
        # Handle special cases for middle, equator, and slice turns
        if face == 'Middle':
            self.turn_middle(direction, repeat)
            return
        elif face == 'Equator':
            self.turn_equator(direction, repeat)
            return
        elif face == 'Slice':
            self.turn_slice(direction, repeat)
            return
        
        # Misinput validation
        if face not in ['Up', 'Down', 'Left', 'Right', 'Front', 'Back']:
            raise ValueError("Invalid face name")
        
        if direction not in ['clockwise', 'counterclockwise']:
            raise ValueError("Invalid direction")
        
        direction_sign = -1 if direction == 'clockwise' else 1
        
        # Rotate the face
        self.__setattr__(face, np.rot90(self.__getattribute__(face), direction_sign))
        
        # Rotate the stickers between adjacent faces
        # This will transfer stickers between the affected faces according to the mapping
        self.rotate_stickers(face, direction)
        
        if repeat > 1:
            # Repeat the turn for the specified number of times
            self.turn(face, direction, repeat - 1)
        
    def turn_middle(self, direction: str, repeat: int = 1):
        """
        Turns the middle slice of the cube in the given direction (the slice in between the Left and Right faces).

        Args:
            direction (str): Either 'clockwise' or 'counterclockwise'.
            repeat (int, optional): Number of times to repeat the turn. Defaults to 1.

        Note:
            This assumes the perspective is facing the Left face.
        """
        # Middle slice is a special case, it affects both Up and Down faces
        if direction not in ['clockwise', 'counterclockwise']:
            raise ValueError("Invalid direction")
    
        # Rotate the middle rows of Up, Front, Down, and Back faces
        if direction == 'clockwise':
            # Rotate Up, Front, Down, and Back faces
            temp = self.Up[:, 1].copy()
            self.Up[:, 1] = np.flip(self.Back[:, 1]) # Needs to be flipped
            self.Back[:, 1] = np.flip(self.Down[:, 1]) # Needs to be flipped
            self.Down[:, 1] = self.Front[:, 1]
            self.Front[:, 1] = temp
        else:
            # Rotate Up, Front, Down, and Back faces in the opposite direction
            temp = np.flip(self.Up[:, 1].copy()) # Needs to be flipped
            self.Up[:, 1] = self.Front[:, 1]
            self.Front[:, 1] = self.Down[:, 1]
            self.Down[:, 1] = np.flip(self.Back[:, 1]) # Needs to be flipped
            self.Back[:, 1] = temp
        
        if repeat > 1:
            # Repeat the turn for the specified number of times
            self.turn_middle(direction, repeat - 1)
    
    def turn_equator(self, direction: str, repeat: int = 1):
        """
        Turns the equator slice of the cube in the given direction (the slice in between the Up and Down faces).

        Args:
            direction (str): Either 'clockwise' or 'counterclockwise'.
            repeat (int, optional): Number of times to repeat the turn. Defaults to 1.

        Note:
            This assumes the perspective is facing the Bottom face.
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
        
        if repeat > 1:
            # Repeat the turn for the specified number of times
            self.turn_equator(direction, repeat - 1)
            
    def turn_slice(self, direction: str, repeat: int = 1):
        """
        Turns the slice of the cube in the given direction (the slice in between the Front and Back faces).

        Args:
            direction (str): Either 'clockwise' or 'counterclockwise'.
            repeat (int, optional): Number of times to repeat the turn. Defaults to 1.

        Note:
            This assumes the perspective is facing the Front face.
        """
        if direction not in ['clockwise', 'counterclockwise']:
            raise ValueError("Invalid direction")
    
        # Rotate the middle rows of Up, Left, Down, and Right faces
        if direction == 'clockwise':
            # Rotate Up, Left, Down, and Right faces
            temp = self.Up[1, :].copy()
            self.Up[1, :] = np.flip(self.Left[:, 1])
            self.Left[:, 1] = self.Down[1, :]
            self.Down[1, :] = np.flip(self.Right[:, 1])
            self.Right[:, 1] = temp
        else:
            # Rotate Up, Left, Down, and Right faces in the opposite direction
            temp = np.flip(self.Up[1, :].copy())
            self.Up[1, :] = self.Right[:, 1]
            self.Right[:, 1] = np.flip(self.Down[1, :])
            self.Down[1, :] = self.Left[:, 1]
            self.Left[:, 1] = temp
        
        if repeat > 1:
            # Repeat the turn for the specified number of times
            self.turn_slice(direction, repeat - 1)

    def get_line(self, face: str, index: int, row_or_col: str, reverse: bool = False):
        """
        Gets a row or column from a face.

        Args:
            face (str): Face name ('Up', 'Down', 'Left', 'Right', 'Front', 'Back').
            index (int): Index of the row or column (0, 1, or 2 for a 3x3 cube).
            row_or_col (str): 'row' or 'col'.
            reverse (bool, optional): If True, reverses the line. Defaults to False.

        Returns:
            numpy.ndarray: The requested row or column.
        """
        # Get line from the specified face
        if row_or_col == 'row':
            line = getattr(self, face)[index, :].copy()
        elif row_or_col == 'col':
            line = getattr(self, face)[:, index].copy()
        else:
            raise ValueError("Invalid type, must be 'row' or 'col'")
        
        # Reverse the line if needed
        if reverse:
            line = np.flip(line)
        return line
        

    def set_line(self, face: str, index: int, row_or_col: str, values: np.ndarray):
        """
        Sets a row or column of a face.

        Args:
            face (str): Face name ('Up', 'Down', 'Left', 'Right', 'Front', 'Back').
            index (int): Index of the row or column (0, 1, or 2 for a 3x3 cube).
            row_or_col (str): 'row' or 'col'.
            values (numpy.ndarray): Numpy array of values to set.
        """
        if row_or_col == 'row':
            getattr(self, face)[index, :] = values.copy()
        elif row_or_col == 'col':
            getattr(self, face)[:, index] = values.copy()
        else:
            raise ValueError("Invalid type, must be 'row' or 'col'")
        

    def rotate_stickers(self, rotating_face: str, direction: str):
        """
        Transfers stickers between faces according to the mapping for a given face and direction.

        Args:
            rotating_face (str): The face being turned.
            direction (str): Either 'clockwise' or 'counterclockwise'.
        """
        steps = Cube.TURN_MAPPINGS.get((rotating_face, direction))
        if not steps:
            raise ValueError(f"No mapping for {rotating_face} {direction}")
        
        # Get the stickers from the first source face
        last_step = steps[0]
        temp_line = self.get_line(face=last_step[0], index=last_step[1], row_or_col=last_step[2], reverse=last_step[6])
        
        for source_face, source_idx, source_type, target_face, target_idx, target_type, reverse in steps[-1:0:-1]:
            # Get the stickers from the source face
            stickers = self.get_line(face=source_face, index=source_idx, row_or_col=source_type, reverse=reverse)
            
            # Set the stickers to the target face
            self.set_line(face=target_face, index=target_idx, row_or_col=target_type, values=stickers)
            
        # Set the stickers from the first source face to the last target face
        first_step = steps[0]
        self.set_line(face=first_step[3], index=first_step[4], row_or_col=first_step[5], values=temp_line)
        
        

    def run_turns(self, turns: str, debug: bool = False):
        """
        Runs a series of turns on the cube.

        Args:
            turns (str): A string of turns in the format "U U' R R' S etc...".
            debug (bool, optional): If True, prints debug information. Defaults to False.
        """
        turns = turns.upper().split()
        for turn in turns:
            if debug:
                print(f"Processing turn: {turn} or {Cube.TRANSLATE[turn[0]]}")
            
            # Translate letters to full turn / face names
            move = Cube.TRANSLATE[turn[0]]
            
            # Direction is counterclockwise if the second character is a single quote (')
            direction = 'clockwise' if len(turn) == 1 or turn[1] != '\'' else 'counterclockwise'
            
            # Repeat is 1 if no number is specified, otherwise it's the integer after the face letter
            repeat = 1 if len(turn) == 1 or turn[1] == '\'' else int(turn[1])
            
            # Perform the turn
            self.turn(move, direction, repeat)
            
            print(self)
        

x = Cube()
print(x)
x.run_turns("U B2 R2 B2 L2 F2 R2 D' F2 L2 B F' L F2 D U' R2 F' L' R'")
print(x)