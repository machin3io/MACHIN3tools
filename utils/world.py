

def get_world_output(world):
    if not world.use_nodes:
        world.use_nodes = True

    output = world.node_tree.nodes.get('World Outputs')

    # fallback
    if not output:
        for node in world.node_tree.nodes:
            if node.type == 'OUTPUT_WORLD':
                return node
    return output
