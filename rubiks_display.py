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
        faces = [
            # name,      origin,         u_vec,         v_vec
            ('Front',  (0, 0, 3), (1, 0, 0), (0, 0, -1)),
            ('Back',   (3, 3, 3), (-1, 0, 0), (0, 0, -1)),
            ('Up',     (0, 3, 3), (1, 0, 0), (0, -1, 0)),
            ('Down',   (0, 0, 0), (1, 0, 0), (0, 1, 0)),
            ('Left',   (0, 3, 3), (0, -1, 0), (0, 0, -1)),
            ('Right',  (3, 0, 3), (0, 1, 0), (0, 0, -1)),
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