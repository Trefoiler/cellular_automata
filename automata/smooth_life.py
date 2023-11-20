import numpy as np


class Kernel:
    '''
    A class representing a kernel to check cells around a center cell.
    '''
    
    def __init__(self, kernel: np.ndarray) -> None:
        self.kernel: np.ndarray = kernel
        self.rows: int = kernel.shape[0]
        self.cols: int = kernel.shape[1]
        self.centerCell: tuple = (self.rows//2, self.cols//2)
        
        self.kernel_positions: np.ndarray = np.zeros((self.rows, self.cols), dtype=tuple)
        for row in range(self.rows):
            for col in range(self.cols):
                self.kernel_positions[row, col] = (row - self.rows//2,
                                                   col - self.cols//2)
        
        # Check if the kernel is a square
        if self.rows != self.cols:
            raise ValueError("Kernel must be a square")
        
        # Check if the kernel has odd dimensions
        if self.rows % 2 == 0:
            raise ValueError("Kernel must have odd dimensions")
        
        # Check if the center cell is 0
        if self.kernel[self.centerCell] != 0:
            raise ValueError("Center cell must be 0")


class Grid:
    """
    A class representing a grid of cells.
    Each cell will be between 0.0 and 1.0.
    """
    
    _default_kernel_3: Kernel = Kernel(np.array([[1, 1, 1],
                                               [1, 0, 1],
                                               [1, 1, 1]]))
    _default_kernel_5: Kernel = Kernel(np.array([[1, 1, 1, 1, 1],
                                                 [1, 1, 1, 1, 1],
                                                 [1, 1, 0, 1, 1],
                                                 [1, 1, 1, 1, 1],
                                                 [1, 1, 1, 1, 1]]))
    _default_kernel_circle_r2: Kernel = Kernel(np.array([[0, 1, 1, 1, 0],
                                                         [1, 1, 1, 1, 1],
                                                         [1, 1, 0, 1, 1],
                                                         [1, 1, 1, 1, 1],
                                                         [0, 1, 1, 1, 0]]))
    _default_kernel_circle_r3: Kernel = Kernel(np.array([[0, 0, 0, 1, 0, 0, 0],
                                                         [0, 1, 1, 1, 1, 1, 0],
                                                         [0, 1, 0, 0, 0, 1, 0],
                                                         [1, 1, 0, 0, 0, 1, 1],
                                                         [0, 1, 0, 0, 0, 1, 0],
                                                         [0, 1, 1, 1, 1, 1, 0],
                                                         [0, 0, 0, 1, 0, 0, 0]]))
    
    
    def __init__(self, size: tuple, kernel: Kernel = _default_kernel_circle_r3) -> None:
        """
        Initialize the grid.
        """
        
        self.size: tuple = size
        self.grid: np.ndarray = np.zeros(self.size, dtype=float);
        self.kernel: Kernel = kernel
    
    
    def set_cell_to(self, cell_pos: tuple, value: float) -> None:
        """
        Sets the value of a cell.
        """
        
        self.grid[cell_pos] = value
    
    
    def set_pattern(self, pattern: np.ndarray, position: tuple) -> None:
        """
        Sets a pattern of cells.
        """
        
        self.grid[position[0]:position[0]+pattern.shape[0],
                  position[1]:position[1]+pattern.shape[1]] = pattern
    
    
    def get_neighbors(self, cell_pos: tuple) -> list:
        """
        Returns a list of the values of the neighbors of a cell.
        """
        
        neighbors: list = []
        
        for row in range(self.kernel.rows):
            for col in range(self.kernel.cols):
                # Runs for every cell in the kernel
                
                # If the cell should be checked...
                if self.kernel.kernel[row, col] == 1:
                    # Compute neighbor position with wrap-around
                    neighbor_x = (cell_pos[0] + self.kernel.kernel_positions[row, col][0]) % self.size[0]
                    neighbor_y = (cell_pos[1] + self.kernel.kernel_positions[row, col][1]) % self.size[1]
                    
                    neighbors.append(self.grid[neighbor_x, neighbor_y])
        
        return neighbors
    
    
    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))
    
    
    def cell_transition_function(self, cell_val: float, neighbor_mean: float) -> float:
        """
        Returns the value of a cell after a transition.
        """
        
        # Parameters for the sigmoid function
        alpha = 10  # Controls the steepness of the sigmoid
        beta_birth = 0.4  # Midpoint of the sigmoid for birth
        beta_survive = 0.55  # Midpoint of the sigmoid for survival

        # Birth and survival thresholds
        birth_threshold = self.sigmoid(alpha * (neighbor_mean - beta_birth))
        survival_threshold = self.sigmoid(alpha * (neighbor_mean - beta_survive))

        if cell_val < 0.5:
            # Cell is more 'dead' than 'alive'
            return birth_threshold
        else:
            # Cell is more 'alive' than 'dead'
            return survival_threshold
        
    
    
    def update_grid(self) -> None:
        """
        Updates the grid by setting each cell to be an average of it's neighbors.
        """
        
        new_grid: np.ndarray = np.zeros_like(self.grid)
        
        for row in range(self.size[0]):
            for col in range(self.size[1]):
                neighbors: list = self.get_neighbors((row, col))
                neighbors_mean = np.mean(neighbors)
                this_cell_val = self.grid[row, col]
                new_grid[row, col] = self.cell_transition_function(this_cell_val, neighbors_mean)
        
        self.grid = new_grid




if __name__ == "__main__":
    kernel_3: np.ndarray = np.array([[1, 1, 1],
                             [1, 0, 1],
                             [1, 1, 1]])
    kernel_5: np.ndarray = np.array([[1, 1, 1, 1, 1],
                                    [1, 1, 1, 1, 1],
                                    [1, 1, 0, 1, 1],
                                    [1, 1, 1, 1, 1],
                                    [1, 1, 1, 1, 1]])
    k3 = Kernel(kernel_3)
    k5 = Kernel(kernel_5)
    
    # Setup grid
    grid = Grid((10, 10), k3)
    grid.grid[4, 4] = 1
    
    print(grid.get_neighbors((5, 4)))
    