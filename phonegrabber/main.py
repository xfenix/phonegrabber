import re
import asyncio
import logging
from typing import Sequence, Optional

import aiohttp


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('phonegrabber')

PHONES_RE = re.compile(r'((!|\?|>|\.|,|-|:|\s)\s*(8|\+7)\s*?(|\()(4|8|9)\d{2}(|\))\s*?\d{3}(-|\s*?|)\d{2}(-|\s*?|)\d{2})')
CLEAN_PHONE_RE = re.compile(r'[^\d+]')


async def fetch_and_process_one_page(session: aiohttp.ClientSession, page_url: str) -> Optional[set]:
    """Download one page and search for phones
    """
    try:
        async with session.get(page_url) as response:
            logger.info('Processing {}...'.format(page_url))
            if response.status == 200:
                page_body = await response.text()
                return extract_phone_numbers(page_body)
            else:
                logger.error('Incorrect server answer')
                return None
    except aiohttp.ClientConnectorError as exc:
        logger.error('Connection error, trace: {}'.format(exc))
        return None


async def fetch_all_pages(pages: Sequence) -> Optional[set]:
    """Download multiple pages and wait when all of them is done
    """
    async with aiohttp.ClientSession() as session:
        results = await asyncio.gather(
            *[fetch_and_process_one_page(session, page_url) for page_url in pages], return_exceptions=True)
        results = filter(lambda x: type(x) == set, results)
        return set.union(*results)


def normalize_phone_number(one_phone: str) -> str:
    """Simple phone normalization to 8KKKNNNNNNN format
    """
    return CLEAN_PHONE_RE.sub('', one_phone.replace('+7', '8'))


def extract_phone_numbers(text: str) -> set:
    """Phones extraction from text
    """
    page_phones = PHONES_RE.finditer(text)
    ready_phones = set()
    for one_phone in page_phones:
        try:
            ready_phones.add(normalize_phone_number(one_phone.group(0)))
        except IndexError as exc:
            logger.error('Cant phone fetch group 0 from Match object, trace: {}'.format(exc))
    return ready_phones


def validate_pages_urls(pages: Sequence) -> (list, set):
    """Simple (and stupid) validation, process all page urls and
    returns bad and good, separated in two different sequences
    We are using set for good pages to avoid multiple queries for duplicated domains
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
    if not pages or len(pages) == 0:
        logger.error('Empty/wrong input')
        return None
    good_urls, bad_urls = validate_pages_urls(pages)
    if len(bad_urls) > 0:
        logger.info('Bad urls are skipped: {}'.format(bad_urls))
    if len(good_urls) > 0:
        return asyncio.run(fetch_all_pages(good_urls))
    else:
        logger.error('There is no good pages urls')


def cli_handler():
    """Console handler for entrypoint in setup.py or manual script call
    """
    import argparse

    parser = argparse.ArgumentParser(description='Process urls list and returns phones in 8KKKNNNNNNN format')
    parser.add_argument('pages', metavar='page_url', type=str, nargs='+', help='an url for the grabber')
    parsed_args = parser.parse_args()

    results = grab_pages(parsed_args.pages)
    if results:
        logger.info('All done. Results here: {}'.format(results))
    else:
        logger.error('There is no results from parser')


if __name__ == '__main__':
    cli_handler()
