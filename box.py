import pygame


class Box:
    def __init__(self, visualizer, i, j):
        self.x = i
        self.y = j
        self.properties = visualizer.properties
        self.width = self.properties.box_width
        self.height = self.properties.box_height
        self.color = self.properties.box_color
        self.window = visualizer.window
        self._initFlags()

    def _initFlags(self):
        self.start = False
        self.wall = False
        self.target = False

    def draw(self):
        if self.wall:
            self.color = (90, 90, 90)
        if self.x >= 0 and self.y >= 0:
            pygame.draw.rect(self.window, self.color, (self.x * self.width,
                                                       self.y * self.height, self.width - 1, self.height - 1))
