import argparse
import os.path
from time import time
from datetime import datetime
from GraphTsetlinMachine.graphs import Graphs
from GraphTsetlinMachine.tm import MultiClassGraphTsetlinMachine
from format import init_graph, train_data_from_file, log_result
from plot import plot

# Hex settings
BOARD_WIDTH = 3

# B = Black
# W = White
# E = Empty
SYMBOLS = ['B', 'W', 'E']
train_path = os.path.join('.', 'data', 'hex_train.json')
test_path = os.path.join('.', 'data', 'hex_test.json')

x_train = train_data_from_file(train_path)['result']
x_test = train_data_from_file(test_path)['result']

dt = datetime.now()
training_log_folder = os.path.join('.', 'log', 'train', f'train-{dt}') # f'train-{datetime.now()}.log'
eval_log_folder = os.path.join('.', 'log', 'eval', f'eval-{dt}') #  f'eval-{datetime.now()}.log'

# Graph settings
def default_args(**kwargs):
    parser = argparse.ArgumentParser()
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
    data=x_train
)

graphs_test = Graphs(args.number_of_examples, init_with=graphs_train)

Y_test = init_graph(
    graphs=graphs_test,
    number_of_examples=args.number_of_examples,
    number_of_classes=args.number_of_classes,
    noise=args.noise,
    board_width=BOARD_WIDTH,
    data=x_test
)

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

log_result(training_log_folder, f'train-{dt}', "#    result train    result test    train time    test time")

# Plot data
plot_x = []
plot_y = []
log_data = ""


for i in range(args.epochs):
    start_training = time()
    tm.fit(graphs_train, Y_train, epochs=1, incremental=True)
    stop_training = time()

    start_testing = time()
    result_test = 100*(tm.predict(graphs_test) == Y_test).mean()
    stop_testing = time()

    result_train = 100*(tm.predict(graphs_train) == Y_train).mean()

    log_data += "%d    %.2f    %.2f    %.2f    %.2f" % (i, result_train, result_test, stop_training - start_training, stop_testing - start_testing)
    log_data += f"\n\nTrain prediction: {tm.predict(graphs_train)}. True value: {Y_train}\nTest prediction: {tm.predict(graphs_test)}. True value: {Y_test}\n"

    if i % args.log_interval == 0:
        log_result(training_log_folder, f'train-{dt}', log_data)
        plot_x.append(i)
        plot_y.append(result_test)
        log_data = ""
        print("Epoch: " + str(i))

plot(plot_x, plot_y, x_label='Epoch', y_label='Accuracy (%)', title='Accuracy Test Data', path=os.path.join(training_log_folder, 'plot.png'))
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

hv_log = f"Test data hypervectors:\n{str(graphs_test.hypervectors)}\n\nTM hypervectors: {str(tm.hypervectors)}"
log_result(training_log_folder, f"test-hv-{dt}", hv_log)
log_result(training_log_folder, f"test-edge-type-{dt}", str(graphs_test.edge_type_id))