import pygame


class Box:
    def __init__(self, visualizer, i, j):
        self.x = i
        self.y = j
        self.grid = visualizer.grid
        self.properties = visualizer.properties
        self.width = self.properties.box_width
        self.height = self.properties.box_height
        self.color = self.properties.box_color
        self.window = visualizer.window
        self._initFlags()
        self.neighbours = []
        self.prior = None

    def _initFlags(self):
        self.start = False
        self.wall = False
        self.target = False
        self.queued = False
        self.visited = False

    def set_neighbours(self):
        if self.x > 0:
            self.neighbours.append(self.grid[self.x - 1][self.y])
        if self.x < self.properties.columns - 1:
            self.neighbours.append(self.grid[self.x + 1][self.y])
        if self.y > 0:
            self.neighbours.append(self.grid[self.x][self.y - 1])
        if self.y < self.properties.rows - 1:
            self.neighbours.append(self.grid[self.x][self.y + 1])

    def draw(self, color):
        if self.x >= 0 and self.y >= 0:
            pygame.draw.rect(self.window, color, (self.x * self.width,
                                                  self.y * self.height, self.width - 1, self.height - 1))
