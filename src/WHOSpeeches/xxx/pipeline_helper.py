import typing as t
from ..dtypes import Speech
from datetime import date, datetime

_date_key = 'FormatedDate'
_date_format =  "%d %B %Y"

def last_speech_date(speeches: t.Iterator[Speech]) -> date:
    max = date.min
    for speech in speeches:
        if _date_key in speech:
            curr = date.fromisoformat(speech[_date_key])
            if curr > max:
                max = curr
    return max    

def filter_old_speeches(end_date: date, speeches: t.Iterator[Speech]) -> t.Iterator[Speech]:
    for speech in speeches:
        if _date_key in speech:
            curr = datetime.strptime(speech[_date_key], _date_format)
            if end_date > curr:
                break
            yield speech 
