import matplotlib.pyplot as plt
import matplotlib.animation as animation

class SmoothLifeVisualizer:
    def __init__(self, grid, interval=200):
        self.grid = grid
        self.interval = interval
        self.fig, self.ax = plt.subplots()
        self.iteration = 0

    def animate(self, i):
        self.ax.clear()
        self.ax.imshow(self.grid.grid, cmap='gray')
        self.ax.set_title(f"Iteration {self.iteration}")
        self.ax.axis('off')
        self.grid.update_grid()
        self.iteration += 1

    def run(self):
        ani = animation.FuncAnimation(self.fig, self.animate, interval=self.interval)
        plt.show()
