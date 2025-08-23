from cube import Cube
from rubiks_display import RubiksCube3DDisplay

# Initialize a cube and the display
cube = Cube()
display = RubiksCube3DDisplay(cube)

# Perform a series of moves on the cube
cube.run_turns("U B D' F2 D B' U' R2 D F2 D' R2 D F2 D' R2")

# Display the cube in 3D
display.draw()  # You can change angles for different views