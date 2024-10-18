import argparse

board = [
                "E",
                "B",
                "E",
                "E",
                "E",
                "E",
                "W",
                "B",
                "E",
                "E",
                "E",
                "E",
                "E",
                "E",
                "E",
                "B",
                "E",
                "E",
                "B",
                "E",
                "E",
                "E",
                "B",
                "E",
                "B",
                "E",
                "B",
                "E",
                "E",
                "W",
                "B",
                "E",
                "E",
                "E",
                "E",
                "E",
                "W",
                "E",
                "E",
                "E",
                "E",
                "E",
                "E",
                "E",
                "E",
                "B",
                "E",
                "E",
                "E",
                "E",
                "B",
                "E",
                "E",
                "E",
                "E",
                "B",
                "B",
                "W",
                "E",
                "E",
                "E",
                "B",
                "W",
                "W",
                "W",
                "W",
                "E",
                "E",
                "E",
                "E",
                "E",
                "E",
                "W",
                "B",
                "E",
                "B",
                "E",
                "E",
                "B",
                "E",
                "E",
                "E",
                "W",
                "E",
                "B",
                "B",
                "E",
                "E",
                "E",
                "B",
                "E",
                "B",
                "W",
                "E",
                "W",
                "E",
                "E",
                "W",
                "E",
                "W",
                "E",
                "E",
                "W",
                "W",
                "E",
                "B",
                "E",
                "E",
                "W",
                "W",
                "W",
                "W",
                "W",
                "W",
                "E",
                "E",
                "B",
                "W",
                "B",
                "E",
                "E"
            ]

small_board = [
    'B', 'B', 'B',
    'W', 'W', 'E',
    'E', 'W', 'B'
]


# Create a hexagonal board with a radius of 1.0, 5 rows and 5 columns
#hex_grid(1.0,  board)

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

for i in args.__dict__.items(): print(i)