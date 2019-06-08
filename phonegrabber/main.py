import re
import asyncio
from typing import Sequence, Optional

import aiohttp


PHONES_RE = re.compile(r'((8|\+7)\s*?(|\()(4|8|9)\d{2}(|\))\s*?\d{3}(-|\s*?|)\d{2}(-|\s*?|)\d{2})', flags=re.U)
CLEAN_PHONE_RE = re.compile(r'[^\d+]')


async def fetch_and_process_one_page(session: aiohttp.ClientSession, page_url: str) -> set:
    """Download one page and search for phones
    """
    async with session.get(page_url) as response:
        print('Processing {}...'.format(page_url))
        page_body = await response.text()
        page_phones = PHONES_RE.finditer(page_body)
        ready_phones = set()
        for one_phone in page_phones:
            # normalize phone to 8KKKNNNNNNN format
            # a little bit of harcode
            ready_phones.add(
                CLEAN_PHONE_RE.sub('', one_phone.group(0).replace('+7', '8')))
        return ready_phones


async def fetch_all_pages(pages: Sequence) -> Optional[set]:
    """Download multiple pages and wait when all of them is done
    """
    async with aiohttp.ClientSession() as session:
        results = await asyncio.gather(
            *[fetch_and_process_one_page(session, page_url) for page_url in pages],
            return_exceptions=True)
        return set.union(*results)


def validate_pages_urls(pages: Sequence) -> (list, set):
    """Simple (and stupid) validation, process all page urls and returns those are not valid
    """
    bad_pages = []
    good_pages = set()
    for one_page in pages:
        if one_page.startswith('http://') or\
           one_page.startswith('https://') or\
           one_page.startswith('//'):
            good_pages.add(one_page)
        else:
            bad_pages.append(one_page)
    return good_pages, bad_pages 


def grab_pages(pages: Sequence) -> Optional[Sequence]:
    """Core function, all work happens here
    """
    good_urls, bad_urls = validate_pages_urls(pages)
    if len(bad_urls) > 0:
        print('Bad urls are skipped: {}'.format(bad_urls))
    if len(good_urls) > 0:
        return asyncio.run(fetch_all_pages(good_urls))
    else:
        print('There is no good pages urls')


def cli_handler():
    """Console handler for entrypoint in setup.py or manual script call
    """
    import argparse

    parser = argparse.ArgumentParser(description='Process urls list and returns phones in 8KKKNNNNNNN format')
    parser.add_argument('pages', metavar='page_url', type=str, nargs='+', help='an url for the grabber')
    parsed_args = parser.parse_args()

    results = grab_pages(parsed_args.pages)
    if results:
        print('All done. Results here: {}'.format(results))
    else:
        print('There is no results from parser')


if __name__ == '__main__':
    cli_handler()
