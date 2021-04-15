import importlib
from argparse import ArgumentParser


def compile(module_name):
    module = importlib.import_module(module_name)
    module.detect_spam.optimize()


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("module_name")
    args = parser.parse_args()
    compile(args.module_name)
