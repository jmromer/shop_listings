from typing import List

import requests
import ujson as json
from redis import StrictRedis


def get_shops_list(etsy_api_key: str,
                   max_stores: int,
                   redis_store: StrictRedis,
                   page: int = 1) -> List[str]:
    """TODO: Implement cache invalidation."""
    cache_key = f'etsy_store_list:page-{page}-num-{max_stores}'
    cache_hit = redis_store.get(cache_key)
    if cache_hit:
        return json.loads(cache_hit)

    api_base_url = 'https://openapi.etsy.com/v2'
    query = {'api_key': etsy_api_key, 'limit': max_stores, page: page}
    resp = requests.get(f'{api_base_url}/shops', params=query)

    if resp.status_code != 200:
        return []

    stores = resp.json()['results']
    shop_names = [store['shop_name'] for store in stores]
    redis_store.set(cache_key, json.dumps(shop_names))
    return shop_names
