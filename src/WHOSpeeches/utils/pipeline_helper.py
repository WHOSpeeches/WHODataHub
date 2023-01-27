import typing as t
from ..dtypes import Speech

def extract_urls(speeches: t.Iterator[Speech]) -> t.Iterator[str]:
    key = 'ItemDefaultUrl'
    for speech in speeches:
        if key in speech:
            yield speech[key]
