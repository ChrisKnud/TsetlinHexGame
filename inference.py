import argparse

from format import load_tm


def default_args(**kwargs):
    parser = argparse.ArgumentParser()
    parser.add_argument('--tm-path', type=str, help='Path of Tsetlin Machine pickle file')
    parser.add_argument('--data-path', type=str, help='Path to json file containing data to run inference on')

    args = parser.parse_args()
    for key, value in kwargs.items():
        if key in args.__dict__:
            setattr(args, key, value)
    return args

args = default_args()

tm = load_tm(args.tm_path)

print(tm.hypervectors)