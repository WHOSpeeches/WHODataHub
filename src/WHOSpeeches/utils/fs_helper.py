import jsonlines as jl # type: ignore
import pathlib
import typing as t
from datetime import datetime
from ..dtypes import Speech

def cache_speeches(folder: pathlib.Path, speeches: t.Iterator[Speech]) -> t.Iterator[Speech]:
    file_name = folder.joinpath(f"{datetime.utcnow().strftime('%Y%m%d%H%M%S')}.jsonl")
    with open(file_name, 'w', encoding = 'utf-8') as fp:
        with jl.Writer(fp, compact = True, sort_keys = True) as writer:
            for speech in speeches:
                writer.write(speech) # type: ignore
                yield speech

def load_cached_speeches(folder: pathlib.Path) -> t.Iterator[Speech]:
    for file_name in folder.iterdir():
        if file_name.is_file() and file_name.suffix.lower() == '.jsonl' and not file_name.stem.startswith('_'):
            with open(file_name, 'r', encoding = 'utf-8') as fp:
                with jl.Reader(fp) as reader:
                    for item in reader: # type: ignore
                        yield item # type: ignore
