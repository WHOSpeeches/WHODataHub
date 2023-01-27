import typing as t

Speech = t.Dict[str, str]
Speeches_Page = t.Dict[str, str | t.List[Speech]]
