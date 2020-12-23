import const
import pathlib
import jsonlines as jl
import progressbar as pb
import typing as t
from argparse import ArgumentParser
from datetime import datetime
from lxml import etree
from typeguard import typechecked


@typechecked
def convert_speeches_text(folder_in: pathlib.Path, file_out: pathlib.Path) -> None:
    """
    Converts the raw HTML speech of the director general's speeches to text

    Parameters
    ----------
    folder_in : pathlib.Path
        Folder to contain the downloaded documents
    file_out : pathlib.Path
        File containing the speeches text
    """

    if not folder_in.exists():
        raise RuntimeError(f'Could not find the HTML folder: {folder_in}')
    if file_out.exists():
        file_out.unlink()

    speech = 1
    widgets = [ 'Converting Speech # ', pb.Counter(), ' ', pb.BouncingBar(marker = '.', left = '[', right = ']'), ' ', pb.Timer()]
    with pb.ProgressBar(widgets = widgets) as bar:
        with open(file_out, 'w', encoding = 'utf-8') as fp:
            with jl.Writer(fp, compact = True, sort_keys = True) as writer:
                for file in folder_in.iterdir():
                    if file.stem.startswith('detail.') and file.suffix == '.html':
                        bar.update(speech)
                        speech = speech + 1
                        json = _process_document(file)
                        if len(json['text']) > 0:
                            writer.write(json)

@typechecked
def _process_document(file_in: pathlib.Path) -> dict:
    """
    Converts the HTML file into a JSON object containing the required elements

    Parameters
    ----------
    file_in : pathlib.Path
        File containing the speech
    """
    with open(file_in, 'r', encoding = 'utf-8') as fp:
        tree = etree.parse(fp, etree.HTMLParser())
    id = file_in.name
    title = tree.find("//head/title").text.strip()
    date = tree.find("//div[@class='row']//div[@class='date']/span").text.strip()
    date = datetime.strptime(date, '%d %B %Y').strftime('%Y-%m-%d')
    paragraphs = tree.findall("//article/div/p")
    paragraphs = [paragraph for paragraph in _get_innertext(paragraphs)]

    json = { 'id' : id, 'title' : title, 'date': date, 'text' : paragraphs }
    return json

@typechecked
def _get_innertext(nodes: t.List[etree.Element]) -> t.Iterator[str]:
    for node in nodes:
        subnodes = node.getchildren()
        result = []
        if node.text is not None:
            text = node.text.strip()
            if len(text) > 0:
                result.append(text)
        if len(subnodes) > 0:
            for text in _get_innertext(subnodes):
                result.append(text)
        if node.tail is not None:
            text = node.tail.strip()
            if len(text) > 0:
                result.append(text)
        result = ' '.join(result).strip()
        if len(result) > 0:
            yield result

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument(
        '-in', '--folder-in',
        help = 'Folder to contain the downloaded documents',
        type = pathlib.Path,
        required = True)
    parser.add_argument(
        '-out', '--file-out',
        help = 'File containing the speeches'' text',
        type = pathlib.Path,
        required = True)
    args = parser.parse_args()
    print(f'folder in: {args.folder_in}')
    print(f'file out: {args.file_out}')
    convert_speeches_text(args.folder_in, args.file_out)
