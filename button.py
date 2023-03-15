import pygame.font


class Button():

    def __init__(self, visualizer, buttontype):
        """Initialize button attributes."""

        self.screen = visualizer.window
        self.screen_rect = self.screen.get_rect()
        # Set the dimensions and properties of the button
        self.width, self.height = 250, 50
        self.button_color = (246, 224, 181)
        self.border_color = None
        self.text_color = (102, 84, 94)
        self.hover = False
        self.selected = False
        self.font = pygame.font.SysFont(None, 32)
        # Build the button's rect object and center it
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.centerx = self.screen_rect.centerx
        if buttontype == 'start  custom':
            self.rect.centery = self.screen_rect.centery - 75
        elif buttontype == 'start  random':
            self.rect.centery = self.screen_rect.centery
        elif buttontype == 'help':
            self.rect.centery = self.screen_rect.centery + 75
        elif buttontype == 'exit':
            self.rect.centery = self.screen_rect.centery + 150
        # The button message needs to be prepped only once
        self.msg = buttontype.upper()
        self.prep_msg(buttontype)

    def prep_msg(self, buttontype):
        """ Turn msg into a rendered image and center text on the button. """
        self.msg_image = self.font.render(self.msg, True, self.text_color,
                                          self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # Draw blank button and then draw message
        self._set_color()
        self.screen.fill(self.button_color, self.rect)
        pygame.draw.rect(self.screen, self.border_color, self.rect, 4)
        self.screen.blit(self.msg_image, self.msg_image_rect)

    def _set_color(self):
        if self.hover:
            self.border_color = (255, 105, 105)
        elif self.selected:
            self.border_color = (20, 170, 35)
        else:
            self.border_color = (0, 0, 0)
