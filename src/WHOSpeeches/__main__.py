import pathlib
import sys
from argparse import ArgumentParser, Namespace
from .dtypes import settings
from .RetrieveSpeeches import RetrieveSpeeches

def main() -> None:
    parser = ArgumentParser(prog = 'WHOSpeeches', description = "Retrieve the WHO's Director General's Speeches.")
    retrieve_parser(parser)
    args = parser.parse_args()
    _print_args(args)
    args.run(args)

def retrieve_parser(parser: ArgumentParser) -> None:
    def run(args: Namespace) -> None:
        set = settings(args.dest)
        app = RetrieveSpeeches(set)
        app.init()
        app.retrieve()
    parser.add_argument('-dest', type = pathlib.Path, required = True, help = 'The location of the retrieved speeches')
    parser.set_defaults(run = run)

def _print_args(args: Namespace) -> None:
    print(f'---------')
    for key in args.__dict__.keys():
        if key not in ['run']:
            print(f'{key}: {args.__dict__[key]}')
    print('---------')

if __name__ == "__main__":
    sys.exit(main())
