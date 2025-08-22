from cube import Cube
from rubiks_display import RubiksCube3DDisplay

cube = Cube()
display = RubiksCube3DDisplay(cube)
display.draw(elev=15, azim=-45)  # You can change angles for different views