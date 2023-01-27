
from lxml import etree # type: ignore

def has_more_pages(page: str) -> bool:
    """
    Determines if the HTML page has another past `page`
    
    Parameters
    ----------
    file_path : pathlib.Path
        The path to the current page
    """
    tree = etree.fromstring(page, etree.HTMLParser()) # type: ignore
    node = tree.find("//ul[@class='pagination']/li[last()]/a")
    result = 'aria-label' in node.attrib and node.attrib['aria-label'] == 'Next'
    return result