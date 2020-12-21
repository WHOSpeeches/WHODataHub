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

_run_id = datetime.utcnow().strftime('%Y%m%d%H%M%S')

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
                for url in fp.readlines():
                    if rtxt.can_fetch(const.USER_AGENT, url):
                        bar.update(speech)
                        speech = speech + 1
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
    #args = parser.parse_args()
    #print(f'file in: {args.file_in}')
    #print(f'folder out: {args.folder_out}')
    #get_speeches_text(args.file_in, args.folder_out)
    get_speeches_text(pathlib.Path('d:/datasets/who/speeches.txt'), pathlib.Path('d:/datasets/who/raw'))
