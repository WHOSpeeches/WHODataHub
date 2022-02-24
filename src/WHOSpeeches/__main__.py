
import pathlib
import sys
from .__init__ import __version__
from .get_speeches_list import get_speeches_list
from argparse import ArgumentParser
from typeguard import typechecked

@typechecked
def main() -> None:
    parser = ArgumentParser(prog = 'WHOSpeeches', description = "Retrieve the WHO's Director General's Speeches.")
    parser.add_argument('-out', dest = 'file_out', type = pathlib.Path, required = True, help = 'File to store the results')
    args = parser.parse_args()

    print(f'WHOSpeeches v{__version__}')
    print('---------')
    print(f'File Out: {str(args.file_out)}')
    print('---------')

    temp = args.file_out.parent.joinpath('./temp')
    get_speeches_list(temp)


if __name__ == "__main__":
    sys.exit(main())