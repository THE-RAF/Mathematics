import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm


# Create a set of line segments so that we can color them individually
# This creates the points as a N x 1 x 2 array so that we can stack points
# together easily to get the segments. The segments array for line collection
# needs to be (numlines) x (points per line) x 2 (for x and y)

def colorline(x, y, ax, cmap, fade=0.1, linewidth=1):
    line_gradient_array = np.arange(0, len(x))
    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)

    # Create a continuous norm to map from data points to colors
    norm = plt.Normalize(line_gradient_array.min(), fade*line_gradient_array.max())
    lc = LineCollection(segments, cmap=cmap, norm=norm)

    # Set the values used for colormapping
    lc.set_array(line_gradient_array)
    lc.set_linewidth(linewidth)
    line = ax.add_collection(lc)
    plt.autoscale()
