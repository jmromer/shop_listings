const baseUrl = ''

const jsonHeaders = {
  Accept: 'application/json',
  'Content-Type': 'application/json',
  credentials: 'same-origin'
}

const getShopNames = () => {
  return window
    .fetch(`${baseUrl}/shop-names`, {
      method: 'GET',
      headers: jsonHeaders
    })
    .then(resp => resp.json())
    .then(json => json.listing)
}

const getKeyTerms = shopName => {
  return window
    .fetch(`${baseUrl}/key-terms?q=${shopName}`, {
      method: 'GET',
      headers: jsonHeaders
    })
    .then(resp => resp.json())
    .then(json => json.results[0])
}

export { getShopNames, getKeyTerms }
