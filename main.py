from tkinter import messagebox, Tk
import pygame
import math
import sys
from queue import Queue
from queue import PriorityQueue

from properties import Properties
from box import Box


class VisualizerApp:
    def __init__(self):
        self.properties = Properties()
        pygame.init()
        self.window = pygame.display.set_mode(
            (self.properties.window_width, self.properties.window_height))
        pygame.display.set_caption("VISUALIZER.ALGO")
        game_icon = pygame.image.load('images/gameicon.jpg')
        pygame.display.set_icon(game_icon)
        self._init_images()
        self.grid = []
        self._createGrid()
        self.start_box = Box(self, -1, -1)
        self.target_box = Box(self, -1, -1)
        self.target_loc = []
        self.start_loc = []
        self.start_box_set = False
        self.target_box_set = False
        self.searching = False
        self.begin_search = []
        self.queue = Queue()
        self.path = []

    def _init_images(self):
        self.start_icon = pygame.image.load('images/home.png')
        self.start_icon = pygame.transform.scale(
            self.start_icon, (self.properties.box_width, self.properties.box_height))
        self.target_icon = pygame.image.load('images/target.png')
        self.target_icon = pygame.transform.scale(
            self.target_icon, (self.properties.box_width, self.properties.box_height))

    def _createGrid(self):
        for i in range(self.properties.columns):
            arr = []
            for j in range(self.properties.rows):
                arr.append(Box(self, i, j))
            self.grid.append(arr)

    def _set_neighbours(self):
        for i in range(self.properties.columns):
            for j in range(self.properties.rows):
                self.grid[i][j].set_neighbours()

    def RunApp(self):

        while True:
            self._checkevents()
            # changes here
            if self.begin_search:
                if self.begin_search[0] == 1:
                    self._run_dijkstra()
                elif self.begin_search[0] == 2:
                    self._run_A_star()
            self._updatescreen()

    def _init_A_star(self):
        self.searching = True
        self._set_neighbours()
        self.count = 0
        self.priority_queue = PriorityQueue()
        self.priority_queue.put((0, self.count, self.start_box))
        self.prior = {}
        self.g_score = {Box: math.inf for row in self.grid for Box in row}
        self.g_score[self.start_box] = 0
        self.f_score = {Box: math.inf for row in self.grid for Box in row}
        self.f_score[self.start_box] = self.start_box.heuristic_func(
            self.target_box)

        self.open_set = {self.start_box}

    def _run_A_star(self):

        if not self.priority_queue.empty() and self.searching:
            current_box = self.priority_queue.get()[2]
            self.open_set.remove(current_box)
            if current_box == self.target_box:
                self.searching = False
                self.begin_search.pop()
                while current_box in self.prior:
                    current_box = self.prior[current_box]
                    self.path.append(current_box)

            for neighbor in current_box.neighbours:
                temp_g_score = self.g_score[current_box] + 1
                if temp_g_score < self.g_score[neighbor]:
                    self.prior[neighbor] = current_box
                    self.g_score[neighbor] = temp_g_score
                    self.f_score[neighbor] = temp_g_score + \
                        neighbor.heuristic_func(self.target_box)
                    if neighbor not in self.open_set:
                        self.count += 1
                        self.priority_queue.put(
                            (self.f_score[neighbor], self.count, neighbor))
                        self.open_set.add(neighbor)
                        if neighbor != self.target_box:
                            neighbor.queued = True
            if current_box != self.start_box:
                current_box.visited = True

        else:
            if self.searching:
                Tk().wm_withdraw()
                messagebox.showinfo("No Solution", "There is no solution!")
                self.searching = False

    def _init_Dijkstra(self):
        self.searching = True
        self._set_neighbours()
        self.queue.put(self.start_box)
        self.start_box.queued = True

    def _run_dijkstra(self):

        if self.queue.qsize() > 0 and self.searching:
            current_box = self.queue.get_nowait()
            current_box.visited = True
            if current_box == self.target_box:
                self.searching = False
                self.begin_search.pop()
                while current_box.prior != self.start_box:
                    self.path.append(current_box.prior)
                    current_box = current_box.prior

            else:
                for neighbour in current_box.neighbours:
                    if not neighbour.queued:
                        neighbour.queued = True
                        neighbour.prior = current_box
                        self.queue.put_nowait(neighbour)
        else:
            if self.searching:
                Tk().wm_withdraw()
                messagebox.showinfo("No Solution", "There is no solution!")
                self.searching = False

    def _checkevents(self):
        for event in pygame.event.get():
            # quit window
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # changes here
            if self.searching:
                continue
            # allows drag n draw
            elif event.type == pygame.MOUSEMOTION:
                mouse_x = pygame.mouse.get_pos()[0]
                mouse_y = pygame.mouse.get_pos()[1]
                if event.buttons[0]:
                    self._mouse_event_createwall(mouse_x, mouse_y)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x = pygame.mouse.get_pos()[0]
                mouse_y = pygame.mouse.get_pos()[1]
                if pygame.mouse.get_pressed()[0]:
                    self._mouse_event_leftclick(mouse_x, mouse_y)
                elif pygame.mouse.get_pressed()[2]:
                    self._mouse_event_rightclick(mouse_x, mouse_y)
            # start algorithm , changes here
            if event.type == pygame.KEYDOWN and self.target_box_set and self.start_box_set and not self.searching:
                # changes here
                if event.key == pygame.K_1:
                    self.begin_search.append(1)
                    self._init_Dijkstra()
                elif event.key == pygame.K_2:
                    self.begin_search.append(2)
                    self._init_A_star()

    def _mouse_event_createwall(self, x, y):
        index_i = x // self.properties.box_width
        index_j = y // self.properties.box_height
        if self.start_box_set:
            if not self.grid[index_i][index_j].target:
                if not self.grid[index_i][index_j].start:
                    if not self.grid[index_i][index_j].wall:
                        self.grid[index_i][index_j].wall = True

    def _mouse_event_leftclick(self, x, y):
        index_i = x // self.properties.box_width
        index_j = y // self.properties.box_height
        if not self.start_box_set:
            # draw start , changes here
            if self.grid[index_i][index_j].wall == False and self.grid[index_i][index_j].target == False:
                self.start_box = self.grid[index_i][index_j]
                self.grid[index_i][index_j].start = True
                self.start_loc.append(index_i)
                self.start_loc.append(index_j)
                self.start_box.start = True
                self.start_box_set = True

        elif self.grid[index_i][index_j].start:
            self.start_box = None
            self.grid[index_i][index_j].reset()
            self.start_loc.pop()
            self.start_loc.pop()
            self.start_box_set = False

        else:
            # draw wall, toggles the state
            if not self.grid[index_i][index_j].target:
                if not self.grid[index_i][index_j].start:
                    self.grid[index_i][index_j].reset()

    def _mouse_event_rightclick(self, x, y):
        index_i = x // self.properties.box_width
        index_j = y // self.properties.box_height
        if not self.target_box_set:
            # changes here
            if self.grid[index_i][index_j].wall == False and self.grid[index_i][index_j].start == False:
                self.target_box = self.grid[index_i][index_j]
                self.grid[index_i][index_j].target = True
                self.target_loc.append(index_i)
                self.target_loc.append(index_j)
                self.target_box.target = True
                self.target_box_set = True
        elif self.grid[index_i][index_j].target:
            self.target_box = None
            self.grid[index_i][index_j].reset()
            self.target_loc.pop()
            self.target_loc.pop()
            self.target_box_set = False

    def _updatescreen(self):
        self.window.fill(self.properties.bg_color)
        self._drawGrid()
        if self.start_box_set:
            self._draw_starticon()
        if self.target_box_set:
            self._draw_targeticon()
        pygame.display.flip()

    def _drawGrid(self):
        for i in range(self.properties.columns):
            for j in range(self.properties.rows):
                box = self.grid[i][j]
                box.draw(self.properties.box_color)
                if box.wall:
                    box.draw((255, 255, 255))
                if box.queued:
                    box.draw((255, 79, 88))
                if box.visited:
                    box.draw((255, 138, 138))

                if box in self.path:
                    box.draw((12, 4, 4))

    def _draw_starticon(self):
        if self.start_loc:
            start_rect = self.start_icon.get_rect()
            start_rect.left = self.window.get_rect(
            ).left + self.start_loc[0] * self.properties.box_width
            start_rect.top = self.window.get_rect(
            ).top + self.start_loc[1] * self.properties.box_height
            self.window.blit(self.start_icon, start_rect)

    def _draw_targeticon(self):
        if self.target_loc:
            target_rect = self.target_icon.get_rect()
            target_rect.left = self.window.get_rect(
            ).left + self.target_loc[0] * self.properties.box_width
            target_rect.top = self.window.get_rect(
            ).top + self.target_loc[1] * self.properties.box_height
            self.window.blit(self.target_icon, target_rect)


if __name__ == '__main__':
    visualizerapp = VisualizerApp()
    visualizerapp.RunApp()
