import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def plot(x, y, x_label = 'x', y_label = 'y', title = '', path = None):
    plt.plot(x, y, 'o')
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.show()
    if path is not None:
        plt.savefig(path)
