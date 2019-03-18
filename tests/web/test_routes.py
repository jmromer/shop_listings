import vcr


def test_index_route(client):
    resp = client.get('/')
    assert resp.status_code == 200


def test_key_terms_route_requires_query_string(client):
    resp = client.get('/key-terms')
    assert resp.status_code == 422
    assert resp.json['error'] == 'missing query string'
    resp = client.get('/key-terms?')
    assert resp.status_code == 422
    assert resp.json['error'] == 'missing query string'
    resp = client.get('/key-terms?name')
    assert resp.status_code == 422
    assert resp.json['error'] == 'missing query string'
    resp = client.get('/key-terms?name=whatever')
    assert resp.status_code == 422
    assert resp.json['error'] == 'missing query string'


def test_key_terms_route_responds_with_json(mocker, client):
    cassette = 'tests/cassettes/etsy_active_listings_drews_tattoos.yml'
    with vcr.use_cassette(cassette):
        resp = client.get('/key-terms?q=DrewsTattoos')
        assert resp.status_code == 200

        [res] = resp.json['results']
        assert sorted(res.keys()) == ['key_terms', 'saved_at', 'shop_name']
        assert res['shop_name'] == 'DrewsTattoos'
        assert res['key_terms'] == 'days drew tattoo tattoos temporary'.split()
