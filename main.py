from GraphTsetlinMachine.graphs import Graphs
import numpy as np
from fontTools.svgLib.path.parser import BOOL_RE
from scipy.sparse import csr_matrix
from GraphTsetlinMachine.tm import MultiClassGraphTsetlinMachine
from time import time
import argparse

from data import x_train
from format import get_number_of_edges, get_node_type

# Hex settings
BOARD_WIDTH = 3

# B = Black
# W = White
# E = Empty
SYMBOLS = ['B', 'W', 'E']


# Graph settings
def default_args(**kwargs):
    parser = argparse.ArgumentParser()
    parser.add_argument("--epochs", default=25, type=int)
    parser.add_argument("--number-of-clauses", default=60, type=int)
    parser.add_argument("--T", default=200, type=int)
    parser.add_argument("--s", default=1.0, type=float)
    parser.add_argument("--depth", default=3, type=int)
    parser.add_argument("--hypervector-size", default=16, type=int)
    parser.add_argument("--hypervector-bits", default=1, type=int)
    parser.add_argument("--message-size", default=256, type=int)
    parser.add_argument("--message-bits", default=2, type=int)
    parser.add_argument('--double-hashing', dest='double_hashing', default=False, action='store_true')
    parser.add_argument("--noise", default=0.01, type=float)
    parser.add_argument("--number-of-examples", default=6, type=int)
    parser.add_argument("--number-of-classes", default=3, type=int)
    parser.add_argument("--max-sequence-length", default=10, type=int)
    parser.add_argument("--max-included-literals", default=4, type=int)

    args = parser.parse_args()
    for key, value in kwargs.items():
        if key in args.__dict__:
            setattr(args, key, value)
    return args


args = default_args()

print("Creating training data")

# Create train data

graphs_train = Graphs(
    args.number_of_examples,
    symbols=SYMBOLS,
    hypervector_size=args.hypervector_size,
    hypervector_bits=args.hypervector_bits,
    double_hashing=args.double_hashing
)

for graph_id in range(args.number_of_examples):
    graphs_train.set_number_of_graph_nodes(graph_id, BOARD_WIDTH * BOARD_WIDTH)

graphs_train.prepare_node_configuration()

for graph_id in range(args.number_of_examples):
    print(f"\n\nGraph: {graph_id}")
    for node_id in range(graphs_train.number_of_graph_nodes[graph_id]):
        number_of_edges = get_number_of_edges(node_id, BOARD_WIDTH)
        print(f"Node ({node_id}) edges: {number_of_edges}")
        graphs_train.add_graph_node(graph_id, node_id, number_of_edges)

graphs_train.prepare_edge_configuration()

Y_train = np.empty(args.number_of_examples, dtype=np.uint32)

for graph_id in range(args.number_of_examples):
    print(f"\n\nGraph: {graph_id}")
    for node_id in range(graphs_train.number_of_graph_nodes[graph_id]):
        node_type = get_node_type(node_id, BOARD_WIDTH)

        match node_type:
            case 'TopLeft':
                connected_nodes = [node_id + 1, node_id + BOARD_WIDTH]
            case 'TopRight':
                connected_nodes = [node_id - 1, node_id + BOARD_WIDTH - 1, node_id + BOARD_WIDTH]
            case 'BottomLeft':
                connected_nodes = [node_id + 1, node_id - BOARD_WIDTH - 1, node_id - BOARD_WIDTH]
            case 'BottomRight':
                connected_nodes = [node_id - 1, node_id - BOARD_WIDTH]
            case '1stRow':
                connected_nodes = [node_id - 1, node_id + 1, node_id + BOARD_WIDTH - 1, node_id + BOARD_WIDTH]
            case 'LastRow':
                connected_nodes = [node_id - 1, node_id + 1, node_id - BOARD_WIDTH + 1, node_id - BOARD_WIDTH]
            case '1stColumn':
                connected_nodes = [node_id + 1, node_id + BOARD_WIDTH, node_id - BOARD_WIDTH + 1, node_id - BOARD_WIDTH]
            case 'LastColumn':
                connected_nodes = [node_id - 1, node_id - BOARD_WIDTH, node_id + BOARD_WIDTH - 1, node_id + BOARD_WIDTH]
            case 'Default':
                connected_nodes = [node_id + 1, node_id - 1, node_id - BOARD_WIDTH, node_id - BOARD_WIDTH + 1, node_id + BOARD_WIDTH, node_id + BOARD_WIDTH + 1]
            case _:
                connected_nodes = None

        if connected_nodes is not None:
            print(f"Node type: {node_type}")
            for destination_node_id in connected_nodes:
                print(f"Adding edge ({node_id}): {destination_node_id}")
                if x_train[graph_id]['board'][node_id] == x_train[graph_id]['board'][destination_node_id]:
                    print(f"Winner node: {x_train[graph_id]['board'][node_id]}")
                    print(f"Node {node_id} and {destination_node_id} Connected")
                    graphs_train.add_graph_node_edge(graph_id, node_id, destination_node_id, 'Connected')
                else:
                    print(f"Node {node_id} and {destination_node_id} NOT connected")
                    graphs_train.add_graph_node_edge(graph_id, node_id, destination_node_id, 'NOT Connected')
        else:
            print("Connected nodes is 1.")
            exit(-1)


    # 0 if black wins, 1 if white wins
    Y_train[graph_id] = 0 if x_train[graph_id]['winner'] == 'B' else 1

    print("Y train: " + str(Y_train[graph_id]))

    node_id = np.random.randint(Y_train[graph_id], graphs_train.number_of_graph_nodes[graph_id])

    for node_pos in range(Y_train[graph_id] + 1):
        if Y_train[graph_id] == 0:
            graphs_train.add_graph_node_property(graph_id, node_id - node_pos, 'B')
        else:
            graphs_train.add_graph_node_property(graph_id, node_id - node_pos, 'W')

    if np.random.rand() <= args.noise:
        Y_train[graph_id] = np.random.choice(np.setdiff1d(np.arange(args.number_of_classes), [Y_train[graph_id]]))

