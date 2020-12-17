import pathlib
import progressbar as pb
from argparse import ArgumentParser
from lxml import etree
from typeguard import typechecked

@typechecked
def convert_speeches_list(folder_out: pathlib.Path) -> None:
    """
    Converts the list of all of the WHO director general's speeches from a collection of HTML files into a single JSONL file

    Parameters
    ----------
    folder_out : pathlib.Path
        Folder to contain the downloaded documents
    """

    folder_out = folder_out.joinpath('./raw')
    if not folder_out.exists():
        raise RuntimeError(f'Could not find the HTML folder: {folder_out}')


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument(
        '-out', '--folder-out',
        help = 'Folder to contain the downloaded documents',
        type = pathlib.Path,
        default = 'd:/datasets/who')
    args = parser.parse_args()
    print(f'folder out: {args.folder_out}')
    convert_speeches_list(args.folder_out)
