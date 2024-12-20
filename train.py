import argparse
import math
import os.path
from time import time
from datetime import datetime
from GraphTsetlinMachine.graphs import Graphs
from GraphTsetlinMachine.tm import GraphTsetlinMachine, MultiClassGraphTsetlinMachine
from format import init_graph, train_data_from_file, log_result, board_as_string, clauses_as_string, save_tm, \
    write_to_csv
from plot import plot
from utils.helper_functions import draw_simple_graph, show_graph_nodes, show_graph_edges

# B = Black
# W = White
# E = Empty
SYMBOLS = ['B', 'W', 'E']

train_path = os.path.join('.', 'data', 'self', 'training_data.json')
test_path = os.path.join('.', 'data', 'self', 'eval_data.json')
csv_path = os.path.join('.', 'log', 'results_bridge.csv')

# Graph settings
def default_args(**kwargs):
    parser = argparse.ArgumentParser()
    parser.add_argument("--use-multigraph-tm", default=False, type=bool)
    parser.add_argument("--epochs", default=1000, type=int)
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
    parser.add_argument("--number-of-eval-examples", default=6, type=int)
    parser.add_argument("--moves-before-end", default=0, type=int)
    parser.add_argument("--number-of-classes", default=3, type=int)
    parser.add_argument("--max-sequence-length", default=10, type=int)
    parser.add_argument("--max-included-literals", default=4, type=int)
    parser.add_argument("--log-interval", default=10, type=int)

    args = parser.parse_args()
    for key, value in kwargs.items():
        if key in args.__dict__:
            setattr(args, key, value)
    return args


args = default_args()

print("Creating training data")

hyperparams = ''
for arg in args.__dict__.items(): hyperparams += str(arg)

x_train = train_data_from_file(train_path)['result']
x_test = train_data_from_file(test_path)['result']


# Hex settings
BOARD_WIDTH = int(math.sqrt(len(x_train[0]['board'])))
print("Board width: " + str(BOARD_WIDTH))

dt = str(datetime.now()).replace(' ', '')
training_log_folder = os.path.join('.', 'log', 'train', f'train-{dt}')
eval_log_folder = os.path.join('.', 'log', 'eval', f'eval-{dt}')

log_result(training_log_folder, f'data-used-{dt}', f"Training data: {train_path}\nTest data: {test_path}")
log_result(training_log_folder, f'hyperparams-{dt}', hyperparams)

# Create train data
graphs_train = Graphs(
    args.number_of_examples,
    symbols=SYMBOLS,
    hypervector_size=args.hypervector_size,
    hypervector_bits=args.hypervector_bits,
    double_hashing = args.double_hashing
)

Y_train = init_graph(
    graphs=graphs_train,
    number_of_examples=args.number_of_examples,
    number_of_classes=args.number_of_classes,
    noise=args.noise,
    board_width=BOARD_WIDTH,
    data=x_train,
    empty_symbol=SYMBOLS[2]
)

graphs_test = Graphs(args.number_of_eval_examples, init_with=graphs_train)

Y_test = init_graph(
    graphs=graphs_test,
    number_of_examples=args.number_of_eval_examples,
    number_of_classes=args.number_of_classes,
    noise=args.noise,
    board_width=BOARD_WIDTH,
    data=x_test,
    empty_symbol=SYMBOLS[2]
)


if args.use_multigraph_tm:
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
else:
    tm = GraphTsetlinMachine(
        args.number_of_clauses,
        args.T,
        args.s,
        depth=args.depth,
        message_size=args.message_size,
        message_bits=args.message_bits,
        max_included_literals=args.max_included_literals,
        grid=(16 * 13, 1, 1),
        block=(128, 1, 1)
    )


print(f"Graph 0 train: {graphs_train.print_graph(0)}")
print(f"Graph 0 test: {graphs_test.print_graph(0)}")

for i in range(len(x_train)):
    log_result(training_log_folder, f'boards-train-{dt}', f'{i} Winner: {x_train[i]["winner"]}\n{board_as_string(x_train[i]["board"])}')

for i in range(len(x_test)):
    log_result(training_log_folder, f'boards-test-{dt}', f'{i} Winner: {x_test[i]["winner"]}\n{board_as_string(x_test[i]["board"])}')

