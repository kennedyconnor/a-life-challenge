import pygame

from view.components.button import Button
from view.constants import WINDOW_BG, WINDOW_HEIGHT, WINDOW_WIDTH, \
    VIEW_GENOMES_X, VIEW_GENOMES_Y, VIEW_GENOMES_HEIGHT, VIEW_GENOMES_WIDTH, \
    LIGHT_GREY_2, BUTTON_WIDTH, EXIT_ICON_HOVER, \
    EXIT_ICON, TITLE_FONT_NAME, BUTTON_HEIGHT, VIEW_GENOMES_TITLE, \
    VIEW_GENOMES_FONT_SIZE, TITLE_TEXT, PREV_ICON, PREV_ICON_HOVER, NEXT_ICON, \
    NEXT_ICON_HOVER, BUTTON_GAP
from view.sections.buttonBarUI import ButtonBarUI
from view.sections.uiComponent import UiComponent
from view.text import render_text, render_text_pair


class ViewGenomeUI(UiComponent):
    """Displays a new view in the Pygame window for view genomes"""
    def __init__(self, screen, exit_fn, world):
        super().__init__()
        self._screen = screen
        self._exit_fn = exit_fn
        self._world = world
        self._genome_num: int = 0

        exit_button_padding: int= 20
        exit_button_x: int = (VIEW_GENOMES_X + VIEW_GENOMES_WIDTH -
                         BUTTON_WIDTH - exit_button_padding)
        exit_button_y: int = VIEW_GENOMES_Y + exit_button_padding

        self._exit_button: Button = Button(exit_button_x, exit_button_y,
                                           EXIT_ICON, EXIT_ICON_HOVER,
                                           self._screen, exit_fn)

        self._genome_data_height: int = 0


    def draw(self):
        self._genome_num = 0
        self._draw_background()
        self._draw_title()
        self._draw_genome_data()

        def next_fn():
            # use hardcoded data for now
            self._genome_num = (self._genome_num + 1) % 3
            # self._genome_num = self._genome_num + 1 % len(self._world.get_genome_data())
            self._draw_genome_data()
        def prev_fn():
            # use hardcoded data for now
            self._genome_num = (self._genome_num - 1) % 3
            # self._genome_num = self._genome_num - 1 % len(self._world.get_genome_data())
            self._draw_genome_data()

        arrows = ButtonBarUI(self._screen, (WINDOW_WIDTH / 2) - (BUTTON_WIDTH + BUTTON_GAP / 2),
                    VIEW_GENOMES_Y + 100,
                    (PREV_ICON, PREV_ICON_HOVER, prev_fn),
                    (NEXT_ICON, NEXT_ICON_HOVER, next_fn))
        self._buttons = arrows._buttons + [self._exit_button]
        for button in self._buttons:
            button.draw()



    def _draw_background(self):
        # Cover the entire background
        background_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT),
                                            pygame.SRCALPHA)
        alpha_value = 200
        background_surface.fill((*LIGHT_GREY_2, alpha_value))
        self._screen.blit(background_surface, (0, 0))

        # Draw "modal" window
        modal_rect = (VIEW_GENOMES_X, VIEW_GENOMES_Y,
                      VIEW_GENOMES_WIDTH, VIEW_GENOMES_HEIGHT)
        pygame.draw.rect(self._screen, WINDOW_BG, modal_rect)

    def _draw_title(self):
        x_center = WINDOW_WIDTH / 2
        y_center = VIEW_GENOMES_Y + BUTTON_HEIGHT
        font = pygame.font.SysFont(TITLE_FONT_NAME, VIEW_GENOMES_FONT_SIZE)
        render_text(VIEW_GENOMES_TITLE, font, TITLE_TEXT,
                    x_center, y_center, self._screen)

    def _draw_genome_data(self):
        # use hardcoded data for now
        # genome_data = self._world.get_genome_data()
        genome_data = [
            {"Color": (255, 0, 0),
             "Creature Type": "Carnivore",
             "Max Energy": 500,
             "Can Move": "True",
             "Status": "Active",
             "Population": 100,
             "Max Population": 390,
             "Day Created": 0,
             "Days Active": 360
             },
            {"Color": (0, 0, 255),
             "Creature Type": "Herbivore",
             "Max Energy": 500,
             "Can Move": "True",
             "Status": "Active",
             "Population": 400,
             "Max Population": 600,
             "Day Created": 0,
             "Days Active": 360
             },
            {"Color": (0, 255, 0),
             "Creature Type": "Passive",
             "Max Energy": 500,
             "Can Move": "False",
             "Status": "Active",
             "Population": 800,
             "Max Population": 1000,
             "Day Created": 0,
             "Days Active": 360
             }
        ]
        y = VIEW_GENOMES_Y + 200

        # remove old data
        pygame.draw.rect(self._screen, WINDOW_BG,
                         (VIEW_GENOMES_X, y, 450, self._genome_data_height))

        # draw new data
        for key, value in genome_data[self._genome_num].items():
            if key == "Color":
                continue
            y += render_text_pair(key, value, y, self._screen, VIEW_GENOMES_X + 100)

        self._genome_data_height = y - (VIEW_GENOMES_Y + 200)

        self._draw_genome_organism(genome_data[self._genome_num])

    def _draw_genome_organism(self, data):
        color = data["Color"]
        organism_width = 200
        rect = (VIEW_GENOMES_X + (VIEW_GENOMES_WIDTH / 2) + (organism_width / 2),
                VIEW_GENOMES_Y + 200,
                organism_width, organism_width)
        pygame.draw.rect(self._screen, color, rect)

    def handle_click_event(self) -> bool:
        # button should not be hovered, next time it is viewed
        self._exit_button.reset()
        return super().handle_click_event()