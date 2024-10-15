import json
import os.path

import numpy as np
from GraphTsetlinMachine.graphs import Graphs

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
    
    
    
def init_graph(graphs, number_of_examples, number_of_classes, noise, board_width, data):

    for graph_id in range(number_of_examples):
        graphs.set_number_of_graph_nodes(graph_id, board_width * board_width)

    graphs.prepare_node_configuration()

    for graph_id in range(number_of_examples):
        print(f"\n\nGraph: {graph_id}")
        for node_id in range(graphs.number_of_graph_nodes[graph_id]):
            number_of_edges = get_number_of_edges(node_id, board_width)
            print(f"Node ({node_id}) edges: {number_of_edges}")
            graphs.add_graph_node(graph_id, node_id, number_of_edges)

    graphs.prepare_edge_configuration()

    Y_train = np.empty(number_of_examples, dtype=np.uint32)

    for graph_id in range(number_of_examples):
        print(f"\n\nGraph: {graph_id}")
        for node_id in range(graphs.number_of_graph_nodes[graph_id]):
            node_type = get_node_type(node_id, board_width)

            match node_type:
                case 'TopLeft':
                    connected_nodes = [node_id + 1, node_id + board_width]
                case 'TopRight':
                    connected_nodes = [node_id - 1, node_id + board_width - 1, node_id + board_width]
                case 'BottomLeft':
                    connected_nodes = [node_id + 1, node_id - board_width - 1, node_id - board_width]
                case 'BottomRight':
                    connected_nodes = [node_id - 1, node_id - board_width]
                case '1stRow':
                    connected_nodes = [node_id - 1, node_id + 1, node_id + board_width - 1, node_id + board_width]
                case 'LastRow':
                    connected_nodes = [node_id - 1, node_id + 1, node_id - board_width + 1, node_id - board_width]
                case '1stColumn':
                    connected_nodes = [node_id + 1, node_id + board_width, node_id - board_width + 1,
                                       node_id - board_width]
                case 'LastColumn':
                    connected_nodes = [node_id - 1, node_id - board_width, node_id + board_width - 1,
                                       node_id + board_width]
                case 'Default':
                    connected_nodes = [node_id + 1, node_id - 1, node_id - board_width, node_id - board_width + 1,
                                       node_id + board_width, node_id + board_width + 1]
                case _:
                    connected_nodes = None

            if connected_nodes is not None:
                print(f"Node type: {node_type}")
                for destination_node_id in connected_nodes:
                    print(f"Adding edge ({node_id}): {destination_node_id}")
                    if data[graph_id]['board'][node_id] == data[graph_id]['board'][destination_node_id]:
                        print(f"Winner node: {data[graph_id]['board'][node_id]}")
                        print(f"Node {node_id} and {destination_node_id} Connected")
                        graphs.add_graph_node_edge(graph_id, node_id, destination_node_id, 'Connected')
                    else:
                        print(f"Node {node_id} and {destination_node_id} NOT connected")
                        graphs.add_graph_node_edge(graph_id, node_id, destination_node_id, 'NOT Connected')
            else:
                print("Connected nodes is 1.")
                exit(-1)

        # 0 if black wins, 1 if white wins
        Y_train[graph_id] = 0 if data[graph_id]['winner'] == 'B' else 1

        print("Y train: " + str(Y_train[graph_id]))

        node_id = np.random.randint(Y_train[graph_id], graphs.number_of_graph_nodes[graph_id])

        for node_pos in range(Y_train[graph_id] + 1):
            if Y_train[graph_id] == 0:
                graphs.add_graph_node_property(graph_id, node_id - node_pos, 'B')
            else:
                graphs.add_graph_node_property(graph_id, node_id - node_pos, 'W')

        if np.random.rand() <= noise:
            Y_train[graph_id] = np.random.choice(np.setdiff1d(np.arange(number_of_classes), [Y_train[graph_id]]))

    graphs.encode()

    return Y_train


def train_data_from_file(path):
    with open(path, "r") as f:
        data = json.load(f)
    return data


def log_result(folder_path, file_name, result):
    if not os.path.exists(folder_path):
        print("Making dir: ")
        os.mkdir(folder_path)

    file_path = os.path.join(folder_path, f'{file_name}.log')

    with open(file_path, "a") as f:
        f.write(result + "\n")