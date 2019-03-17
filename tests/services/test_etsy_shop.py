import pytest

from services.etsy_shop import EtsyShop


def test_etsy_shop_initialization():
    shop = EtsyShop(name='DrewsTattoos', api_key='DUMMY_API_KEY')
    assert shop.name == 'DrewsTattoos'


def test_active_listings_url_returns_a_url():
    shop = EtsyShop(
        name='DrewsTattoos',
        api_key='DUMMY_API_KEY',
        api_base_url='https://some-subdomain.etsy.com')
    assert 'https://some-subdomain.etsy.com' in shop.active_listings_url
    assert 'DrewsTattoos/listings/active' in shop.active_listings_url


def test_active_listings_query_dict_returns_params_dict():
    shop = EtsyShop(
        name='DrewsTattoos', api_key='DUMMY_API_KEY', api_query_limit=235)

    query = shop.active_listings_query_dict(page=22)

    assert list(query.keys()) == ['api_key', 'page', 'limit']
    assert query['api_key'] == 'DUMMY_API_KEY'
    assert query['page'] == 22
    assert query['limit'] == 235


def test_active_listings_query_dict_returns_params_dict_with_defaults():
    shop = EtsyShop(name='DrewsTattoos', api_key='DUMMY_API_KEY')
    query = shop.active_listings_query_dict()
    assert query['page'] == 1
    assert query['limit'] == 25


@pytest.mark.vcr()
def test_get_active_listings_queries_for_all_pages_of_results():
    """listings property is set from API response as expected."""
    shop = EtsyShop(name='DrewsTattoos', api_key='DUMMY_API_KEY')

    shop.get_active_listings()

    assert len(shop.listings) == 29
    assert all(isinstance(listing, dict) for listing in shop.listings)
    assert all('title' in listing and 'description' in listing
               for listing in shop.listings)
