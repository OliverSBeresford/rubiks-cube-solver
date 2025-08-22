import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np

# Map sticker letters to matplotlib colors
STICKER_COLORS = {
    'W': 'white',
    'Y': 'yellow',
    'R': 'red',
    'O': 'orange',
    'G': 'green',
    'B': 'blue'
}

class RubiksCube3DDisplay:
    def __init__(self, cube):
        """
        Args:
            cube (Cube): An instance of the Cube class.
        """
        self.cube = cube

    def draw(self, elev=30, azim=30):
        """
        Draws the cube in 3D using matplotlib.

        Args:
            elev (float): Elevation angle in the z plane.
            azim (float): Azimuth angle in the x,y plane.
        """
        fig = plt.figure(figsize=(7, 7))
        ax = fig.add_subplot(111, projection='3d')
        ax.set_box_aspect([1,1,1])

        # Hide axes
        ax.set_axis_off()

        # Each face: (name, origin, u vector, v vector)
        # All faces are defined so that (i, j) runs over the 3x3 grid in the correct orientation
        faces = [
            # name,      origin,         u_vec,         v_vec
            ('Front',  (0, 0, 3), (1, 0, 0), (0, 0, -1)),  # z=2
            ('Back',   (3, 3, 3), (-1, 0, 0), (0, 0, -1)), # z=0, mirrored x
            ('Up',     (0, 3, 3), (1, 0, 0), (0, -1, 0)), # y=2, z decreases
            ('Down',   (0, 0, 0), (1, 0, 0), (0, 1, 0)),  # y=0, z increases
            ('Left',   (0, 3, 3), (0, -1, 0), (0, 0, -1)),  # x=0
            ('Right',  (3, 0, 3), (0, 1, 0), (0, 0, -1)), # x=2, z decreases
        ]

        for face_name, origin, u_vec, v_vec in faces:
            face = getattr(self.cube, face_name)
            for i in range(3):
                for j in range(3):
                    # Calculate the 4 corners of the sticker (rectangle)
                    corners = []
                    for du, dv in [(0,0), (1,0), (1,1), (0,1)]:
                        x = origin[0] + u_vec[0]*(i+du) + v_vec[0]*(j+dv)
                        y = origin[1] + u_vec[1]*(i+du) + v_vec[1]*(j+dv)
                        z = origin[2] + u_vec[2]*(i+du) + v_vec[2]*(j+dv)
                        corners.append([x, y, z])
                    color = STICKER_COLORS.get(face[i, j], 'gray')
                    poly = Poly3DCollection([corners])
                    poly.set_facecolor(color)
                    poly.set_edgecolor('black')
                    ax.add_collection3d(poly)

        ax.set_xlim([0, 3])
        ax.set_ylim([0, 3])
        ax.set_zlim([0, 3])
        ax.view_init(elev=elev, azim=azim)
        plt.show()