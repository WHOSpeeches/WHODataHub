import csv
import pathlib
import jsonlines as jl
import progressbar as pb
import typing as t
from argparse import ArgumentParser
from typeguard import typechecked

@typechecked
def qa_speeches_text(raw_folder: pathlib.Path, jsonl_file: pathlib.Path, file_out: pathlib.Path) -> None:
    """
    Runs a simple QA check on the converted speeches

    Parameters
    ----------
    raw_folder : pathlib.Path
        Folder to contain the downloaded documents
    jsonl_file : pathlib.Path
        File containing the speeches text
    file_out : pathlib.Path
        File containing the QA results
    """

    if not raw_folder.exists():
        raise RuntimeError(f'Could not find the HTML folder: {raw_folder}')
    if not jsonl_file.exists():
        raise RuntimeError(f'Could not find the JSONL file: {jsonl_file}')
    if file_out.exists():
        file_out.unlink()

    speech = 1
    widgets = [ 'QA Speech # ', pb.Counter(), ' ', pb.BouncingBar(marker = '.', left = '[', right = ']'), ' ', pb.Timer()]
    with pb.ProgressBar(widgets = widgets) as bar:
        with open(jsonl_file, 'r', encoding = 'utf-8') as fpr:
            with jl.Reader(fpr) as reader:
                with open(file_out, 'w', encoding = 'utf-8', newline = '') as fpw:            
                    writer = csv.writer(fpw, delimiter = ',', quotechar = '"', quoting = csv.QUOTE_ALL)
                    writer.writerow(['id', 'raw_count', 'converted_count'])
                    for json in reader:
                        bar.update(speech)
                        speech = speech + 1
                        (full, converted) = _process_document(raw_folder, json)
                        writer.writerow([json['id'], full, converted])

@typechecked
def _process_document(raw_folder: pathlib.Path, json: dict) -> t.Tuple[int, int]:
    """
    Calculates basic measures to help understand if the process worked as expected
    """
    
    file_in = raw_folder.joinpath(json['id'])
    with open(file_in, 'r', encoding = 'utf-8') as fp:
        full_size = sum([len(line) for line in fp.readlines()])    
    converted_size = sum([len(line) for line in json['text']])

    return full_size, converted_size

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument(
        '-raw', '--raw-folder',
        help = 'Folder to contain the downloaded documents',
        type = pathlib.Path,
        required = True)
    parser.add_argument(
        '-jsonl', '--jsonl-file',
        help = 'File containing the speeches'' text',
        type = pathlib.Path,
        required = True)
    parser.add_argument(
        '-out', '--file-out',
        help = 'File containing the QA results',
        type = pathlib.Path,
        required = True)
    args = parser.parse_args()
    print(f'raw folder in: {args.raw_folder}')
    print(f'jsonl file in: {args.jsonl_file}')
    print(f'qa file out: {args.file_out}')
    qa_speeches_text(args.raw_folder, args.jsonl_file, args.file_out)
