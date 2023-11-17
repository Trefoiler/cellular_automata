import numpy as np
from automata.conways_game import Grid, Species
from visualizer.conway_visualizer import ConwayVisualizer

def main():
    SIZE = (50, 100)
    INTERVAL = 50
    grid = Grid(SIZE)

    middle = (SIZE[0]//2, SIZE[1]//2)
    for i in range(1, SIZE[1], 5):
        grid.set_pattern(Species.Spaceship.glider, position=(0, i))
    for i in range(1, SIZE[1], 5):
        grid.set_pattern(np.rot90(Species.Spaceship.glider), position=(SIZE[0]-4, i))
    grid.set_pattern(Species.Oscillator.blinker, position=(middle[0], middle[1]))

    visualizer = ConwayVisualizer(grid, interval=INTERVAL)
    visualizer.run()

if __name__ == "__main__":
    main()
