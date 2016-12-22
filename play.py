from game_of_life.location import Location
from game_of_life.render_life import render_life
from game_of_life.world import World

world = World.random(min_location=Location(0, 0),
                     max_location=Location(20, 20),
                     cell_count=50)
print(render_life(world, turns=20))
