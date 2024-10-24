import pygame
from view.constants import *
from view.playbackUI import PlaybackUI


class View:
    def __init__(self, width: int, height: int, rows: int, cols: int, world,
                 grid_size: float):
        self.world_width: int = width
        self.world_height: int = height
        self._rows: int = rows
        self._cols: int = cols
        self._world = world
        self._grid_size: float = grid_size

        pygame.init()
        self._screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(GAME_TITLE)

        # initialize window
        self._screen.fill(WINDOW_BG)
        self._render_title()

        self._playback_ui = PlaybackUI(self._screen)

        self._draw_world_border()

    def _draw_world_border(self):
        # Create world border
        pygame.draw.rect(self._screen, WORLD_BORDER_COLOR,
                         (WORLD_X - BORDER_WIDTH,
                          WORLD_Y - BORDER_WIDTH,
                          self._grid_size * self._cols + BORDER_WIDTH * 2,
                          self._grid_size * self._rows + BORDER_WIDTH * 2),
                         border_radius=5)

    def render_grid(self):
        # Draw the world background
        pygame.draw.rect(self._screen, WORLD_BG,
                         (WORLD_X, WORLD_Y,
                          WORLD_HEIGHT, WORLD_WIDTH))


        for row in range(self._rows):
            for col in range(self._cols):
                organism = self._world.get_cell(row, col)
                if organism:
                    self._draw_organism(organism, row, col)

    def _draw_organism(self, organism, row, col):
        color = organism.get_color()

        # Draw as a square
        rect = self._convert_cell_to_rect(row, col)
        pygame.draw.rect(self._screen, color, rect)


    def _convert_cell_to_rect(self, row, col):
        return (col * self._grid_size + WORLD_X,
                row * self._grid_size + WORLD_Y,
                self._grid_size, self._grid_size)

    @staticmethod
    def render_text(text, font, color, x_center, y_center, screen):
        surface = font.render(text, True, color)
        rect = surface.get_rect(center=(x_center, y_center))
        screen.blit(surface, rect)

    def _render_title(self):
        x_center = WORLD_X / 2
        y_center = 60
        font = pygame.font.SysFont(TITLE_FONT_NAME, TITLE_FONT_SIZE)
        self.render_text(GAME_TITLE, font, TITLE_TEXT,
                    x_center, y_center, self._screen)

    def handle_click(self):
        playback_action = self._playback_ui.handle_click_event()
        if playback_action:
            return playback_action
        return None

    def handle_mouse_move(self):
        if self._playback_ui.handle_hover_event():
            return

    def update_playback_state(self, playbackState):
        self._playback_ui.update_playback_state(playbackState)