graphs_train.encode()












"""

# Create test data

print("Creating testing data")

graphs_test = Graphs(args.number_of_examples, init_with=graphs_train)
for graph_id in range(args.number_of_examples):
    graphs_test.set_number_of_graph_nodes(graph_id, np.random.randint(args.number_of_classes, args.max_sequence_length+1))

graphs_test.prepare_node_configuration()

for graph_id in range(args.number_of_examples):
    for node_id in range(graphs_test.number_of_graph_nodes[graph_id]):
        number_of_edges = 1 if node_id > 0 and node_id < graphs_test.number_of_graph_nodes[graph_id]-1 else 0
        graphs_test.add_graph_node(graph_id, node_id, number_of_edges)

graphs_test.prepare_edge_configuration()

Y_test = np.empty(args.number_of_examples, dtype=np.uint32)
for graph_id in range(args.number_of_examples):
    for node_id in range(graphs_test.number_of_graph_nodes[graph_id]):
        if node_id > 0:
            destination_node_id = node_id - 1
            edge_type = "Left"
            graphs_test.add_graph_node_edge(graph_id, node_id, destination_node_id, edge_type)

        if node_id < graphs_test.number_of_graph_nodes[graph_id]-1:
            destination_node_id = node_id + 1
            edge_type = "Right"
            graphs_test.add_graph_node_edge(graph_id, node_id, destination_node_id, edge_type)

    Y_test[graph_id] = np.random.randint(args.number_of_classes)
    node_id = np.random.randint(Y_test[graph_id], graphs_test.number_of_graph_nodes[graph_id])
    for node_pos in range(Y_test[graph_id] + 1):
        graphs_test.add_graph_node_property(graph_id, node_id - node_pos, 'A')

graphs_test.encode()

tm = MultiClassGraphTsetlinMachine(
    args.number_of_clauses,
    args.T,
    args.s,
    depth=args.depth,
    message_size=args.message_size,
    message_bits=args.message_bits,
    max_included_literals=args.max_included_literals,
    grid=(16*13,1,1),
    block=(128,1,1)
)

for i in range(args.epochs):
    start_training = time()
    tm.fit(graphs_train, Y_train, epochs=1, incremental=True)
    stop_training = time()

    start_testing = time()
    result_test = 100*(tm.predict(graphs_test) == Y_test).mean()
    stop_testing = time()

    result_train = 100*(tm.predict(graphs_train) == Y_train).mean()

    print("%d %.2f %.2f %.2f %.2f" % (i, result_train, result_test, stop_training-start_training, stop_testing-start_testing))

weights = tm.get_state()[1].reshape(2, -1)
for i in range(tm.number_of_clauses):
        print("Clause #%d W:(%d %d)" % (i, weights[0,i], weights[1,i]), end=' ')
        l = []
        for k in range(args.hypervector_size * 2):
            if tm.ta_action(0, i, k):
                if k < args.hypervector_size:
                    l.append("x%d" % (k))
                else:
                    l.append("NOT x%d" % (k - args.hypervector_size))

        for k in range(args.message_size * 2):
            if tm.ta_action(1, i, k):
                if k < args.message_size:
                    l.append("c%d" % (k))
                else:
                    l.append("NOT c%d" % (k - args.message_size))

        print(" AND ".join(l))

print(graphs_test.hypervectors)
print(tm.hypervectors)
print(graphs_test.edge_type_id)
"""