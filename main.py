from cube import Cube
from rubiks_display import RubiksCube3DDisplay

cube = Cube()
cube.run_turns("F L F U' R U F2 L2 U' L' B D' B' L2 U")
display = RubiksCube3DDisplay(cube)
display.draw(elev=15, azim=-45)  # You can change angles for different views