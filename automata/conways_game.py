import numpy as np

class Grid:
    def __init__(self, size):
        """
        Initialize the grid.
        """
        
        self.size = size
        self.grid = np.zeros(self.size, dtype=int)

    def set_pattern(self, pattern, position=(0, 0)):
        """
        Set a specific pattern on the grid.
        """
        
        x, y = position
        sx, sy = pattern.shape
        self.grid[x:x+sx, y:y+sy] = pattern

    def count_live_neighbors(self, x, y):
        """
        Count the number of live neighbors for a cell at position (x, y).

        Args:
            x (int): Row position of the cell.
            y (int): Column position of the cell.

        Returns:
            int: Number of live neighbors.
        """
        
        count = 0

        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                # Skip the cell itself
                if i == 0 and j == 0:
                    continue
                
                # Compute neighbor position with wrap-around
                neighbor_x = (x + i) % self.size[0]
                neighbor_y = (y + j) % self.size[1]

                count += self.grid[neighbor_x, neighbor_y]

        return count

    def update(self):
        """
        Update the grid based on Conway's Game of Life rules.
        """
        new_grid = np.zeros_like(self.grid)
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                live_neighbors = self.count_live_neighbors(x, y)
                cell = self.grid[x, y]

                if cell == 1 and (live_neighbors == 2 or live_neighbors == 3):
                    # Live cell with 2 or 3 neighbors stays alive
                    new_grid[x, y] = 1
                elif cell == 0 and live_neighbors == 3:
                    # Dead cell with exactly 3 neighbors becomes alive
                    new_grid[x, y] = 1
                # All other cells remain dead or become dead

        self.grid = new_grid

class Species:
    class StillLife:
        block = np.array([[1, 1],
                          [1, 1]])
        beehive = np.array([[0, 1, 1, 0],
                            [1, 0, 0, 1],
                            [0, 1, 1, 0]])

    class Oscillator:
        blinker = np.array([[1, 1, 1]])
        toad = np.array([[0, 1, 1, 1],
                         [1, 1, 1, 0]])
        beacon = np.array([[1, 1, 0, 0],
                           [1, 1, 0, 0],
                           [0, 0, 1, 1],
                           [0, 0, 1, 1]])

    class Spaceship:
        glider = np.array([[0, 1, 0],
                           [0, 0, 1],
                           [1, 1, 1]])
        lightweight_spaceship = np.array([[0, 1, 0, 0, 1],
                                          [1, 0, 0, 0, 0],
                                          [1, 0, 0, 0, 1],
                                          [1, 1, 1, 1, 0]])


