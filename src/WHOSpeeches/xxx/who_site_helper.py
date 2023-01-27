import requests
import protego # type: ignore
import time
import typing as t
from ..utils.const import *
from .html_helper import has_more_pages

def read_speech_list() -> t.Iterator[str]:
    """
    Get the list of all of the WHO director general's speeches.

    Parameters
    ----------
    folder_out : pathlib.Path
        Folder to contain the downloaded documents
    """
    with requests.Session() as session:
        session.headers['User-Agent'] = USER_AGENT
        rtxt = _setup_robots_txt(session)
        page = 1
        url = URL_SPEECHES.format(page = page)
        if rtxt.can_fetch(USER_AGENT, url): # type: ignore
            curr_page = _download_page(session, page)
            if curr_page is not None:
                yield curr_page
                while has_more_pages(curr_page):
                    _take_a_nap(rtxt)
                    page = page + 1
                    url = URL_SPEECHES.format(page = page)
                    curr_page = _download_page(session, page)
                    if curr_page is None: break
                    yield curr_page
        else:
            print(f'robots.txt forbids url: {url}')

def _setup_robots_txt(session: requests.Session) -> protego.Protego:
    with session.get(URL_ROBOTS) as response:
        rtxt: protego.Protego = protego.Protego.parse(response.text) # type: ignore
    return rtxt

def _download_page(session: requests.Session, page: int) -> str | None:
    url = URL_SPEECHES.format(page = page)
    with session.get(url) as response:
        if response.status_code == 200:
            return response.text
        else:
            print(f'could not open ({response.status_code}) url: {url}')

def _take_a_nap(rtxt: protego.Protego) -> None:
    delay: int | None = rtxt.crawl_delay(USER_AGENT) # type: ignore
    if isinstance(delay, int):
        time.sleep(delay)
    else:
        time.sleep(WEB_DELAY)
