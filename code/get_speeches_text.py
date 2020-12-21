import const
import pathlib
import time
import requests
import protego
import progressbar as pb
from argparse import ArgumentParser
from datetime import datetime
from lxml import etree
from typeguard import typechecked

@typechecked
def get_speeches_text(file_in: pathlib.Path, folder_out: pathlib.Path) -> None:
    """
    Get the text of all of the WHO director general's speeches.
    When running the 2nd time, check your local copy to determine how far back you need to pull.

    Parameters
    ----------
    file_in : pathlib.Path
        File containing the list to download
    folder_out : pathlib.Path
        Folder to contain the downloaded documents
    """

    if not file_in.exists():
        raise RuntimeError(f'Could not find the list of speeches to download: {file_in}')
    folder_out.mkdir(parents = True, exist_ok = True)

    with requests.Session() as session:
        session.headers['User-Agent'] = const.USER_AGENT
        rtxt = _setup_robots_txt(session)
        speech = 1
        widgets = [ 'Retrieving Speech # ', pb.Counter(), ' ', pb.BouncingBar(marker = '.', left = '[', right = ']'), ' ', pb.Timer()]
        with pb.ProgressBar(widgets = widgets) as bar:
            with open(file_in, 'r', encoding = 'utf-8') as fp:
                for line in fp.readlines():
                    url = line.strip()
                    if rtxt.can_fetch(const.USER_AGENT, url):
                        bar.update(speech)
                        speech = speech + 1
                        if _needs_download(folder_out, url):
                            _download_speech(session, folder_out, url)
                            _take_a_nap(rtxt)
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
    with session.get(const.URL_ROBOTS) as response:
        rtxt = protego.Protego.parse(response.text)
    return rtxt

@typechecked
def _needs_download(folder_out: pathlib.Path, url: str) -> bool:
    """
    Get a single speech.

    Parameters
    ----------
    folder_out : pathlib.Path
        Folder to contain the downloaded documents
    url : str
        The URL to download
    """

    result_path = _url_to_filepath(folder_out, url)
    result = not result_path.exists()
    return result

@typechecked
def _url_to_filepath(folder_out: pathlib.Path, url: str) -> pathlib.Path:
    h = 0
    url = url.upper()
    for c in url:
        h = (h + ord(c)) % 1073741843
    result_path = folder_out.joinpath( f'./detail.{h:010d}.html')
    return result_path

@typechecked
def _download_speech(session: requests.Session, folder_out: pathlib.Path, url: str) -> None:
    """
    Get a single speech.

    Parameters
    ----------
    session: requests.Session
        The browser session
    folder_out : pathlib.Path
        Folder to contain the downloaded documents
    url : str
        The URL to download
    """

    result_path = _url_to_filepath(folder_out, url)
    with session.get(url) as response:
        if response.status_code == 200:
            with open(result_path, 'w', encoding = 'utf-8') as fp:
                fp.write(response.text)
        else:
            print(f'could not open ({response.status_code}) url: {url}')

@typechecked
def _take_a_nap(rtxt: protego.Protego) -> None:
    delay = rtxt.crawl_delay(const.USER_AGENT)
    delay = delay if delay is not None else const.WEB_DELAY
    time.sleep(delay)

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument(
        '-in', '--file-in',
        help = 'File containing the list to download',
        type = pathlib.Path,
        required = True)
    parser.add_argument(
        '-out', '--folder-out',
        help = 'Folder to contain the downloaded documents',
        type = pathlib.Path,
        required = True)
    args = parser.parse_args()
    print(f'file in: {args.file_in}')
    print(f'folder out: {args.folder_out}')
    get_speeches_text(args.file_in, args.folder_out)
