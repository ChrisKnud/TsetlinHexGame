def add_hex_edges(graphs, graph_id, node_id, destination_node_ids):
    for id in destination_node_ids:
        graphs.add_graph_node_edge(graph_id, node_id, id, 'Connected')


def get_number_of_edges(node_id, board_width):
    node_type = get_node_type(node_id, board_width)

    match node_type:
        case 'TopLeft' | 'BottomRight':
            return 2
        case 'TopRight' | 'BottomLeft':
            return 3
        case '1stRow' | 'LastRow' | '1stColumn' | 'LastColumn':
            return 4
        case 'Default':
            return 6
        case _:
            return exit(-1)

"""
Returns one of the following:
    Corner
    1st Row (excluding corners)
    Last row (excluding corners)
    1st column (excluding corners)
    Last column (excluding corners)
    Default
"""
def get_node_type(node_id, board_width):
    board_size = board_width * board_width
    top_left = 0
    top_right = board_width - 1
    bottom_left = board_size - board_width
    bottom_right = board_size - 1

    # Corners
    if node_id == top_left:
        return 'TopLeft'
    elif node_id == top_right:
        return 'TopRight'
    elif node_id == bottom_left:
        return 'BottomLeft'
    elif node_id == bottom_right:
        return 'BottomRight'
    # 1st Row (excluding corners)
    elif 1 <= node_id <= board_width - 2:
        return '1stRow'
    # Last row (excluding corners)
    elif board_size - board_width + 1 <= node_id <= board_size - 2:
        return 'LastRow'
    # 1st column (excluding corners)
    elif node_id % board_width == 0 and node_id != bottom_left:
        return '1stColumn'
    # Last column (excluding corners)
    elif (node_id + 1) % board_width == 0 and node_id != bottom_right:
        return 'LastColumn'
    else:
        return 'Default'