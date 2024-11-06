import random
import pygame
import pickle

import events
from models import CreatureType, Genome, PassiveOrganism, HerbivoreOrganism, CarnivoreOrganism
from view.constants import ButtonEvent
from view.view import View
from world import World

ROWS, COLS = World.ROWS, World.COLS

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

PLAY, PAUSE, STEP = 0, 1, 2
state = PAUSE
running = True
dt = 0

def create_genome(creature_type, world) -> Genome:
    if creature_type == CreatureType.PASSIVE:
        return Genome(GREEN, creature_type, world.get_world_max_passive_energy(), False)
    if creature_type == CreatureType.CARNIVORE:
        return Genome(RED, creature_type, world.get_world_max_carnivore_energy(), True)
    return Genome(BLUE, creature_type, world.get_world_max_herbivore_energy(), True)


def setup_life(world):
    for row in range(ROWS):
        for col in range(COLS):
            val = random.randint(0, 20)
            # 0-5 passive, 5-7 herbivore, 8 carnivore
            if val < 6:
                world.add_organism(PassiveOrganism(create_genome(CreatureType.PASSIVE, world), row, col, world), row, col)
            elif 6< val < 8:
                world.add_organism(HerbivoreOrganism(create_genome(CreatureType.HERBIVORE, world), row, col, world), row, col)
            elif val == 8:
                 world.add_organism(CarnivoreOrganism(create_genome(CreatureType.CARNIVORE, world), row, col, world), row, col)

def process_cells(world):
    visited = set()
    day = world.get_day()
    for row in range(ROWS):
        for col in range(COLS):
            organism = world.get_cell(row, col)
            if (organism and (organism not in visited) and
                (day == 0 or day != organism.get_birthday())):
                visited.add(organism)
                organism.choose_action()

    world.inc_day()


def start_game():
    """ Starts the current simulation if state is PAUSE"""
    global state
    state = PLAY
    view.update_playback_state(ButtonEvent.PLAY)

def pause_game():
    """ Pauses the current simulation if state is PLAY"""
    global state
    state = PAUSE
    view.update_playback_state(ButtonEvent.PAUSE)

def reset_game():
    """ Reinitializes new world and view object to reset simulation"""
    global world
    global view
    global state
    # Always start at Pause state
    state = PAUSE
    view.update_playback_state(ButtonEvent.PAUSE)

    world.reset()
    setup_life(world)
    view.update()

def step_game():
    """ Pauses current simulation to step forward one frame of gameloop"""
    global state
    state = PAUSE
    view.update_playback_state(ButtonEvent.PAUSE)
    process_cells(world)
    view.update()

def save_game():
    """ Saves current data to specified file """
    global world

    # Save data using pickle
    with open("world_save.pkl", "wb") as file:
        pickle.dump(world, file)
    print("Data saved successfully!")

def load_game():
    """ Loads a previously saved pickle file"""
    global world
    global view

    # Attempts to open file called "world_save"
    try:
        with open("world_save.pkl", 'rb') as file:
            savedWorld = pickle.load(file)

            # Overwrites current world and view object before updating view
            world = savedWorld
            view = View(ROWS, COLS, world, start_game, pause_game, reset_game, step_game, save_game, load_game)
            view.update()
    except:
        print("File not found! Try saving first.")


world = World()
view = View(ROWS, COLS, world, start_game, pause_game, reset_game, step_game,
            save_game, load_game)
clock = pygame.time.Clock()

setup_life(world)
view.update()
pygame.display.flip()

# main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break

        if event.type == pygame.KEYDOWN:
            # Press p to pause and unpause simulation
            if event.key == pygame.K_p and state == PLAY:
                pause_game()
            elif event.key == pygame.K_p and state == PAUSE:
                start_game()

            # Press r to restart simulation
            elif event.key == pygame.K_r:
                reset_game()

            # Press q to quit simulation
            elif event.key == pygame.K_q:
                pygame.quit()

            # Press s to save, brings up file explorer to name file
            elif event.key == pygame.K_s:
                save_game()

            # Press l to reload save, opens file explorer to choose file
            elif event.key == pygame.K_l:
                load_game()

            # Press m to generate a meteor to kill organisms in a 10x10 area
            elif event.key == pygame.K_m:
                events.meteor(world, view)
                view = View(ROWS, COLS, world, start_game, pause_game, reset_game, step_game, save_game, load_game)
                view.update()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            view.handle_click()
        elif event.type == pygame.MOUSEMOTION:
            view.handle_mouse_move()
        elif event.type == pygame.MOUSEBUTTONUP:
            view.handle_mouse_up()


    if state == PLAY:
        process_cells(world)
        view.update()

    pygame.display.flip()
    # limits FPS to 1
    # dt is delta time in seconds since last frame, used for framerate-independent physics.
    dt = clock.tick(20)

pygame.quit()