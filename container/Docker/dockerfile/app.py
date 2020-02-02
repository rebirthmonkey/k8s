import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--msg1", type=str)
parser.add_argument("--msg2", type=str)
args = parser.parse_args()


def main():
    if args.msg1:
        print(args.msg1)

    if args.msg2:
        print(args.msg2)


if __name__ == "__main__":
    main()