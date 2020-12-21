import const
import pathlib
import progressbar as pb
import typing as t
from argparse import ArgumentParser
from lxml import etree
from typeguard import typechecked


@typechecked
def convert_speeches_list(folder_in: pathlib.Path, file_out: pathlib.Path) -> None:
    """
    Converts the list of all of the WHO director general's speeches from a collection of HTML files into a single JSONL file

    Parameters
    ----------
    folder_in : pathlib.Path
        Folder to contain the downloaded documents
    file_out : pathlib.Path
        File contain the URLs to the speeches
    """

    if not folder_in.exists():
        raise RuntimeError(f'Could not find the HTML folder: {folder_in}')
    if file_out.exists():
        file_out.unlink()

    files = [f for f in folder_in.iterdir()]
    files = [f for f in files if f.suffix == '.html' and f.stem.startswith('header.')]
    links = [_extract_links(f) for f in files]
    links = [x for y in links for x in y]
    links = [link for link in sorted(list(set(links)))]

    with open(file_out, 'w', encoding = 'utf-8') as fp:
        for link in links:
            fp.writelines([link, '\n'])


@typechecked
def _extract_links(file_in: pathlib.Path) -> t.List[str]:
    """
    Extracts all the links from a single page
    
    Parameters
    ----------
    file_in : pathlib.Path
        The path to the current page
    """
    with open(file_in, 'r', encoding = 'utf-8') as fp:
        tree = etree.parse(fp, etree.HTMLParser())
    nodes = tree.findall("//div/div[@class='list-view--item vertical-list-item']/a[@role='link']")
    links = [node.attrib['href'] for node in nodes if 'href' in node.attrib]
    links = [f'{const.URL_TLD}{link}' for link in links]

    return links


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument(
        '-in', '--folder-in',
        help = 'Folder to contain the downloaded documents',
        type = pathlib.Path,
        required = True)
    parser.add_argument(
        '-out', '--file-out',
        help = 'File contain the URLs to the speeches',
        type = pathlib.Path,
        required = True)
    args = parser.parse_args()
    print(f'folder in: {args.folder_in}')
    print(f'file out: {args.file_out}')
    convert_speeches_list(args.folder_in, args.file_out)
