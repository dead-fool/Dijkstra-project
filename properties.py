class Properties:

    def __init__(self):
        self.window_width = 1200
        self.window_height = 600
        self.columns = self.window_width // 30
        self.rows = self.window_height // 30
        self.box_width = self.window_width // self.columns  # floor division
        self.box_height = self.window_height // self.rows
        self.bg_color = (138, 154, 91)
        self.box_color = (4, 57, 39)
        self.winningstroke_color = (0, 215, 0)
        self.boardinit = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
