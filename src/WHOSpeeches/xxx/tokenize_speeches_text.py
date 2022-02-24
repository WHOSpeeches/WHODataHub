import pathlib
import jsonlines as jl
import progressbar as pb
import typing as t
from argparse import ArgumentParser
from nltk.tokenize import word_tokenize, sent_tokenize
from typeguard import typechecked

_replace = {'`': '\'', '’': '\'', '‘': '\'', '“': '"', '”': '"', '–': '-'}

@typechecked
def tokenize_speeches_text(file_in: pathlib.Path, file_out: pathlib.Path) -> None:
    """
    Tokenizes all the files into the standard form: one sentence per line

    Parameters
    ----------
    file_in : pathlib.Path
        The JSONL containing all the speeches
    file_out : pathlib.Path
        The JSONL containing all the speeches after tokenization
    """

    if not file_in.exists():
        raise RuntimeError(f'Could not find the JSONL speeches: {file_in}')
    if file_out.exists():
        file_out.unlink()

    cnt = 1
    widgets = [ 'Tokenizing Speech # ', pb.Counter(), ' ', pb.BouncingBar(marker = '.', left = '[', right = ']'), ' ', pb.Timer()]
    with pb.ProgressBar(widgets = widgets) as bar:
        with open(file_in, 'r', encoding = 'utf-8') as fpin:        
            with open(file_out, 'w', encoding = 'utf-8') as fpout:
                with jl.Reader(fpin) as reader:
                    with jl.Writer(fpout, compact = True, sort_keys = True) as writer:
                        for speech in reader:
                            bar.update(cnt)
                            cnt = cnt + 1
                            json = _process_speech(speech)
                            writer.write(json)

@typechecked
def _process_speech(speech: dict) -> dict:
    lines = [line.strip() for line in speech['text']]
    lines = [line for line in _cleanup_lines(lines)]
    lines = [line for line in _tokenize_lines(lines)]
    json = {}
    for key, value in speech.items():
        json[key] = value
    json['tokenized'] = lines
    return json

@typechecked
def _cleanup_lines(lines: t.List[str]) -> t.Iterator[str]:
    """
    Does all the charactor swaps we may need
    """
    for line in lines:
        for key, value in _replace.items():
            line = line.replace(key, value)
        yield line

@typechecked
def _tokenize_lines(lines: t.List[str]) -> t.Iterator[str]:
    """
    Tokenizes all the lines into paragraphs/words using standard Punkt + Penn Treebank tokenizers
    """

    for line in lines:
        if line == '':
            yield ''
        else:
            sentences = sent_tokenize(line)
            for sentence in sentences:
                words = word_tokenize(sentence)
                yield ' '.join(words)

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument(
        '-in', '--file-in',
        help = 'The JSONL containing all the speeches',
        type = pathlib.Path,
        required = True)
    parser.add_argument(
        '-out', '--file-out',
        help = 'The JSONL containing all the speeches after tokenization',
        type = pathlib.Path,
        required = True)
    args = parser.parse_args()    
    print(f'file in: {args.file_in}')
    print(f'file out: {args.file_out}')
    tokenize_speeches_text(args.file_in, args.file_out)
