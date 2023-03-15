from queue import Queue
from queue import PriorityQueue
import math
import random
import sys

from tkinter import messagebox, Tk
import pygame


from properties import Properties
from box import Box
from button import Button


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
        self._init_variables()
        self._create_grid()
        self.homescreen = True
        self.helpscreen = False
        self.start_custom = Button(self, 'start  custom')
        self.start_random = Button(self, 'start  random')
        self.help_button = Button(self, 'help')
        self.exit_button = Button(self, 'exit')

    def _init_variables(self):
        self.grid = []
        self.start_box = Box(self, -1, -1)
        self.target_box = Box(self, -1, -1)
        self.target_loc = []
        self.start_loc = []
        self.start_box_set = False
        self.target_box_set = False
        self.searching = False
        self.completed = False
        self.begin_search = {'dijk': False, 'astar': False}
        self.queue = Queue()
        self.path = []

    def _reset_algo_variables(self):
        self.queue = Queue()
        self.path = []
        for i in range(self.properties.columns):
            for j in range(self.properties.rows):
                self.grid[i][j].resetflags()
                self.grid[i][j].resetvalues()

    def _init_images(self):
        self.start_icon = pygame.image.load('images/home.png')
        self.start_icon = pygame.transform.scale(
            self.start_icon, (self.properties.box_width, self.properties.box_height))
        self.target_icon = pygame.image.load('images/target.png')
        self.target_icon = pygame.transform.scale(
            self.target_icon, (self.properties.box_width, self.properties.box_height))
        self.homescreen_img = pygame.image.load('images/landing.png')

    def _create_grid(self):
        for i in range(self.properties.columns):
            arr = []
            for j in range(self.properties.rows):
                arr.append(Box(self, i, j))
            self.grid.append(arr)

    def _set_neighbours(self):
        for i in range(self.properties.columns):
            for j in range(self.properties.rows):
                self.grid[i][j].set_neighbours()

    def run_app(self):

        while True:
            if self.homescreen:
                self._check_hover()
            self._checkevents()
            # changes here
            if self.begin_search:
                if self.begin_search['dijk']:
                    self._run_dijkstra()
                elif self.begin_search['astar']:
                    self._run_A_star()
            self._updatescreen()
            if self.homescreen and not self.helpscreen:
                self._click_action()

    def _click_action(self):

        if self.exit_button.selected:
            pygame.quit()
            sys.exit()

        elif self.help_button.selected:
            pygame.time.delay(1000)
            self.helpscreen = True
            self.help_button.selected = False

        elif self.start_custom.selected:
            self.homescreen = False
            self._reset_algo_variables()
            for i in range(self.properties.columns):
                for j in range(self.properties.rows):
                    self.grid[i][j].resetwall()
            self.start_custom.selected = False

        elif self.start_random.selected:
            self.homescreen = False
            self._reset_algo_variables()
            self._resetgrid(2)
            self._init_randomgrid()
            self.start_random.selected = False

    def _check_hover(self):
        self._hover_reset()
        if self.start_random.rect.collidepoint(pygame.mouse.get_pos()) and not self.start_random.selected:
            self.start_random.hover = True
        elif self.start_custom.rect.collidepoint(pygame.mouse.get_pos()) and not self.start_custom.selected:
            self.start_custom.hover = True
        elif self.help_button.rect.collidepoint(pygame.mouse.get_pos()) and not self.help_button.selected:
            self.help_button.hover = True
        elif self.exit_button.rect.collidepoint(pygame.mouse.get_pos()) and not self.exit_button.selected:
            self.exit_button.hover = True

    def _buttoncheck(self):
        if self.start_random.rect.collidepoint(pygame.mouse.get_pos()):
            self.start_random.selected = True
        elif self.start_custom.rect.collidepoint(pygame.mouse.get_pos()):
            self.start_custom.selected = True
        elif self.help_button.rect.collidepoint(pygame.mouse.get_pos()):
            self.help_button.selected = True
        elif self.exit_button.rect.collidepoint(pygame.mouse.get_pos()):
            self.exit_button.selected = True

    def _hover_reset(self):
        self.start_random.hover = False
        self.start_custom.hover = False
        self.help_button.hover = False
        self.exit_button.hover = False

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
                self.completed = True
                self.begin_search['astar'] = False
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
                self.begin_search['astar'] = False
                self._no_solution_prompt()

    def _no_solution_prompt(self):
        self.searching = False
        self.completed = True
        self._reset_algo_variables()
        Tk().wm_withdraw()
        messagebox.showinfo("No Solution", "There is no solution!")

    def _init_Dijkstra(self):
        self.searching = True
        self.prior = {}
        self._set_neighbours()
        self.queue.put(self.start_box)
        self.start_box.queued = True

    def _run_dijkstra(self):

        if self.queue.qsize() > 0 and self.searching:
            current_box = self.queue.get_nowait()
            current_box.visited = True
            if current_box == self.target_box:
                self.searching = False
                self.completed = True
                self.begin_search['dijk'] = False
                while current_box in self.prior:
                    current_box = self.prior[current_box]
                    self.path.append(current_box)

            else:
                for neighbour in current_box.neighbours:
                    if not neighbour.queued:
                        neighbour.queued = True
                        self.prior[neighbour] = current_box
                        self.queue.put_nowait(neighbour)
        else:
            if self.searching:
                self.begin_search['dijk'] = False
                self._no_solution_prompt()

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
                    if not self.homescreen:
                        self._mouse_event_createwall(mouse_x, mouse_y)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.completed:
                    self._reset_algo_variables()
                if self.homescreen:
                    self._buttoncheck()
                mouse_x = pygame.mouse.get_pos()[0]
                mouse_y = pygame.mouse.get_pos()[1]
                if not self.homescreen:
                    if pygame.mouse.get_pressed()[0]:
                        self._mouse_event_leftclick(mouse_x, mouse_y)
                    elif pygame.mouse.get_pressed()[2]:
                        self._mouse_event_rightclick(mouse_x, mouse_y)
            # start algorithm , changes here
            if event.type == pygame.KEYDOWN and not self.searching and not self.homescreen:
                if event.key == pygame.K_ESCAPE:
                    self.homescreen = True

            if event.type == pygame.KEYDOWN and self.target_box_set and self.start_box_set and not self.searching and not self.homescreen:
                # changes here

                if event.key == pygame.K_1:
                    self.begin_search['dijk'] = True
                    self.completed = False
                    self._reset_algo_variables()
                    self._init_Dijkstra()
                elif event.key == pygame.K_2:
                    self.begin_search['astar'] = True
                    self.completed = False
                    self._reset_algo_variables()
                    self._init_A_star()

    def _resetgrid(self, val):
        for i in range(self.properties.columns):
            for j in range(self.properties.rows):
                self.grid[i][j].resetwall

    def _init_randomgrid(self):
        for i in range(self.properties.columns):
            for j in range(self.properties.rows):
                self.grid[i][j].wall == False
                if self.grid[i][j].start == True:
                    continue
                elif self.grid[i][j].target == True:
                    continue
                else:
                    self.grid[i][j].wall = self._get_randomwall()

    def _get_randomwall(self):
        n = random.randint(1, 100)
        if n % 5 <= 2:
            n = random.randint(1, 2)
            if n == 1:
                return False
            if n == 2:
                return True
        else:
            return False

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
                self._select_start_box(index_i, index_j)

        elif self.grid[index_i][index_j].start:
            self._unselect_start_box(index_i, index_j)

        else:
            # draw wall, toggles the state
            if not self.grid[index_i][index_j].target:
                if not self.grid[index_i][index_j].start:
                    self.grid[index_i][index_j].reset()

    def _select_start_box(self, i, j):
        self.start_box = self.grid[i][j]
        self.grid[i][j].start = True
        self.start_loc.append(i)
        self.start_loc.append(j)
        self.start_box.start = True
        self.start_box_set = True

    def _unselect_start_box(self, i, j):
        self.start_box = None
        self.grid[i][j].reset()
        self.start_loc.pop()
        self.start_loc.pop()
        self.start_box_set = False

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
        if not self.homescreen:
            self.window.fill(self.properties.bg_color)
            self._drawGrid()
            if self.start_box_set:
                self._draw_starticon()
            if self.target_box_set:
                self._draw_targeticon()
        else:
            self._displayhomescreen()
            if not self.helpscreen:
                self._displayhomebuttons()
        pygame.display.flip()

    def _displayhomescreen(self):
        homescreenrect = self.homescreen_img.get_rect()
        homescreenrect.center = self.window.get_rect().center
        self.window.blit(self.homescreen_img, homescreenrect)

    def _displayhomebuttons(self):
        self.start_custom.draw_button()
        self.start_random.draw_button()
        self.help_button.draw_button()
        self.exit_button.draw_button()

    def _drawGrid(self):
        for i in range(self.properties.columns):
            for j in range(self.properties.rows):
                box = self.grid[i][j]
                box.draw(self.properties.box_color)
                if box.wall:
                    box.draw(self.properties.wallcolor)
                if box.queued:
                    box.draw(self.properties.queuedcolor)
                if box.visited:
                    box.draw(self.properties.visitedcolor)

                if box in self.path:
                    box.draw(self.properties.pathcolor)

    def _draw_starticon(self):
        if self.start_box_set:
            start_rect = self.start_icon.get_rect()
            start_rect.left = self.window.get_rect(
            ).left + self.start_loc[0] * self.properties.box_width
            start_rect.top = self.window.get_rect(
            ).top + self.start_loc[1] * self.properties.box_height
            self.window.blit(self.start_icon, start_rect)

    def _draw_targeticon(self):
        if self.target_box_set:
            target_rect = self.target_icon.get_rect()
            target_rect.left = self.window.get_rect(
            ).left + self.target_loc[0] * self.properties.box_width
            target_rect.top = self.window.get_rect(
            ).top + self.target_loc[1] * self.properties.box_height
            self.window.blit(self.target_icon, target_rect)


if __name__ == '__main__':
    visualizerapp = VisualizerApp()
    visualizerapp.run_app()
