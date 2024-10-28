import pygame.draw

from view.constants import SLIDER_WIDTH, SLIDER_HEIGHT, SLIDER_TRACK, \
    SLIDER_CIRCLE, SLIDER_RADIUS, WINDOW_BG, FONT_NAME, \
    STATS_FONT_SIZE, STATS_COLOR
from view.text import render_text


class Slider:
    """
    Horizontal slider that displays a title on the left and the value on the
    right.
    """
    def __init__(self, x: float, y: float, screen,
                 min_val: int, max_val: int, default_val: int,
                 title: str):
        # draw the title, use the width place slider track
        font = pygame.font.SysFont(FONT_NAME, STATS_FONT_SIZE)
        title_width = render_text(title, font, STATS_COLOR, x, y - 10, screen,
                                  False)
        self._x: float = x + title_width + 15
        self._y: float = y
        self._screen = screen

        # start using default val.
        # need to get relative position using min,max,width and x
        self._slider_position: float = (self._x +
                                        ((default_val - min_val) /
                                         (max_val - min_val)) * SLIDER_WIDTH)
        self._is_sliding: bool = False
        self._min_val: int = min_val
        self._max_val: int = max_val
        self._val: int = default_val

        self.draw()

    def draw(self):
        """Draws the slider track, circle, and value"""
        # slider track
        slider_rect = (self._x, self._y, SLIDER_WIDTH, SLIDER_HEIGHT)
        pygame.draw.rect(self._screen, SLIDER_TRACK, slider_rect,
                         border_radius=15)

        # slider circle
        circle_center = (self._slider_position, self._y + SLIDER_HEIGHT // 2)
        pygame.draw.circle(self._screen, SLIDER_CIRCLE, circle_center,
                           SLIDER_RADIUS)

        self._draw_val()

    def _draw_val(self):
        """Draws or updates the slider's value"""
        val_x = self._x + SLIDER_WIDTH + 30
        # Erase old val
        pygame.draw.rect(self._screen, WINDOW_BG,
                         (val_x - 20,
                          self._y - 10, 40, 20))

        font = pygame.font.SysFont(FONT_NAME, STATS_FONT_SIZE)
        render_text(str(self._val), font, STATS_COLOR, val_x, self._y,
                    self._screen)

    def _remove_circle(self):
        """Removes the slider circle to prepare for updating the screen"""
        #  remove old slider circle
        circle_center = (self._slider_position, self._y + SLIDER_HEIGHT // 2)
        pygame.draw.circle(self._screen, WINDOW_BG, circle_center,
                           SLIDER_RADIUS)

    def get_val(self) -> int:
        """Gets the integer value based on the slider's position"""
        # converts the x position into a value using min/max and width
        relative_position = (self._slider_position - self._x) / SLIDER_WIDTH
        return int(self._min_val + relative_position * (
                    self._max_val - self._min_val))

    def handle_click_event(self) -> bool:
        """Checks if the slider circle is clicked"""
        left = self._slider_position - SLIDER_RADIUS
        right = self._slider_position + SLIDER_RADIUS
        top = self._y - SLIDER_RADIUS
        bottom = self._y + SLIDER_RADIUS
        pos_x, pos_y = pygame.mouse.get_pos()

        if (left <= pos_x <= right and
                top <= pos_y <= bottom):
            self._is_sliding = True
            return True
        return False

    def handle_mouse_move(self) -> (bool, int):
        """Updates the slider position and val if the user clicks and drags"""
        if self._is_sliding:
            self._remove_circle()    # remove old circle to prepare redraw
            # get the new mouse pos, but make sure it stays within bounds
            pos_x, pos_y = pygame.mouse.get_pos()
            if pos_x < self._x:
                self._slider_position = self._x
            elif pos_x > self._x + SLIDER_WIDTH:
                self._slider_position = self._x + SLIDER_WIDTH
            else:
                self._slider_position = pos_x
            self._val = self.get_val()  # convert the new position to the val
            self.draw() # redraw slider circle in new position and new val
            return True, self._val
        return False, -1

    def handle_mouse_up(self) -> bool:
        """Checks if the user releases click from the slider circle"""
        if self._is_sliding:
            self._is_sliding = False
            return True
        return False