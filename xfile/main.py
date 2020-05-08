import argparse
from xfile.base import File, Engine


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file')
    args = parser.parse_args()

    e = Engine()
    for results in e.run(File(args.file)):
        results.show()


if __name__ == '__main__':
    main()
