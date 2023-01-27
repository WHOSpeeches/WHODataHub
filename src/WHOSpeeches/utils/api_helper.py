import json
import requests
import protego # type: ignore
import time
import typing as t
from .const import *
from ..dtypes import Speech, Speeches_Page

def api_speeches(skip: int = 0) -> t.Iterator[Speech]:
    """
    Get the list of all of the WHO director general's speeches.

    Parameters
    ----------
    skip : int
        How many documents from the front do we already have
    """
    next_link = API_SPEECHES.format(skip = skip)
    with requests.Session() as session:
        session.headers['User-Agent'] = USER_AGENT
        rtxt = _setup_robots_txt(session)
        if rtxt.can_fetch(USER_AGENT, next_link): # type: ignore            
            curr_page = _download_page(session, next_link)
            while curr_page is not None:
                speeches = _null_coalesce(curr_page, 'value')
                if isinstance(speeches, list):
                    for speech in speeches:
                        yield speech
                next_link = _null_coalesce(curr_page, '@odata.nextLink')
                if isinstance(next_link, str):
                    _take_a_nap(rtxt)
                    curr_page = _download_page(session, next_link)
                else:
                    curr_page = None
        else:
            print(f'robots.txt forbids url: {next_link}')

def _setup_robots_txt(session: requests.Session) -> protego.Protego:
    with session.get(URL_ROBOTS) as response:
        rtxt = protego.Protego.parse(response.text) # type: ignore
    return rtxt

def _download_page(session: requests.Session, url: str) -> Speeches_Page | None:
    with session.get(url) as response:
        if response.status_code == 200:
            page: Speeches_Page = json.loads(response.text)
            return page
        else:
            print(f'could not open ({response.status_code}) url: {url}')

def _null_coalesce(page: Speeches_Page, key: str) -> str | t.List[Speech] | None:
    if key in page:
        return page[key]

def _take_a_nap(rtxt: protego.Protego) -> None:
    delay: int | None = rtxt.crawl_delay(USER_AGENT) # type: ignore
    if isinstance(delay, int):
        time.sleep(delay)
    else:
        time.sleep(WEB_DELAY)
