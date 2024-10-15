import math

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import RegularPolygon

def plot(x, y, x_label = 'x', y_label = 'y', title = '', path = None):
    plt.plot(x, y, 'o')
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.show()
    if path is not None:
        plt.savefig(path)


# Function to calculate hexagon vertices
def hex_grid(radius, board_data):
    fig, ax = plt.subplots()

    # Set aspect ratio to equal to keep the hexagons uniform
    ax.set_aspect('equal')

    board_width = int(math.sqrt(len(board_data)))

    count = 0
    # Loop through each hexagon in the grid
    for row in range(board_width):
        for col in range(board_width):
            # Calculate x, y position of the hexagon
            x = col * 1.5 * radius
            y = -(row * np.sqrt(3) * radius)

            # Offset every other column (staggered grid)
            if col % 2 == 1:
                y += np.sqrt(3) / 2 * radius

            print("x " + str(x))
            print("y " + str(y))
            print(str(count) + " : " + board_data[count])

            if board_data[count] == 'B':
                face_color = 'black'
            elif board_data[count] == 'W':
                face_color = 'white'
            else:
                face_color = 'grey'

            # Create a hexagon using RegularPolygon
            hexagon = RegularPolygon((x, y), numVertices=6, radius=radius,
                                     orientation=np.pi / 6, facecolor=face_color, edgecolor='black')

            # Add the hexagon to the plot
            ax.add_patch(hexagon)
            count += 1

    # Set limits and remove axes
    ax.set_xlim(-radius, (board_width * 1.5 * radius) + radius)  # x limits
    ax.set_ylim(-radius, (board_width * np.sqrt(3) * radius) + radius)  # y limits
    ax.axis('off')  # Turn off the axes

    plt.show()