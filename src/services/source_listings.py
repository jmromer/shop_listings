"""
Write shop listings data, sourced from the Etsy API, to CSV.
"""

import csv
import logging
import os

import dotenv
from requests_futures.sessions import FuturesSession

from etsy_shop import EtsyShop

logging.basicConfig(level=logging.INFO)

dotenv.load_dotenv()

LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
OUTPUT_FILE = os.getenv('OUTPUT_FILE', './data/shop_listings.csv')
SUBSET = os.getenv('SUBSET') is not None

ETSY_API_KEY = os.getenv('ETSY_API_KEY', '')
ETSY_API_BASE_URL = os.getenv('ETSY_API_BASE_URL', '')
ETSY_API_MAX_REQ_PER_SEC = int(os.getenv('ETSY_API_MAX_REQ_PER_SEC', '10'))

SHOP_NAMES = [
    'AgnesHart',
    'DesignsByBrandiCo',
    'IttyBittyBookCo',
    'MusePortfolios',
    'TheCamillaStore',
    'TwoWoodenDots',
    'cozyblue',
    'hushedcommotion',
    'irenestrange',
    'turbansfortots',
]

if SUBSET:
    SHOP_NAMES = SHOP_NAMES[0:2]


def write_listings_to_csv(filename: str) -> None:
    """
    Source listings data from the Etsy API for the given SHOP_NAMES,
    write them to a CSV file (in ./data/shops.csv by default).
    """
    with open(filename, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['shop_name', 'text'])
        writer.writeheader()

        session = FuturesSession()
        shops = [
            EtsyShop(
                name=shop_name,
                log_level=LOG_LEVEL,
                api_key=ETSY_API_KEY,
                api_base_url=ETSY_API_BASE_URL,
                api_max_reqs_per_sec=ETSY_API_MAX_REQ_PER_SEC,
                session=session,
            ) for shop_name in SHOP_NAMES
        ]

        for shop in [shop.get_active_listings() for shop in shops]:
            for listing in shop.listings:
                writer.writerow({
                    'shop_name':
                    shop.name,
                    'text':
                    listing['title'] + ' ' + listing['description'],
                })


if __name__ == '__main__':
    write_listings_to_csv(OUTPUT_FILE)
