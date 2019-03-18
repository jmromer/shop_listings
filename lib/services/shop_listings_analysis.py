"""
Source data from the Etsy API and perform key terms analysis of shop listings
text.
"""

from datetime import datetime as dt
from logging import Logger
from typing import Any, Dict

import ujson as json
from redis import StrictRedis

from services.etsy_shop import EtsyShop
from services.key_terms import compute_key_terms


def perform_analysis(
        shop_name: str,
        logger: Logger,
        log_level: str,
        etsy_api_key: str,
        max_number_of_terms: int,
        redis_store: StrictRedis,
) -> Dict[str, Any]:
    """
    Request listings for the given Etsy shop SHOP_NAME.
    Determine the key terms across the corpus of listing text.

    Note: Used cached values where possible.
    TODO: Re-source data and recompute if the cached data is stale.

    Return a dict containing the key terms.
    """
    cache_key = f'etsy:{shop_name}'
    cache_hit = redis_store.get(cache_key)

    if cache_hit:
        payload = json.loads(cache_hit)
        del payload['corpus']
        return payload

    # source listings from the etsy api
    shop = EtsyShop(
        name=shop_name,
        log_level=log_level,
        api_key=etsy_api_key,
        logger=logger,
    ).get_active_listings()

    # determine key terms across the corpus of listing text
    corpus = [f"{l['title']} {l['description']}" for l in shop.listings]
    key_terms = compute_key_terms(corpus, number=max_number_of_terms)

    payload = {
        'shop_name': shop_name,
        'corpus': corpus,
        'key_terms': key_terms,
        'saved_at': int(dt.utcnow().strftime('%s')),
    }

    if shop_name and corpus and key_terms:
        redis_store.set(cache_key, json.dumps(payload))

    del payload['corpus']
    return payload
