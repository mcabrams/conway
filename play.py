import os

from game_of_life.location import Location
from game_of_life.turn_renderings import turn_renderings
from game_of_life.world import World


def clear_stdout():
    os.system('cls' if os.name == 'nt' else 'clear')


def play_demo():
    """
    Plays demo of Game of Life over 20 turns to stdout.
    """
    world = World.random(min_location=Location(0, 0),
                         max_location=Location(20, 20),
                         cell_count=50)

    for rendering in turn_renderings(world, turns=20):
        clear_stdout()
        print(rendering)

play_demo()