log_result(training_log_folder, f'train-{dt}', "#    result train    result test    train time    test time")

# Plot data
plot_x = []
plot_y = []
log_data = ""

best_train_result = 0
best_test_result = 0
highest_train_time = 0
highest_test_time = 0

total_start_time = time()

for i in range(args.epochs):
    start_training = time()

    if args.use_multigraph_tm:
        tm.fit(graphs_train, Y_train, epochs=1, incremental=True)
    else:
        tm.fit(graphs_train, Y_train)

    train_predictions = tm.predict(graphs_train)
    test_predictions = tm.predict(graphs_test)

    result_train = 100 * (train_predictions == Y_train).mean()
    stop_training = time()

    start_testing = time()
    result_test = 100 * (test_predictions == Y_test).mean()
    stop_testing = time()

    train_time = stop_training - start_training
    test_time = stop_testing - start_testing

    if result_train > best_train_result:
        best_train_result = result_train
    if result_test > best_test_result:
        print("New best")
        best_test_result = result_test
    if train_time > highest_train_time:
        highest_train_time = train_time
    if test_time > highest_test_time:
        highest_test_time = test_time

    weights = tm.get_state()[1].reshape(2, -1)

    print(f"Current best {best_test_result}%")
    print(f"Epoch {str(i)}: train result: {result_train}\n"
          f"test result: {result_test}\n")
          #f"Weights: {weights}")
          #f"{clauses_as_string(tm, weights, args.hypervector_size, args.message_size)}")
    print(f"Score graph train 0: {tm.score(graphs_train)[0]}")
    print(f"Score graph test 0: {tm.score(graphs_test)[0]}")

    print(f"Train prediction: {train_predictions}.\nTrue value: {Y_train}\n\nTest prediction: {test_predictions}.\nTrue value: {Y_test}\n\n")

    log_data += "%d    %.2f    %.2f    %.2f    %.2f" % (i, result_train, result_test, train_time, test_time)
    log_data += f"\n\nTrain prediction: {train_predictions}.\nTrue value: {Y_train}\n\nTest prediction: {test_predictions}.\nTrue value: {Y_test}\n"

    if i % args.log_interval == 0:
        log_result(training_log_folder, f'train-{dt}', log_data)
        plot_x.append(i)
        plot_y.append(result_test)
        log_data = ""

total_end_time = time()

plot(plot_x, plot_y, x_label='Epoch', y_label='Accuracy (%)', title='Accuracy Test Data', path=os.path.join(training_log_folder, 'plot.png'))

# Uncomment to log clauses. Uses alot of time
# when using a lot of clauses
#if args.use_multigraph_tm:
#    weights = tm.get_state()[1].reshape(2, -1)
#    clauses = clauses_as_string(tm, weights, args.hypervector_size, args.message_size)
#    log_result(training_log_folder, f'clauses-{dt}', clauses)

print(graphs_test.hypervectors)
print(tm.hypervectors)
print(graphs_test.edge_type_id)

hv_log = f"Test data hypervectors:\n{str(graphs_test.hypervectors)}\n\nTM hypervectors: {str(tm.hypervectors)}"
log_result(training_log_folder, f"test-hv-{dt}", hv_log)
log_result(training_log_folder, f"test-edge-type-{dt}", str(graphs_test.edge_type_id))

print('Saving Tsetlin Machine at: ' + str(os.path.join(training_log_folder, 'tm.pkl')))
save_tm(tm, os.path.join(training_log_folder, 'tm.pkl'))

#Write to csv
gtm_type = "Multi" if args.use_multigraph_tm else "Single"
csv_data = [
    {"GTM Type": gtm_type, "Board Size": BOARD_WIDTH, "Game State": args.moves_before_end, "Train Dataset": train_path, "Test Dataset": test_path, "Log Folder": training_log_folder, "#Examples": args.number_of_examples, "Epochs": args.epochs, "#Clauses": args.number_of_clauses, "T": args.T, "s": args.s, "Train Accuracy": best_train_result, "Test Accuracy": best_test_result, "Train Time": highest_train_time, "Test Time": highest_test_time, "Total Time": total_end_time - total_start_time},
]

write_to_csv(csv_path, csv_data)