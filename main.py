import numpy as np
from automata import conways_game
from automata import smooth_life
from visualizer.conway_visualizer import ConwayVisualizer
from visualizer.smooth_life_visualizer import SmoothLifeVisualizer

def run_conways_game():
    SIZE = (50, 100)
    INTERVAL = 50
    grid = conways_game.Grid(SIZE)

    middle = (SIZE[0]//2, SIZE[1]//2)
    for i in range(1, SIZE[1], 5):
        grid.set_pattern(conways_game.Species.Spaceship.glider, position=(0, i))
    for i in range(1, SIZE[1], 5):
        grid.set_pattern(np.rot90(conways_game.Species.Spaceship.glider), position=(SIZE[0]-4, i))
    grid.set_pattern(conways_game.Species.Oscillator.blinker, position=(middle[0], middle[1]))

    visualizer = ConwayVisualizer(grid, interval=INTERVAL)
    visualizer.run()

def run_smooth_life():
    SIZE = (50, 100)
    INTERVAL = 50
    
    grid = smooth_life.Grid(SIZE)
    # puts a 10x10 square of random values in the middle of the grid
    grid.set_pattern(np.random.rand(30, 30), position=(10, 10))

    visualizer = SmoothLifeVisualizer(grid, interval=INTERVAL)
    visualizer.run()

if __name__ == "__main__":
    #run_conways_game()
    run_smooth_life()
