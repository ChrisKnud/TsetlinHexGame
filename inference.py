import argparse

from GraphTsetlinMachine.graphs import Graphs

from format import load_tm

SYMBOLS = ['B', 'W', 'E']

def default_args(**kwargs):
    parser = argparse.ArgumentParser()
    parser.add_argument('--tm-path', type=str, help='Path of Tsetlin Machine pickle file')
    parser.add_argument('--data-path', type=str, help='Path to json file containing data to run inference on')
    parser.add_argument("--number-of-examples", default=6, type=int)
    parser.add_argument("--hypervector-size", default=16, type=int)
    parser.add_argument("--hypervector-bits", default=1, type=int)
    parser.add_argument('--double-hashing', dest='double_hashing', default=False, action='store_true')

    args = parser.parse_args()
    for key, value in kwargs.items():
        if key in args.__dict__:
            setattr(args, key, value)
    return args

args = default_args()


# Make graph
graphs = Graphs(
    args.number_of_examples,
    symbols=SYMBOLS,
    hypervector_size=args.hypervector_size,
    hypervector_bits=args.hypervector_bits,
    double_hashing = args.double_hashing
)

# Load Tsetlin Machine
tm = load_tm(args.tm_path)
tm.predict(graphs)

result = tm.predict(graphs)

print(result)