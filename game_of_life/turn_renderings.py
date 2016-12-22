from .world_renderer import WorldRenderer


def turn_renderings(world, turns=1, animate=False):
    for turn in range(0, turns + 1):
        if turn > 0:
            world = world.tick()

        yield 'Turn {}:\n'.format(turn) + WorldRenderer(world).render()
