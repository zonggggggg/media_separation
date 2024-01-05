from src.args import parse_args
from src.separate import Separation


if __name__ == "__main__":
    args = parse_args()
    executor = Separation()
    executor.separation(args=args)
