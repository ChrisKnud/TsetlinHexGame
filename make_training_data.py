import argparse

from generate_training_data.granmo_c_to_train import granmo_c_to_train
from generate_training_data.kaggle_hex_to_train import kaggle_hex_to_train


def default_args(**kwargs):
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-format", default='granmo', type=str, help="Format of the source data: granmo or kaggle")
    parser.add_argument("--file-name", type=str, help="File to the text file containing training data from Granmo's C code")
    parser.add_argument("--split", default=True, type=bool, help="Whether to split training data or not")
    parser.add_argument("--number-of-items", default=1000, type=int, help="Number of trainnig examples to convert when using the kaggle dataset")

    args = parser.parse_args()
    for key, value in kwargs.items():
        if key in args.__dict__:
            setattr(args, key, value)
    return args

args = default_args()


if args.data_format == 'granmo':
    granmo_c_to_train(file_name=args.file_name, split=args.split)
elif args.data_format == 'kaggle':
    kaggle_hex_to_train(number_of_items=args.number_of_items, split=args.split)