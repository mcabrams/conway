from .world import WorldRenderer


def render_life(world, turns=1):
    render = ''
    for turn in range(0, turns + 1):
        if turn > 0:
            world = world.tick()
        render += ('Turn {}:\n'.format(turn) + WorldRenderer(world).render() + '\n')

    return render
