import pathlib
import requests
import protego
import progressbar as pb
from .const import *
from .utils import *
from datetime import datetime
from lxml import etree
from typeguard import typechecked

_run_id = datetime.utcnow().strftime('%Y%m%d%H%M%S')

@typechecked
def get_speeches_list(folder_out: pathlib.Path) -> None:
    """
    Get the list of all of the WHO director general's speeches.
    When running the 2nd time, check your local copy to determine how far back you need to pull.

    Parameters
    ----------
    folder_out : pathlib.Path
        Folder to contain the downloaded documents
    """

    folder_out.mkdir(parents = True, exist_ok = True)

    with requests.Session() as session:
        session.headers['User-Agent'] = USER_AGENT
        rtxt = _setup_robots_txt(session)
        page = 1
        url = URL_SPEECHES.format(page = page)
        if rtxt.can_fetch(USER_AGENT, url):
            widgets = [ 'Retrieving Page # ', pb.Counter(), ' ', pb.BouncingBar(marker = '.', left = '[', right = ']'), ' ', pb.Timer()]
            with pb.ProgressBar(widgets = widgets) as bar:
                bar.update(page)
                curr_file = _download_page(session, page, folder_out)
                while _has_more_pages(curr_file) and _need_more_pages(curr_file):
                    take_a_nap(rtxt)
                    page = page + 1
                    url = URL_SPEECHES.format(page = page)
                    bar.update(page)                    
                    curr_file = _download_page(session, page, folder_out)
        else:
            print(f'robots.txt forbids url: {url}')

@typechecked
def _setup_robots_txt(session: requests.Session) -> protego.Protego:
    """
    Gets the robots.txt from the WHO and makes our parser

    Parameters
    ----------
    session: requests.Session
        The browser session
    """
    with session.get(URL_ROBOTS) as response:
        rtxt = protego.Protego.parse(response.text)
    return rtxt

@typechecked
def _download_page(session: requests.Session, page: int, folder_out: pathlib.Path) -> pathlib.Path:
    """
    Get a single page worth of speeches.

    Parameters
    ----------
    session: requests.Session
        The browser session
    page : int
        The page in question
    folder_out : pathlib.Path
        Folder to contain the downloaded documents
    """

    url = URL_SPEECHES.format(page = page)
    result_path = folder_out.joinpath( f'./header.{_run_id}.{page}.html')
    with session.get(url) as response:
        if response.status_code == 200:
            with open(result_path, 'w', encoding = 'utf-8') as fp:
                fp.write(response.text)
            return result_path
        else:
            print(f'could not open ({response.status_code}) url: {url}')

@typechecked
def _has_more_pages(file_path: pathlib.Path) -> bool:
    """
    Determines if the file has another page past `page`
    
    Parameters
    ----------
    file_path : pathlib.Path
        The path to the current page
    """
    with open(file_path, 'r', encoding = 'utf-8') as fp:
        tree = etree.parse(fp, etree.HTMLParser())
    node = tree.find("//ul[@class='pagination']/li[last()]/a")
    result = 'aria-label' in node.attrib and node.attrib['aria-label'] == 'Next'
    return result

@typechecked
def _need_more_pages(file_path: pathlib.Path) -> bool:
    """
    Determines if more pages need downloading for the current run

    Parameters
    ----------
    file_path : pathlib.Path
        The path to the current page
    """

    # get prior run
    curr_run = file_path.stem[7:21]
    file_paths = [f for f in file_path.parent.iterdir() if f.suffix == '.html' and f.stem.startswith('header.')]
    file_paths = [f.stem[7:21] for f in file_paths if f.stem.endswith('.1')]
    file_paths = [f for f in file_paths if f < curr_run]
    file_paths = [f for f in sorted(file_paths, reverse = True)]

    if len(file_paths) == 0:
        return True

    prior_run = file_path.parent.joinpath(f'header.{file_paths[0]}.1.html')

    curr_last_date = _speech_date(file_path, False)
    prior_first_date = _speech_date(prior_run, True)
    result = curr_last_date >= prior_first_date
    return result

@typechecked
def _speech_date(file_path: pathlib.Path, first: bool) -> datetime.date:
    """
    Gets the date of a particular speech on the page

    Parameters
    ----------
    file_path : pathlib.Path
        The path to the current page
    first : bool
        Get the first speech's date (True) xor last speech's date (False)
    """
    fxol = '1' if first else 'last()'
    xpath = f"//div[@class='list-view vertical-list vertical-list--image']/div[{fxol}]/a/div/div[@class='date']/span"

    with open(file_path, 'r', encoding = 'utf-8') as fp:
        tree = etree.parse(fp, etree.HTMLParser())
    node = tree.find(xpath)
    result = datetime.strptime(node.text, '%d %B %Y')
    return result.date()
