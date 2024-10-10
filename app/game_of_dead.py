import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class GameOfDead:
    def __init__(self, size=100):
        self.size = size
        self.grid = np.random.choice([0, 1, 2], size*size, p=[0.8, 0.15, 0.05]).reshape(size, size)
        # 0: Leer, 1: Lebend, 2: Zombie

    def count_neighbors(self, i, j):
        neighbors = self.grid[(i-1)%self.size:(i+2)%self.size, 
                              (j-1)%self.size:(j+2)%self.size]
        return [(neighbors == 1).sum() - (self.grid[i, j] == 1),
                (neighbors == 2).sum() - (self.grid[i, j] == 2)]

    def update(self):
        new_grid = self.grid.copy()
        for i in range(self.size):
            for j in range(self.size):
                live_neighbors, zombie_neighbors = self.count_neighbors(i, j)
                
                if self.grid[i, j] == 0:  # Leere Zelle
                    if live_neighbors == 3:
                        new_grid[i, j] = 1
                    elif zombie_neighbors >= 3:
                        new_grid[i, j] = 2
                elif self.grid[i, j] == 1:  # Lebende Zelle
                    if live_neighbors < 2 or live_neighbors > 3:
                        new_grid[i, j] = 0
                    elif zombie_neighbors >= 2:
                        new_grid[i, j] = 2
                else:  # Zombie Zelle
                    if live_neighbors >= 2:  # Neue Regel: Zombie wird gelöscht bei 2+ lebenden Nachbarn
                        new_grid[i, j] = 0
                    elif zombie_neighbors < 2 or zombie_neighbors > 3:
                        new_grid[i, j] = 0
        
        self.grid = new_grid

    def animate(self, frame):
        self.update()
        self.img.set_array(self.grid)
        return self.img,

    def run(self):
        fig, ax = plt.subplots()
        self.img = ax.imshow(self.grid, interpolation='nearest', cmap='viridis')
        ani = FuncAnimation(fig, self.animate, frames=200, interval=100, blit=True)
        plt.show()

if __name__ == "__main__":
    game = GameOfDead()
    game.run()